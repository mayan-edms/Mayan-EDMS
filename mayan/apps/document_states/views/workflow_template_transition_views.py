from __future__ import absolute_import, unicode_literals

from django.contrib import messages
from django.db import transaction
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.generics import (
    AddRemoveView, ConfirmView, FormView, SingleObjectCreateView,
    SingleObjectDeleteView, SingleObjectDetailView,
    SingleObjectDynamicFormCreateView, SingleObjectDynamicFormEditView,
    SingleObjectEditView, SingleObjectListView
)
from mayan.apps.common.mixins import ExternalObjectMixin
from mayan.apps.documents.events import event_document_type_edited
from mayan.apps.documents.models import DocumentType
from mayan.apps.documents.permissions import permission_document_type_edit
from mayan.apps.events.classes import EventType
from mayan.apps.events.models import StoredEventType

from ..classes import WorkflowAction
from ..events import event_workflow_edited
from ..forms import (
    WorkflowActionSelectionForm, WorkflowForm, WorkflowPreviewForm,
    WorkflowStateActionDynamicForm, WorkflowStateForm, WorkflowTransitionForm,
    WorkflowTransitionTriggerEventRelationshipFormSet
)
from ..icons import (
    icon_workflow_template_list, icon_workflow_state, icon_workflow_state_action,
    icon_workflow_transition, icon_workflow_transition_field
)
from ..links import (
    link_workflow_template_create, link_workflow_template_state_create,
    link_workflow_template_state_action_selection,
    link_workflow_template_transition_create,
    link_workflow_template_transition_field_create,
)
from ..models import (
    Workflow, WorkflowState, WorkflowStateAction, WorkflowTransition,
    WorkflowTransitionField
)
from ..permissions import (
    permission_workflow_create, permission_workflow_delete,
    permission_workflow_edit, permission_workflow_tools,
    permission_workflow_view,
)
from ..tasks import task_launch_all_workflows


class WorkflowTemplateTransitionCreateView(ExternalObjectMixin, SingleObjectCreateView):
    external_object_class = Workflow
    external_object_permission = permission_workflow_edit
    external_object_pk_url_kwarg = 'pk'
    form_class = WorkflowTransitionForm

    def get_extra_context(self):
        return {
            'object': self.get_workflow(),
            'title': _(
                'Create transitions for workflow: %s'
            ) % self.get_workflow()
        }

    def get_form_kwargs(self):
        kwargs = super(
            WorkflowTemplateTransitionCreateView, self
        ).get_form_kwargs()
        kwargs['workflow'] = self.get_workflow()
        return kwargs

    def get_instance_extra_data(self):
        return {'workflow': self.get_workflow()}

    def get_source_queryset(self):
        return self.get_workflow().transitions.all()

    def get_success_url(self):
        return reverse(
            viewname='document_states:workflow_template_transition_list',
            kwargs={'pk': self.kwargs['pk']}
        )

    def get_workflow(self):
        return self.external_object


class WorkflowTemplateTransitionDeleteView(SingleObjectDeleteView):
    model = WorkflowTransition
    object_permission = permission_workflow_edit
    pk_url_kwarg = 'pk'

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'navigation_object_list': ('object', 'workflow_instance'),
            'title': _(
                'Delete workflow transition: %s?'
            ) % self.object,
            'workflow_instance': self.get_object().workflow,
        }

    def get_success_url(self):
        return reverse(
            viewname='document_states:workflow_template_transition_list',
            kwargs={'pk': self.get_object().workflow.pk}
        )


class WorkflowTemplateTransitionEditView(SingleObjectEditView):
    form_class = WorkflowTransitionForm
    model = WorkflowTransition
    object_permission = permission_workflow_edit
    pk_url_kwarg = 'pk'

    def get_extra_context(self):
        return {
            'navigation_object_list': ('object', 'workflow_instance'),
            'object': self.get_object(),
            'title': _(
                'Edit workflow transition: %s'
            ) % self.object,
            'workflow_instance': self.get_object().workflow,
        }

    def get_form_kwargs(self):
        kwargs = super(
            WorkflowTemplateTransitionEditView, self
        ).get_form_kwargs()
        kwargs['workflow'] = self.get_object().workflow
        return kwargs

    def get_success_url(self):
        return reverse(
            viewname='document_states:workflow_template_transition_list',
            kwargs={'pk': self.get_object().workflow.pk}
        )


class WorkflowTemplateTransitionListView(ExternalObjectMixin, SingleObjectListView):
    external_object_class = Workflow
    external_object_permission = permission_workflow_view
    external_object_pk_url_kwarg = 'pk'
    object_permission = permission_workflow_view

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_workflow_transition,
            'no_results_main_link': link_workflow_template_transition_create.resolve(
                context=RequestContext(
                    self.request, {'object': self.get_workflow()}
                )
            ),
            'no_results_text': _(
                'Create a transition and use it to move a workflow from '
                ' one state to another.'
            ),
            'no_results_title': _(
                'This workflow doesn\'t have any transitions'
            ),
            'object': self.get_workflow(),
            'title': _(
                'Transitions of workflow: %s'
            ) % self.get_workflow()
        }

    def get_source_queryset(self):
        return self.get_workflow().transitions.all()

    def get_workflow(self):
        return self.external_object


