from django.template import RequestContext
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.generics import (
    SingleObjectCreateView, SingleObjectDeleteView, SingleObjectEditView,
    SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectViewMixin

from ..forms import WorkflowStateEscalationForm
from ..icons import (
    icon_workflow_template_state_escalation_create,
    icon_workflow_template_state_escalation_delete,
    icon_workflow_template_state_escalation_edit,
    icon_workflow_template_state_escalation_list,
    icon_workflow_template_state_escalation
)
from ..links import link_workflow_template_state_escalation_create
from ..models import WorkflowState, WorkflowStateEscalation
from ..permissions import (
    permission_workflow_template_edit, permission_workflow_template_view
)


class WorkflowTemplateStateEscalationCreateView(
    ExternalObjectViewMixin, SingleObjectCreateView
):
    external_object_class = WorkflowState
    external_object_permission = permission_workflow_template_edit
    external_object_pk_url_kwarg = 'workflow_template_state_id'
    form_class = WorkflowStateEscalationForm
    view_icon = icon_workflow_template_state_escalation_create

    def get_extra_context(self):
        return {
            'navigation_object_list': (
                'workflow_template_state', 'workflow_template',
            ),
            'title': _(
                'Create escalation for workflow state: %s'
            ) % self.external_object,
            'workflow_template': self.external_object.workflow,
            'workflow_template_state': self.external_object
        }

    def get_form_extra_kwargs(self):
        return {
            'workflow_template_state': self.external_object
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
            'state': self.external_object
        }

    def get_source_queryset(self):
        return self.external_object.escalations.all()

    def get_success_url(self):
        return reverse(
            viewname='document_states:workflow_template_state_escalation_list',
            kwargs={
                'workflow_template_state_id': self.kwargs[
                    'workflow_template_state_id'
                ]
            }
        )


class WorkflowTemplateStateEscalationDeleteView(SingleObjectDeleteView):
    model = WorkflowStateEscalation
    object_permission = permission_workflow_template_edit
    pk_url_kwarg = 'workflow_template_state_escalation_id'
    view_icon = icon_workflow_template_state_escalation_delete

    def get_extra_context(self):
        return {
            'navigation_object_list': (
                'object', 'workflow_template_state', 'workflow_template'
            ),
            'object': self.object,
            'title': _('Delete workflow state escalation: %s') % self.object,
            'workflow_template': self.object.state.workflow,
            'workflow_template_state': self.object.state,
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }

    def get_post_escalation_redirect(self):
        return reverse(
            viewname='document_states:workflow_template_state_escalation_list',
            kwargs={
                'workflow_template_state_id': self.object.state.pk
            }
        )


class WorkflowTemplateStateEscalationEditView(SingleObjectEditView):
    form_class = WorkflowStateEscalationForm
    model = WorkflowStateEscalation
    object_permission = permission_workflow_template_edit
    pk_url_kwarg = 'workflow_template_state_escalation_id'
    view_icon = icon_workflow_template_state_escalation_edit

    def get_extra_context(self):
        return {
            'navigation_object_list': (
                'object', 'workflow_template_state', 'workflow_template',
            ),
            'object': self.object,
            'title': _('Edit workflow state escalation: %s') % self.object,
            'workflow_template': self.object.state.workflow,
            'workflow_template_state': self.object.state,
        }

    def get_form_extra_kwargs(self):
        return {
            'workflow_template_state': self.object.state
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class WorkflowTemplateStateEscalationListView(
    ExternalObjectViewMixin, SingleObjectListView
):
    external_object_class = WorkflowState
    external_object_permission = permission_workflow_template_view
    external_object_pk_url_kwarg = 'workflow_template_state_id'
    view_icon = icon_workflow_template_state_escalation_list

    def get_extra_context(self):
        return {
            'hide_object': True,
            'navigation_object_list': (
                'workflow_template_state', 'workflow_template',
            ),
            'no_results_icon': icon_workflow_template_state_escalation,
            'no_results_main_link': link_workflow_template_state_escalation_create.resolve(
                context=RequestContext(
                    request=self.request, dict_={
                        'object': self.external_object
                    }
                )
            ),
            'no_results_text': _(
                'Workflow state escalation allow workflows to execute a '
                'a transition automatically after a specific amount of time.'
            ),
            'no_results_title': _(
                'There are no escalations for this workflow state'
            ),
            'title': _(
                'Escalations for workflow template state: %s'
            ) % self.external_object,
            'workflow_template': self.external_object.workflow,
            'workflow_template_state': self.external_object
        }

    def get_source_queryset(self, queryset=None):
        return self.external_object.escalations.all()
