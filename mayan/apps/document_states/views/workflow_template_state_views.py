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


class WorkflowTemplateStateActionCreateView(SingleObjectDynamicFormCreateView):
    form_class = WorkflowStateActionDynamicForm
    object_permission = permission_workflow_edit

    def get_class(self):
        try:
            return WorkflowAction.get(name=self.kwargs['class_path'])
        except KeyError:
            raise Http404(
                '{} class not found'.format(self.kwargs['class_path'])
            )

    def get_extra_context(self):
        return {
            'navigation_object_list': ('object', 'workflow'),
            'object': self.get_object(),
            'title': _(
                'Create a "%s" workflow action'
            ) % self.get_class().label,
            'workflow': self.get_object().workflow
        }

    def get_form_extra_kwargs(self):
        return {
            'request': self.request,
            'action_path': self.kwargs['class_path']
        }

    def get_form_schema(self):
        return self.get_class()().get_form_schema(request=self.request)

    def get_instance_extra_data(self):
        return {
            'action_path': self.kwargs['class_path'],
            'state': self.get_object()
        }

    def get_object(self):
        return get_object_or_404(klass=WorkflowState, pk=self.kwargs['pk'])

    def get_post_action_redirect(self):
        return reverse(
            viewname='document_states:workflow_template_state_action_list',
            kwargs={'pk': self.get_object().pk}
        )


class WorkflowTemplateStateActionDeleteView(SingleObjectDeleteView):
    model = WorkflowStateAction
    object_permission = permission_workflow_edit

    def get_extra_context(self):
        return {
            'navigation_object_list': (
                'object', 'workflow_state', 'workflow'
            ),
            'object': self.get_object(),
            'title': _('Delete workflow state action: %s') % self.get_object(),
            'workflow': self.get_object().state.workflow,
            'workflow_state': self.get_object().state,
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='document_states:workflow_template_state_action_list',
            kwargs={'pk': self.get_object().state.pk}
        )


class WorkflowTemplateStateActionEditView(SingleObjectDynamicFormEditView):
    form_class = WorkflowStateActionDynamicForm
    model = WorkflowStateAction
    object_permission = permission_workflow_edit

    def get_extra_context(self):
        return {
            'navigation_object_list': (
                'object', 'workflow_state', 'workflow'
            ),
            'object': self.get_object(),
            'title': _('Edit workflow state action: %s') % self.get_object(),
            'workflow': self.get_object().state.workflow,
            'workflow_state': self.get_object().state,
        }

    def get_form_extra_kwargs(self):
        return {
            'request': self.request,
            'action_path': self.get_object().action_path,
        }

    def get_form_schema(self):
        return self.get_object().get_class_instance().get_form_schema(
            request=self.request
        )

    def get_post_action_redirect(self):
        return reverse(
            viewname='document_states:workflow_template_state_action_list',
            kwargs={'pk': self.get_object().state.pk}
        )


class WorkflowTemplateStateActionListView(SingleObjectListView):
    object_permission = permission_workflow_edit

    def get_extra_context(self):
        return {
            'hide_object': True,
            'navigation_object_list': ('object', 'workflow'),
            'no_results_icon': icon_workflow_state_action,
            'no_results_main_link': link_workflow_template_state_action_selection.resolve(
                context=RequestContext(
                    request=self.request, dict_={
                        'object': self.get_workflow_state()
                    }
                )
            ),
            'no_results_text': _(
                'Workflow state actions are macros that get executed when '
                'documents enters or leaves the state in which they reside.'
            ),
            'no_results_title': _(
                'There are no actions for this workflow state'
            ),
            'object': self.get_workflow_state(),
            'title': _(
                'Actions for workflow state: %s'
            ) % self.get_workflow_state(),
            'workflow': self.get_workflow_state().workflow,
        }

    def get_form_schema(self):
        return {'fields': self.get_class().fields}

    def get_source_queryset(self):
        return self.get_workflow_state().actions.all()

    def get_workflow_state(self):
        return get_object_or_404(klass=WorkflowState, pk=self.kwargs['pk'])


class WorkflowTemplateStateActionSelectionView(FormView):
    form_class = WorkflowActionSelectionForm
    view_permission = permission_workflow_edit

    def form_valid(self, form):
        klass = form.cleaned_data['klass']
        return HttpResponseRedirect(
            redirect_to=reverse(
                viewname='document_states:workflow_template_state_action_create',
                kwargs={'pk': self.get_object().pk, 'class_path': klass}
            )
        )

    def get_extra_context(self):
        return {
            'navigation_object_list': (
                'object', 'workflow'
            ),
            'object': self.get_object(),
            'title': _('New workflow state action selection'),
            'workflow': self.get_object().workflow,
        }

    def get_object(self):
        return get_object_or_404(klass=WorkflowState, pk=self.kwargs['pk'])


class WorkflowTemplateStateCreateView(ExternalObjectMixin, SingleObjectCreateView):
    external_object_class = Workflow
    external_object_permission = permission_workflow_edit
    external_object_pk_url_kwarg = 'pk'
    form_class = WorkflowStateForm

    def get_extra_context(self):
        return {
            'object': self.get_workflow(),
            'title': _(
                'Create states for workflow: %s'
            ) % self.get_workflow()
        }

    def get_instance_extra_data(self):
        return {'workflow': self.get_workflow()}

    def get_source_queryset(self):
        return self.get_workflow().states.all()

    def get_success_url(self):
        return reverse(
            viewname='document_states:workflow_template_state_list',
            kwargs={'pk': self.kwargs['pk']}
        )

    def get_workflow(self):
        return self.external_object


class WorkflowTemplateStateDeleteView(SingleObjectDeleteView):
    model = WorkflowState
    object_permission = permission_workflow_edit
    pk_url_kwarg = 'pk'

    def get_extra_context(self):
        return {
            'navigation_object_list': ('object', 'workflow_instance'),
            'object': self.get_object(),
            'title': _(
                'Delete workflow state: %s?'
            ) % self.object,
            'workflow_instance': self.get_object().workflow,
        }

    def get_success_url(self):
        return reverse(
            viewname='document_states:workflow_template_state_list',
            kwargs={'pk': self.get_object().workflow.pk}
        )


class WorkflowTemplateStateEditView(SingleObjectEditView):
    form_class = WorkflowStateForm
    model = WorkflowState
    object_permission = permission_workflow_edit
    pk_url_kwarg = 'pk'

    def get_extra_context(self):
        return {
            'navigation_object_list': ('object', 'workflow_instance'),
            'object': self.get_object(),
            'title': _(
                'Edit workflow state: %s'
            ) % self.object,
            'workflow_instance': self.get_object().workflow,
        }

    def get_success_url(self):
        return reverse(
            viewname='document_states:workflow_template_state_list',
            kwargs={'pk': self.get_object().workflow.pk}
        )


class WorkflowTemplateStateListView(ExternalObjectMixin, SingleObjectListView):
    external_object_class = Workflow
    external_object_permission = permission_workflow_view
    external_object_pk_url_kwarg = 'pk'
    object_permission = permission_workflow_view

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_workflow_state,
            'no_results_main_link': link_workflow_template_state_create.resolve(
                context=RequestContext(
                    self.request, {'object': self.get_workflow()}
                )
            ),
            'no_results_text': _(
                'Create states and link them using transitions.'
            ),
            'no_results_title': _(
                'This workflow doesn\'t have any states'
            ),
            'object': self.get_workflow(),
            'title': _('States of workflow: %s') % self.get_workflow()
        }

    def get_source_queryset(self):
        return self.get_workflow().states.all()

    def get_workflow(self):
        return self.external_object
