from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.generics import SingleObjectListView
from mayan.apps.common.mixins import ExternalObjectMixin
from mayan.apps.documents.models import Document
from mayan.apps.documents.views.document_views import DocumentListView

from ..icons import icon_workflow_template_list
from ..links import link_workflow_template_create, link_workflow_template_state_create
from ..models import WorkflowRuntimeProxy, WorkflowStateRuntimeProxy
from ..permissions import permission_workflow_view


class WorkflowRuntimeProxyDocumentListView(
    ExternalObjectMixin, DocumentListView
):
    external_object_class = WorkflowRuntimeProxy
    external_object_permission = permission_workflow_view
    external_object_pk_url_kwarg = 'workflow_runtime_proxy_id'

    def get_document_queryset(self):
        return Document.objects.filter(
            workflows__workflow=self.external_object
        )

    def get_extra_context(self):
        context = super(
            WorkflowRuntimeProxyDocumentListView, self
        ).get_extra_context()
        context.update(
            {
                'no_results_text': _(
                    'Associate a workflow with some document types and '
                    'documents of those types will be listed in this view.'
                ),
                'no_results_title': _(
                    'There are no documents executing this workflow'
                ),
                'object': self.external_object,
                'title': _(
                    'Documents with the workflow: %s'
                ) % self.external_object
            }
        )
        return context


class WorkflowRuntimeProxyListView(SingleObjectListView):
    model = WorkflowRuntimeProxy
    object_permission = permission_workflow_view

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_workflow_template_list,
            'no_results_main_link': link_workflow_template_create.resolve(
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


class WorkflowRuntimeProxyStateDocumentListView(
    ExternalObjectMixin, DocumentListView
):
    external_object_class = WorkflowStateRuntimeProxy
    external_object_permission = permission_workflow_view
    external_object_pk_url_kwarg = 'workflow_runtime_proxy_state_id'

    def get_document_queryset(self):
        return self.external_object.get_documents()

    def get_extra_context(self):
        context = super(
            WorkflowRuntimeProxyStateDocumentListView, self
        ).get_extra_context()
        context.update(
            {
                'object': self.external_object,
                'navigation_object_list': ('object', 'workflow'),
                'no_results_title': _(
                    'There are no documents in this workflow state'
                ),
                'title': _(
                    'Documents in the workflow "%s", state "%s"'
                ) % (
                    self.external_object.workflow, self.external_object
                ),
                'workflow': WorkflowRuntimeProxy.objects.get(
                    pk=self.external_object.workflow.pk
                ),
            }
        )
        return context


class WorkflowRuntimeProxyStateListView(
    ExternalObjectMixin, SingleObjectListView
):
    external_object_class = WorkflowRuntimeProxy
    external_object_permission = permission_workflow_view
    external_object_pk_url_kwarg = 'workflow_runtime_proxy_id'

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_main_link': link_workflow_template_state_create.resolve(
                context=RequestContext(
                    request=self.request, dict_={'object': self.external_object}
                )
            ),
            'no_results_text': _(
                'Create states and link them using transitions.'
            ),
            'no_results_title': _(
                'This workflow doesn\'t have any state'
            ),
            'object': self.external_object,
            'title': _('States of workflow: %s') % self.external_object
        }

    def get_source_queryset(self):
        return WorkflowStateRuntimeProxy.objects.filter(
            workflow=self.external_object
        )
