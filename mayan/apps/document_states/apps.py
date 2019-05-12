from __future__ import unicode_literals

from django.apps import apps
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.classes import ModelAttribute
from mayan.apps.common.links import link_object_error_list
from mayan.apps.common.html_widgets import TwoStateWidget
from mayan.apps.common.menus import (
    menu_facet, menu_list_facet, menu_main, menu_object, menu_secondary,
    menu_setup, menu_tools
)
from mayan.apps.common.permissions_runtime import permission_error_log_view
from mayan.apps.events.classes import ModelEventType
from mayan.apps.events.links import (
    link_events_for_object, link_object_event_types_user_subcriptions_list
)
from mayan.apps.navigation.classes import SourceColumn

from .classes import DocumentStateHelper, WorkflowAction
from .events import event_workflow_created, event_workflow_edited
from .dependencies import *  # NOQA
from .handlers import (
    handler_index_document, handler_launch_workflow, handler_trigger_transition
)
from .links import (
    link_document_workflow_instance_list, link_setup_document_type_workflows,
    link_setup_workflow_document_types, link_setup_workflow_create,
    link_setup_workflow_delete, link_setup_workflow_edit,
    link_setup_workflow_list, link_setup_workflow_states,
    link_setup_workflow_state_action_delete,
    link_setup_workflow_state_action_edit,
    link_setup_workflow_state_action_list,
    link_setup_workflow_state_action_selection,
    link_setup_workflow_state_create, link_setup_workflow_state_delete,
    link_setup_workflow_state_edit, link_setup_workflow_transitions,
    link_setup_workflow_transition_create,
    link_setup_workflow_transition_delete, link_setup_workflow_transition_edit,
    link_tool_launch_all_workflows, link_workflow_instance_detail,
    link_workflow_instance_transition, link_workflow_runtime_proxy_document_list,
    link_workflow_runtime_proxy_list, link_workflow_preview,
    link_workflow_runtime_proxy_state_document_list, link_workflow_runtime_proxy_state_list,
    link_workflow_transition_events
)
from .permissions import (
    permission_workflow_delete, permission_workflow_edit,
    permission_workflow_transition, permission_workflow_view
)
from .widgets import widget_transition_events


