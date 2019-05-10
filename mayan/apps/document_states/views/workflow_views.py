from __future__ import absolute_import, unicode_literals

from django.contrib import messages
from django.core.files.base import ContentFile
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
    SingleObjectDownloadView, SingleObjectEditView, SingleObjectListView
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
    icon_workflow_list, icon_workflow_state, icon_workflow_state_action,
    icon_workflow_transition
)
from ..links import (
    link_setup_workflow_create, link_setup_workflow_state_create,
    link_setup_workflow_state_action_selection,
    link_setup_workflow_transition_create
)
from ..models import (
    Workflow, WorkflowState, WorkflowStateAction, WorkflowTransition
)
from ..permissions import (
    permission_workflow_create, permission_workflow_delete,
    permission_workflow_edit, permission_workflow_tools,
    permission_workflow_view,
)
from ..tasks import task_launch_all_workflows

__all__ = (
    'WorkflowImageView', 'WorkflowPreviewView',
    'SetupWorkflowListView', 'SetupWorkflowCreateView', 'SetupWorkflowEditView',
    'SetupWorkflowDeleteView', 'SetupWorkflowDocumentTypesView',
    'SetupWorkflowStateActionCreateView', 'SetupWorkflowStateActionDeleteView',
    'SetupWorkflowStateActionEditView', 'SetupWorkflowStateActionListView',
    'SetupWorkflowStateActionSelectionView', 'SetupWorkflowStateCreateView',
    'SetupWorkflowStateDeleteView', 'SetupWorkflowStateEditView',
    'SetupWorkflowStateListView', 'SetupWorkflowTransitionCreateView',
    'SetupWorkflowTransitionDeleteView', 'SetupWorkflowTransitionEditView',
    'SetupWorkflowTransitionListView',
    'SetupWorkflowTransitionTriggerEventListView', 'ToolLaunchAllWorkflows'
)


class SetupDocumentTypeWorkflowsView(AddRemoveView):
    main_object_permission = permission_document_type_edit
    main_object_model = DocumentType
    main_object_pk_url_kwarg = 'pk'
    secondary_object_model = Workflow
    secondary_object_permission = permission_workflow_edit
    list_available_title = _('Available workflows')
    list_added_title = _('Workflows assigned this document type')
    related_field = 'workflows'

    def get_actions_extra_kwargs(self):
        return {'_user': self.request.user}

    def get_extra_context(self):
        return {
            'object': self.main_object,
            'subtitle': _(
                'Removing a workflow from a document type will also '
                'remove all running instances of that workflow.'
            ),
            'title': _(
                'Workflows assigned the document type: %s'
            ) % self.main_object,
        }

    def action_add(self, queryset, _user):
        with transaction.atomic():
            event_document_type_edited.commit(
                actor=_user, target=self.main_object
            )

            for obj in queryset:
                self.main_object.workflows.add(obj)
                event_workflow_edited.commit(
                    action_object=self.main_object, actor=_user, target=obj
                )

    def action_remove(self, queryset, _user):
        with transaction.atomic():
            event_document_type_edited.commit(
                actor=_user, target=self.main_object
            )

            for obj in queryset:
                self.main_object.workflows.remove(obj)
                event_workflow_edited.commit(
                    action_object=self.main_object, actor=_user,
                    target=obj
                )
                obj.instances.filter(
                    document__document_type=self.main_object
                ).delete()


class SetupWorkflowListView(SingleObjectListView):
    model = Workflow
    object_permission = permission_workflow_view

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_workflow_list,
            'no_results_main_link': link_setup_workflow_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Workflows store a series of states and keep track of the '
                'current state of a document. Transitions are used to change the '
                'current state to a new one.'
            ),
            'no_results_title': _(
                'No workflows have been defined'
            ),
            'title': _('Workflows'),
        }


class SetupWorkflowCreateView(SingleObjectCreateView):
    extra_context = {'title': _('Create workflow')}
    form_class = WorkflowForm
    model = Workflow
    post_action_redirect = reverse_lazy(
        viewname='document_states:setup_workflow_list'
    )
    view_permission = permission_workflow_create

    def get_save_extra_data(self):
        return {'_user': self.request.user}


class SetupWorkflowDeleteView(SingleObjectDeleteView):
    model = Workflow
    object_permission = permission_workflow_delete
    post_action_redirect = reverse_lazy(
        viewname='document_states:setup_workflow_list'
    )


