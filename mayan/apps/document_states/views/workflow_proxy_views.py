from __future__ import absolute_import, unicode_literals

from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.common.generics import SingleObjectListView
from mayan.apps.documents.models import Document
from mayan.apps.documents.views import DocumentListView

from ..icons import icon_workflow_list
from ..links import link_setup_workflow_create, link_setup_workflow_state_create
from ..models import WorkflowRuntimeProxy, WorkflowStateRuntimeProxy
from ..permissions import permission_workflow_view

__all__ = (
    'WorkflowDocumentListView', 'WorkflowListView',
    'WorkflowStateDocumentListView', 'WorkflowStateListView'
)


class WorkflowDocumentListView(DocumentListView):
    def dispatch(self, request, *args, **kwargs):
        self.workflow = get_object_or_404(
            klass=WorkflowRuntimeProxy, pk=self.kwargs['pk']
        )

        AccessControlList.objects.check_access(
            obj=self.workflow, permissions=(permission_workflow_view,),
            user=request.user
        )

        return super(
            WorkflowDocumentListView, self
        ).dispatch(request, *args, **kwargs)

    def get_document_queryset(self):
        return Document.objects.filter(workflows__workflow=self.workflow)

    def get_extra_context(self):
        context = super(WorkflowDocumentListView, self).get_extra_context()
        context.update(
            {
                'no_results_text': _(
                    'Associate a workflow with some document types and '
                    'documents of those types will be listed in this view.'
                ),
                'no_results_title': _(
                    'There are no documents executing this workflow'
                ),
                'object': self.workflow,
                'title': _('Documents with the workflow: %s') % self.workflow
            }
        )
        return context


class WorkflowListView(SingleObjectListView):
    object_permission = permission_workflow_view

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_workflow_list,
            'no_results_main_link': link_setup_workflow_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Create some workflows and associated them with a document '
                'type. Active workflows will be shown here and the documents '
                'for which they are executing.'
            ),
            'no_results_title': _('There are no workflows'),
            'title': _('Workflows'),
        }

    def get_source_queryset(self):
        return WorkflowRuntimeProxy.objects.all()


class WorkflowStateDocumentListView(DocumentListView):
    def get_document_queryset(self):
        return self.get_workflow_state().get_documents()

    def get_extra_context(self):
        workflow_state = self.get_workflow_state()
        context = super(WorkflowStateDocumentListView, self).get_extra_context()
        context.update(
            {
                'object': workflow_state,
                'navigation_object_list': ('object', 'workflow'),
                'no_results_title': _(
                    'There are no documents in this workflow state'
                ),
                'title': _(
                    'Documents in the workflow "%s", state "%s"'
                ) % (
                    workflow_state.workflow, workflow_state
                ),
                'workflow': WorkflowRuntimeProxy.objects.get(
                    pk=workflow_state.workflow.pk
                ),
            }
        )
        return context

    def get_workflow_state(self):
        workflow_state = get_object_or_404(
            klass=WorkflowStateRuntimeProxy, pk=self.kwargs['pk']
        )

        AccessControlList.objects.check_access(
            obj=workflow_state.workflow,
            permissions=(permission_workflow_view,), user=self.request.user
        )

        return workflow_state


class WorkflowStateListView(SingleObjectListView):
    def dispatch(self, request, *args, **kwargs):
        AccessControlList.objects.check_access(
            obj=self.get_workflow(), permissions=(permission_workflow_view,),
            user=request.user
        )

        return super(
            WorkflowStateListView, self
        ).dispatch(request, *args, **kwargs)

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_main_link': link_setup_workflow_state_create.resolve(
                context=RequestContext(
                    request=self.request, dict_={'object': self.get_workflow()}
                )
            ),
            'no_results_text': _(
                'Create states and link them using transitions.'
            ),
            'no_results_title': _(
                'This workflow doesn\'t have any state'
            ),
            'object': self.get_workflow(),
            'title': _('States of workflow: %s') % self.get_workflow()
        }

    def get_source_queryset(self):
        return WorkflowStateRuntimeProxy.objects.filter(
            workflow=self.get_workflow()
        )

    def get_workflow(self):
        return get_object_or_404(
            klass=WorkflowRuntimeProxy, pk=self.kwargs['pk']
        )