class DocumentStatesApp(MayanAppConfig):
    app_namespace = 'document_states'
    app_url = 'workflows'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.document_states'
    verbose_name = _('Workflows')

    def ready(self):
        super(DocumentStatesApp, self).ready()
        from actstream import registry

        Action = apps.get_model(
            app_label='actstream', model_name='Action'
        )
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        DocumentType = apps.get_model(
            app_label='documents', model_name='DocumentType'
        )
        ErrorLogEntry = apps.get_model(
            app_label='common', model_name='ErrorLogEntry'
        )

        Workflow = self.get_model('Workflow')
        WorkflowInstance = self.get_model('WorkflowInstance')
        WorkflowInstanceLogEntry = self.get_model('WorkflowInstanceLogEntry')
        WorkflowRuntimeProxy = self.get_model('WorkflowRuntimeProxy')
        WorkflowState = self.get_model('WorkflowState')
        WorkflowStateAction = self.get_model('WorkflowStateAction')
        WorkflowStateRuntimeProxy = self.get_model('WorkflowStateRuntimeProxy')
        WorkflowTransition = self.get_model('WorkflowTransition')
        WorkflowTransitionTriggerEvent = self.get_model(
            'WorkflowTransitionTriggerEvent'
        )

        Document.add_to_class(
            name='workflow', value=DocumentStateHelper.constructor
        )

        ErrorLogEntry.objects.register(model=WorkflowStateAction)

        WorkflowAction.initialize()

        ModelAttribute(
            model=Document,
            name='workflow.< workflow internal name >.get_current_state',
            label=_('Current state of a workflow'), description=_(
                'Return the current state of the selected workflow'
            )
        )
        ModelAttribute(
            model=Document,
            name='workflow.< workflow internal name >.get_current_state.completion',
            label=_('Current state of a workflow'), description=_(
                'Return the completion value of the current state of the '
                'selected workflow'
            )
        )

        ModelEventType.register(
            event_types=(
                event_workflow_created, event_workflow_edited
            ), model=Workflow
        )

        ModelPermission.register(
            model=Document, permissions=(permission_workflow_view,)
        )
        ModelPermission.register(
            model=Workflow, permissions=(
                permission_error_log_view, permission_workflow_delete,
                permission_workflow_edit, permission_workflow_transition,
                permission_workflow_view,
            )
        )

        ModelPermission.register_inheritance(
            model=WorkflowInstance, related='workflow',
        )
        ModelPermission.register_inheritance(
            model=WorkflowInstanceLogEntry,
            related='workflow_instance__workflow',
        )
        ModelPermission.register(
            model=WorkflowTransition,
            permissions=(permission_workflow_transition,)
        )

        ModelPermission.register_inheritance(
            model=WorkflowState, related='workflow',
        )
        ModelPermission.register_inheritance(
            model=WorkflowStateAction, related='state__workflow',
        )
        ModelPermission.register_inheritance(
            model=WorkflowTransition, related='workflow',
        )
        ModelPermission.register_inheritance(
            model=WorkflowTransitionTriggerEvent,
            related='transition__workflow',
        )

        SourceColumn(
            attribute='label', is_sortable=True, source=Workflow
        )
        SourceColumn(
            attribute='internal_name', is_sortable=True, source=Workflow
        )
        SourceColumn(
            attribute='get_initial_state', empty_value=_('None'),
            source=Workflow
        )

        SourceColumn(
            source=WorkflowInstance, label=_('Current state'),
            attribute='get_current_state'
        )
        SourceColumn(
            source=WorkflowInstance, label=_('User'),
            func=lambda context: getattr(
                context['object'].get_last_log_entry(), 'user', _('None')
            )
        )
        SourceColumn(
            source=WorkflowInstance, label=_('Last transition'),
            attribute='get_last_transition'
        )
        SourceColumn(
            source=WorkflowInstance, label=_('Date and time'),
            func=lambda context: getattr(
                context['object'].get_last_log_entry(), 'datetime', _('None')
            )
        )
        SourceColumn(
            source=WorkflowInstance, label=_('Completion'),
            func=lambda context: getattr(
                context['object'].get_current_state(), 'completion', _('None')
            )
        )

        SourceColumn(
            source=WorkflowInstanceLogEntry, label=_('Date and time'),
            attribute='datetime'
        )
        SourceColumn(
            source=WorkflowInstanceLogEntry, label=_('User'), attribute='user'
        )
        SourceColumn(
            source=WorkflowInstanceLogEntry, label=_('Transition'),
            attribute='transition'
        )
        SourceColumn(
            source=WorkflowInstanceLogEntry, label=_('Comment'),
            attribute='comment'
        )

        SourceColumn(
            attribute='label', is_sortable=True, source=WorkflowState
        )
        SourceColumn(
            attribute='initial', is_sortable=True, source=WorkflowState,
            widget=TwoStateWidget
        )
        SourceColumn(
            attribute='completion', source=WorkflowState, is_sortable=True,
        )

        SourceColumn(
            attribute='label', is_sortable=True, source=WorkflowStateAction
        )
        SourceColumn(
            attribute='enabled', is_sortable=True, source=WorkflowStateAction,
            widget=TwoStateWidget
        )
        SourceColumn(
            attribute='get_when_display', label=_('When?'),
            source=WorkflowStateAction
        )
        SourceColumn(
            attribute='get_class_label', label=_('Action type'),
            source=WorkflowStateAction
        )

        SourceColumn(
            attribute='label', is_sortable=True, source=WorkflowTransition,
        )
        SourceColumn(
            attribute='origin_state', is_sortable=True,
            source=WorkflowTransition
        )
        SourceColumn(
            attribute='destination_state', is_sortable=True,
            source=WorkflowTransition
        )
        SourceColumn(
            source=WorkflowTransition, label=_('Triggers'),
            func=lambda context: widget_transition_events(
                transition=context['object']
            )
        )

        menu_facet.bind_links(
            links=(link_document_workflow_instance_list,), sources=(Document,)
        )

        menu_list_facet.bind_links(
            links=(
                link_acl_list, link_events_for_object,
                link_object_event_types_user_subcriptions_list,
                link_setup_workflow_document_types,
                link_setup_workflow_states, link_setup_workflow_transitions,
                link_workflow_preview
            ), sources=(Workflow,)
        )
        menu_list_facet.bind_links(
            links=(
                link_setup_document_type_workflows,
            ), sources=(DocumentType,)
        )

        menu_main.bind_links(links=(link_workflow_runtime_proxy_list,), position=10)
        menu_object.bind_links(
            links=(
                link_setup_workflow_delete, link_setup_workflow_edit
            ), sources=(Workflow,)
        )
        menu_object.bind_links(
            links=(
                link_setup_workflow_state_edit,
                link_setup_workflow_state_action_list,
                link_setup_workflow_state_delete
            ), sources=(WorkflowState,)
        )
        menu_object.bind_links(
            links=(
                link_setup_workflow_transition_edit,
                link_workflow_transition_events, link_acl_list,
                link_setup_workflow_transition_delete
            ), sources=(WorkflowTransition,)
        )
        menu_object.bind_links(
            links=(
                link_workflow_instance_detail,
                link_workflow_instance_transition
            ), sources=(WorkflowInstance,)
        )

        menu_list_facet.bind_links(
            links=(
                link_workflow_runtime_proxy_document_list,
                link_workflow_runtime_proxy_state_list,
            ), sources=(WorkflowRuntimeProxy,)
        )
        menu_list_facet.bind_links(
            links=(
                link_workflow_runtime_proxy_state_document_list,
            ), sources=(WorkflowStateRuntimeProxy,)
        )
        menu_object.bind_links(
            links=(
                link_setup_workflow_state_action_edit,
                link_object_error_list,
                link_setup_workflow_state_action_delete,
            ), sources=(WorkflowStateAction,)
        )

        menu_secondary.bind_links(
            links=(link_setup_workflow_list, link_setup_workflow_create),
            sources=(
                Workflow, 'document_states:setup_workflow_create',
                'document_states:setup_workflow_list'
            )
        )
        menu_secondary.bind_links(
            links=(link_workflow_runtime_proxy_list,),
            sources=(
                WorkflowRuntimeProxy,
            )
        )
        menu_secondary.bind_links(
            links=(link_setup_workflow_state_action_selection,),
            sources=(
                WorkflowState,
            )
        )
        menu_secondary.bind_links(
            links=(
                link_setup_workflow_transition_create,
            ), sources=(
                WorkflowTransition,
                'document_states:setup_workflow_transition_list',
            )
        )
        menu_secondary.bind_links(
            links=(
                link_setup_workflow_state_create,
            ), sources=(
                WorkflowState,
                'document_states:setup_workflow_state_list',
            )
        )

        menu_setup.bind_links(links=(link_setup_workflow_list,))

        menu_tools.bind_links(links=(link_tool_launch_all_workflows,))

        post_save.connect(
            dispatch_uid='workflows_handler_launch_workflow',
            receiver=handler_launch_workflow,
            sender=Document
        )

        # Index updating

        post_save.connect(
            dispatch_uid='workflows_handler_index_document_save',
            receiver=handler_index_document,
            sender=WorkflowInstanceLogEntry
        )
        post_save.connect(
            dispatch_uid='workflows_handler_trigger_transition',
            receiver=handler_trigger_transition,
            sender=Action
        )

        registry.register(Workflow)