class SetupWorkflowEditView(SingleObjectEditView):
    form_class = WorkflowForm
    model = Workflow
    object_permission = permission_workflow_edit
    post_action_redirect = reverse_lazy(
        viewname='document_states:setup_workflow_list'
    )

    def get_save_extra_data(self):
        return {'_user': self.request.user}


class SetupWorkflowDocumentTypesView(AddRemoveView):
    main_object_permission = permission_workflow_edit
    main_object_model = Workflow
    main_object_pk_url_kwarg = 'pk'
    secondary_object_model = DocumentType
    secondary_object_permission = permission_document_type_edit
    list_available_title = _('Available document types')
    list_added_title = _('Document types assigned this workflow')
    related_field = 'document_types'

    def get_actions_extra_kwargs(self):
        return {'_user': self.request.user}

    def get_extra_context(self):
        return {
            'object': self.main_object,
            'subtitle': _(
                'Removing a document type from a workflow will also '
                'remove all running instances of that workflow for '
                'documents of the document type just removed.'
            ),
            'title': _(
                'Document types assigned the workflow: %s'
            ) % self.main_object,
        }

    def action_add(self, queryset, _user):
        with transaction.atomic():
            event_workflow_edited.commit(
                actor=_user, target=self.main_object
            )

            for obj in queryset:
                self.main_object.document_types.add(obj)
                event_document_type_edited.commit(
                    action_object=self.main_object, actor=_user, target=obj
                )

    def action_remove(self, queryset, _user):
        with transaction.atomic():
            event_workflow_edited.commit(
                actor=_user, target=self.main_object
            )

            for obj in queryset:
                self.main_object.document_types.remove(obj)
                event_document_type_edited.commit(
                    action_object=self.main_object, actor=_user,
                    target=obj
                )
                self.main_object.instances.filter(
                    document__document_type=obj
                ).delete()


# Workflow state actions


class SetupWorkflowStateActionCreateView(SingleObjectDynamicFormCreateView):
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
            viewname='document_states:setup_workflow_state_action_list',
            kwargs={'pk': self.get_object().pk}
        )


class SetupWorkflowStateActionDeleteView(SingleObjectDeleteView):
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
            viewname='document_states:setup_workflow_state_action_list',
            kwargs={'pk': self.get_object().state.pk}
        )


class SetupWorkflowStateActionEditView(SingleObjectDynamicFormEditView):
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
            viewname='document_states:setup_workflow_state_action_list',
            kwargs={'pk': self.get_object().state.pk}
        )


