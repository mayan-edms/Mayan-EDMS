from __future__ import absolute_import, unicode_literals

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.common.generics import FormView, SingleObjectListView
from mayan.apps.documents.models import Document

from ..forms import WorkflowInstanceTransitionForm
from ..icons import icon_workflow_instance_detail, icon_workflow_list
from ..links import link_workflow_instance_transition
from ..models import WorkflowInstance
from ..permissions import permission_workflow_view

__all__ = (
    'DocumentWorkflowInstanceListView', 'WorkflowInstanceDetailView',
    'WorkflowInstanceTransitionView'
)


class DocumentWorkflowInstanceListView(SingleObjectListView):
    def dispatch(self, request, *args, **kwargs):
        AccessControlList.objects.check_access(
            obj=self.get_document(), permissions=(permission_workflow_view,),
            user=request.user
        )

        return super(
            DocumentWorkflowInstanceListView, self
        ).dispatch(request, *args, **kwargs)

    def get_document(self):
        return get_object_or_404(klass=Document, pk=self.kwargs['pk'])

    def get_extra_context(self):
        return {
            'hide_link': True,
            'no_results_icon': icon_workflow_list,
            'no_results_text': _(
                'Assign workflows to the document type of this document '
                'to have this document execute those workflows. '
            ),
            'no_results_title': _(
                'There are no workflow for this document'
            ),
            'object': self.get_document(),
            'title': _(
                'Workflows for document: %s'
            ) % self.get_document(),
        }

    def get_source_queryset(self):
        return self.get_document().workflows.all()


class WorkflowInstanceDetailView(SingleObjectListView):
    def dispatch(self, request, *args, **kwargs):
        AccessControlList.objects.check_access(
            obj=self.get_workflow_instance().document,
            permissions=(permission_workflow_view,), user=request.user
        )

        return super(
            WorkflowInstanceDetailView, self
        ).dispatch(request, *args, **kwargs)

    def get_extra_context(self):
        return {
            'hide_object': True,
            'navigation_object_list': ('object', 'workflow_instance'),
            'no_results_icon': icon_workflow_instance_detail,
            'no_results_main_link': link_workflow_instance_transition.resolve(
                context=RequestContext(
                    dict_={'object': self.get_workflow_instance()},
                    request=self.request
                )
            ),
            'no_results_text': _(
                'This view will show the state changes as a workflow '
                'instance is transitioned.'
            ),
            'no_results_title': _(
                'There are no details for this workflow instance'
            ),
            'object': self.get_workflow_instance().document,
            'title': _('Detail of workflow: %(workflow)s') % {
                'workflow': self.get_workflow_instance()
            },
            'workflow_instance': self.get_workflow_instance(),
        }

    def get_source_queryset(self):
        return self.get_workflow_instance().log_entries.order_by('-datetime')

    def get_workflow_instance(self):
        return get_object_or_404(klass=WorkflowInstance, pk=self.kwargs['pk'])


class WorkflowInstanceTransitionView(FormView):
    form_class = WorkflowInstanceTransitionForm
    template_name = 'appearance/generic_form.html'

    def form_valid(self, form):
        self.get_workflow_instance().do_transition(
            comment=form.cleaned_data['comment'],
            transition=form.cleaned_data['transition'], user=self.request.user
        )
        messages.success(
            self.request, _(
                'Document "%s" transitioned successfully'
            ) % self.get_workflow_instance().document
        )
        return HttpResponseRedirect(redirect_to=self.get_success_url())

    def get_extra_context(self):
        return {
            'navigation_object_list': ('object', 'workflow_instance'),
            'object': self.get_workflow_instance().document,
            'submit_label': _('Submit'),
            'title': _(
                'Do transition for workflow: %s'
            ) % self.get_workflow_instance(),
            'workflow_instance': self.get_workflow_instance(),
        }

    def get_form_extra_kwargs(self):
        return {
            'user': self.request.user,
            'workflow_instance': self.get_workflow_instance()
        }

    def get_success_url(self):
        return self.get_workflow_instance().get_absolute_url()

    def get_workflow_instance(self):
        return get_object_or_404(klass=WorkflowInstance, pk=self.kwargs['pk'])