class WorkflowTemplateTransitionTriggerEventListView(ExternalObjectMixin, FormView):
    external_object_class = WorkflowTransition
    external_object_permission = permission_workflow_edit
    external_object_pk_url_kwarg = 'pk'
    form_class = WorkflowTransitionTriggerEventRelationshipFormSet

    def dispatch(self, *args, **kwargs):
        EventType.refresh()
        return super(
            WorkflowTemplateTransitionTriggerEventListView, self
        ).dispatch(*args, **kwargs)

    def form_valid(self, form):
        try:
            for instance in form:
                instance.save()
        except Exception as exception:
            messages.error(
                message=_(
                    'Error updating workflow transition trigger events; %s'
                ) % exception, request=self.request

            )
        else:
            messages.success(
                message=_(
                    'Workflow transition trigger events updated successfully'
                ), request=self.request
            )

        return super(
            WorkflowTemplateTransitionTriggerEventListView, self
        ).form_valid(form=form)

    def get_extra_context(self):
        return {
            'form_display_mode_table': True,
            'navigation_object_list': ('object', 'workflow'),
            'object': self.get_object(),
            'subtitle': _(
                'Triggers are events that cause this transition to execute '
                'automatically.'
            ),
            'title': _(
                'Workflow transition trigger events for: %s'
            ) % self.get_object(),
            'workflow': self.get_object().workflow,
        }

    def get_initial(self):
        obj = self.get_object()
        initial = []

        # Return the queryset by name from the sorted list of the class
        event_type_ids = [event_type.id for event_type in EventType.all()]
        event_type_queryset = StoredEventType.objects.filter(
            name__in=event_type_ids
        )

        # Sort queryset in Python by namespace, then by label
        event_type_queryset = sorted(
            event_type_queryset, key=lambda x: (x.namespace, x.label)
        )

        for event_type in event_type_queryset:
            initial.append({
                'transition': obj,
                'event_type': event_type,
            })
        return initial

    def get_object(self):
        return self.external_object

    def get_post_action_redirect(self):
        return reverse(
            viewname='document_states:workflow_template_transition_list',
            kwargs={'pk': self.get_object().workflow.pk}
        )


class WorkflowTemplateTransitionFieldCreateView(ExternalObjectMixin, SingleObjectCreateView):
    external_object_class = WorkflowTransition
    external_object_permission = permission_workflow_edit
    fields = (
        'name', 'label', 'field_type', 'help_text', 'required', 'widget',
        'widget_kwargs'
    )

    def get_extra_context(self):
        return {
            'navigation_object_list': ('transition', 'workflow'),
            'transition': self.external_object,
            'title': _(
                'Create a field for workflow transition: %s'
            ) % self.external_object,
            'workflow': self.external_object.workflow
        }

    def get_instance_extra_data(self):
        return {
            'transition': self.external_object,
        }

    def get_queryset(self):
        return self.external_object.fields.all()

    def get_post_action_redirect(self):
        return reverse(
            viewname='document_states:workflow_template_transition_field_list',
            kwargs={'pk': self.external_object.pk}
        )


class WorkflowTemplateTransitionFieldDeleteView(SingleObjectDeleteView):
    model = WorkflowTransitionField
    object_permission = permission_workflow_edit

    def get_extra_context(self):
        return {
            'navigation_object_list': (
                'object', 'workflow_transition', 'workflow'
            ),
            'object': self.object,
            'title': _('Delete workflow transition field: %s') % self.object,
            'workflow': self.object.transition.workflow,
            'workflow_transition': self.object.transition,
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='document_states:workflow_template_transition_field_list',
            kwargs={'pk': self.object.transition.pk}
        )


class WorkflowTemplateTransitionFieldEditView(SingleObjectEditView):
    fields = (
        'name', 'label', 'field_type', 'help_text', 'required', 'widget',
        'widget_kwargs'
    )
    model = WorkflowTransitionField
    object_permission = permission_workflow_edit

    def get_extra_context(self):
        return {
            'navigation_object_list': (
                'object', 'workflow_transition', 'workflow'
            ),
            'object': self.object,
            'title': _('Edit workflow transition field: %s') % self.object,
            'workflow': self.object.transition.workflow,
            'workflow_transition': self.object.transition,
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='document_states:workflow_template_transition_field_list',
            kwargs={'pk': self.object.transition.pk}
        )


class WorkflowTemplateTransitionFieldListView(ExternalObjectMixin, SingleObjectListView):
    external_object_class = WorkflowTransition
    external_object_permission = permission_workflow_edit

    def get_extra_context(self):
        return {
            'hide_object': True,
            'navigation_object_list': ('object', 'workflow'),
            'no_results_icon': icon_workflow_transition_field,
            'no_results_main_link': link_workflow_template_transition_field_create.resolve(
                context=RequestContext(
                    request=self.request, dict_={
                        'object': self.external_object
                    }
                )
            ),
            'no_results_text': _(
                'Workflow transition fields allow adding data to the '
                'workflow\'s context. This additional context data can then '
                'be used by other elements of the workflow system like the '
                'workflow state actions.'
            ),
            'no_results_title': _(
                'There are no fields for this workflow transition'
            ),
            'object': self.external_object,
            'title': _(
                'Fields for workflow transition: %s'
            ) % self.external_object,
            'workflow': self.external_object.workflow,
        }

    def get_source_queryset(self):
        return self.external_object.fields.all()