class SetupWorkflowStateActionListView(SingleObjectListView):
    object_permission = permission_workflow_edit

    def get_extra_context(self):
        return {
            'hide_object': True,
            'navigation_object_list': ('object', 'workflow'),
            'no_results_icon': icon_workflow_state_action,
            'no_results_main_link': link_setup_workflow_state_action_selection.resolve(
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


class SetupWorkflowStateActionSelectionView(FormView):
    form_class = WorkflowActionSelectionForm
    view_permission = permission_workflow_edit

    def form_valid(self, form):
        klass = form.cleaned_data['klass']
        return HttpResponseRedirect(
            redirect_to=reverse(
                viewname='document_states:setup_workflow_state_action_create',
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


# Workflow states


class SetupWorkflowStateCreateView(ExternalObjectMixin, SingleObjectCreateView):
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
            viewname='document_states:setup_workflow_state_list',
            kwargs={'pk': self.kwargs['pk']}
        )

    def get_workflow(self):
        return self.external_object


class SetupWorkflowStateDeleteView(SingleObjectDeleteView):
    model = WorkflowState
    object_permission = permission_workflow_edit
    pk_url_kwarg = 'pk'

    def get_extra_context(self):
        return {
            'navigation_object_list': ('object', 'workflow_instance'),
            'object': self.get_object(),
            'workflow_instance': self.get_object().workflow,
        }

    def get_success_url(self):
        return reverse(
            viewname='document_states:setup_workflow_state_list',
            kwargs={'pk': self.get_object().workflow.pk}
        )


class SetupWorkflowStateEditView(SingleObjectEditView):
    form_class = WorkflowStateForm
    model = WorkflowState
    object_permission = permission_workflow_edit
    pk_url_kwarg = 'pk'

    def get_extra_context(self):
        return {
            'navigation_object_list': ('object', 'workflow_instance'),
            'object': self.get_object(),
            'workflow_instance': self.get_object().workflow,
        }

    def get_success_url(self):
        return reverse(
            viewname='document_states:setup_workflow_state_list',
            kwargs={'pk': self.get_object().workflow.pk}
        )


class SetupWorkflowStateListView(ExternalObjectMixin, SingleObjectListView):
    external_object_class = Workflow
    external_object_permission = permission_workflow_view
    external_object_pk_url_kwarg = 'pk'
    object_permission = permission_workflow_view

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_workflow_state,
            'no_results_main_link': link_setup_workflow_state_create.resolve(
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


# Transitions


class SetupWorkflowTransitionCreateView(ExternalObjectMixin, SingleObjectCreateView):
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
            SetupWorkflowTransitionCreateView, self
        ).get_form_kwargs()
        kwargs['workflow'] = self.get_workflow()
        return kwargs

    def get_instance_extra_data(self):
        return {'workflow': self.get_workflow()}

    def get_source_queryset(self):
        return self.get_workflow().transitions.all()

    def get_success_url(self):
        return reverse(
            viewname='document_states:setup_workflow_transition_list',
            kwargs={'pk': self.kwargs['pk']}
        )

    def get_workflow(self):
        return self.external_object


class SetupWorkflowTransitionDeleteView(SingleObjectDeleteView):
    model = WorkflowTransition
    object_permission = permission_workflow_edit
    pk_url_kwarg = 'pk'

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'navigation_object_list': ('object', 'workflow_instance'),
            'workflow_instance': self.get_object().workflow,
        }

    def get_success_url(self):
        return reverse(
            viewname='document_states:setup_workflow_transition_list',
            kwargs={'pk': self.get_object().workflow.pk}
        )


class SetupWorkflowTransitionEditView(SingleObjectEditView):
    form_class = WorkflowTransitionForm
    model = WorkflowTransition
    object_permission = permission_workflow_edit
    pk_url_kwarg = 'pk'

    def get_extra_context(self):
        return {
            'navigation_object_list': ('object', 'workflow_instance'),
            'object': self.get_object(),
            'workflow_instance': self.get_object().workflow,
        }

    def get_form_kwargs(self):
        kwargs = super(
            SetupWorkflowTransitionEditView, self
        ).get_form_kwargs()
        kwargs['workflow'] = self.get_object().workflow
        return kwargs

    def get_success_url(self):
        return reverse(
            viewname='document_states:setup_workflow_transition_list',
            kwargs={'pk': self.get_object().workflow.pk}
        )


class SetupWorkflowTransitionListView(ExternalObjectMixin, SingleObjectListView):
    external_object_class = Workflow
    external_object_permission = permission_workflow_view
    external_object_pk_url_kwarg = 'pk'
    object_permission = permission_workflow_view

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_workflow_transition,
            'no_results_main_link': link_setup_workflow_transition_create.resolve(
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


class SetupWorkflowTransitionTriggerEventListView(ExternalObjectMixin, FormView):
    external_object_class = WorkflowTransition
    external_object_permission = permission_workflow_edit
    external_object_pk_url_kwarg = 'pk'
    form_class = WorkflowTransitionTriggerEventRelationshipFormSet

    def dispatch(self, *args, **kwargs):
        EventType.refresh()
        return super(
            SetupWorkflowTransitionTriggerEventListView, self
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
            SetupWorkflowTransitionTriggerEventListView, self
        ).form_valid(form=form)

    def get_object(self):
        return self.external_object

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

        for event_type in event_type_queryset:
            initial.append({
                'transition': obj,
                'event_type': event_type,
            })
        return initial

    def get_post_action_redirect(self):
        return reverse(
            viewname='document_states:setup_workflow_transition_list',
            kwargs={'pk': self.get_object().workflow.pk}
        )


class ToolLaunchAllWorkflows(ConfirmView):
    extra_context = {
        'title': _('Launch all workflows?'),
        'subtitle': _(
            'This will launch all workflows created after documents have '
            'already been uploaded.'
        )
    }
    view_permission = permission_workflow_tools

    def view_action(self):
        task_launch_all_workflows.apply_async()
        messages.success(
            message=_('Workflow launch queued successfully.'),
            request=self.request
        )


class WorkflowImageView(SingleObjectDownloadView):
    attachment = False
    model = Workflow
    object_permission = permission_workflow_view

    def get_file(self):
        workflow = self.get_object()
        return ContentFile(workflow.render(), name=workflow.label)

    def get_mimetype(self):
        return 'image'


class WorkflowPreviewView(SingleObjectDetailView):
    form_class = WorkflowPreviewForm
    model = Workflow
    object_permission = permission_workflow_view

    def get_extra_context(self):
        return {
            'hide_labels': True,
            'title': _('Preview of: %s') % self.get_object()
        }
