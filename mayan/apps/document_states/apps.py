from django.apps import apps
from django.db.models.signals import post_migrate, post_save
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.classes import (
    ModelCopy, ModelField, ModelProperty, ModelReverseField
)
from mayan.apps.common.menus import (
    menu_facet, menu_list_facet, menu_main, menu_multi_item, menu_object,
    menu_related, menu_secondary, menu_setup, menu_tools
)
from mayan.apps.documents.links.document_type_links import link_document_type_list
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.logging.classes import ErrorLog
from mayan.apps.logging.permissions import permission_error_log_view
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.views.html_widgets import TwoStateWidget

from .classes import DocumentStateHelper, WorkflowAction
from .events import event_workflow_template_edited
from .handlers import (
    handler_create_workflow_image_cache, handler_index_document,
    handler_launch_workflow, handler_trigger_transition
)
from .html_widgets import WorkflowLogExtraDataWidget, widget_transition_events
from .links import (
    link_document_multiple_workflow_templates_launch,
    link_document_single_workflow_templates_launch,
    link_tool_launch_workflows, link_workflow_instance_list,
    link_workflow_instance_detail, link_workflow_instance_transition,
    link_workflow_runtime_proxy_document_list,
    link_workflow_runtime_proxy_list, link_workflow_template_preview,
    link_workflow_runtime_proxy_state_document_list,
    link_workflow_runtime_proxy_state_list,
    link_document_type_workflow_templates, link_workflow_template_create,
    link_workflow_template_document_types, link_workflow_template_edit,
    link_workflow_template_multiple_delete, link_workflow_template_launch,
    link_workflow_template_list, link_workflow_template_single_delete,
    link_workflow_template_state_list,
    link_workflow_template_state_action_delete,
    link_workflow_template_state_action_edit,
    link_workflow_template_state_action_list,
    link_workflow_template_state_action_selection,
    link_workflow_template_state_create, link_workflow_template_state_delete,
    link_workflow_template_state_edit,
    link_workflow_template_transition_create,
    link_workflow_template_transition_delete,
    link_workflow_template_transition_edit,
    link_workflow_template_transition_list,
    link_workflow_template_transition_events,
    link_workflow_template_transition_field_create,
    link_workflow_template_transition_field_delete,
    link_workflow_template_transition_field_edit,
    link_workflow_template_transition_field_list
)
from .permissions import (
    permission_workflow_template_delete, permission_workflow_template_edit,
    permission_workflow_tools, permission_workflow_instance_transition,
    permission_workflow_template_view
)


class DocumentStatesApp(MayanAppConfig):
    app_namespace = 'document_states'
    app_url = 'workflows'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.document_states'
    verbose_name = _('Workflows')

    def ready(self):
        super().ready()

        Action = apps.get_model(
            app_label='actstream', model_name='Action'
        )
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        DocumentType = apps.get_model(
            app_label='documents', model_name='DocumentType'
        )

        Workflow = self.get_model('Workflow')
        WorkflowInstance = self.get_model('WorkflowInstance')
        WorkflowInstanceLogEntry = self.get_model('WorkflowInstanceLogEntry')
        WorkflowRuntimeProxy = self.get_model('WorkflowRuntimeProxy')
        WorkflowState = self.get_model('WorkflowState')
        WorkflowStateAction = self.get_model('WorkflowStateAction')
        WorkflowStateRuntimeProxy = self.get_model('WorkflowStateRuntimeProxy')
        WorkflowTransition = self.get_model('WorkflowTransition')
        WorkflowTransitionField = self.get_model('WorkflowTransitionField')
        WorkflowTransitionTriggerEvent = self.get_model(
            'WorkflowTransitionTriggerEvent'
        )

        Document.add_to_class(
            name='workflow', value=DocumentStateHelper.constructor
        )

        error_log = ErrorLog(app_config=self)
        error_log.register_model(model=WorkflowStateAction)

        EventModelRegistry.register(model=Workflow)
        EventModelRegistry.register(model=WorkflowState)
        EventModelRegistry.register(model=WorkflowStateAction)
        EventModelRegistry.register(model=WorkflowTransition)
        EventModelRegistry.register(model=WorkflowTransitionField)

        WorkflowAction.load_modules()

        ModelCopy(model=WorkflowState).add_fields(
            field_names=(
                'actions', 'workflow', 'label', 'initial', 'completion'
            )
        )
        ModelCopy(model=WorkflowStateAction).add_fields(
            field_names=(
                'state', 'label', 'enabled', 'when', 'action_path',
                'action_data', 'condition'
            )
        )
        ModelCopy(model=WorkflowTransition).add_fields(
            field_names=(
                'workflow', 'label', 'origin_state', 'destination_state',
                'condition', 'fields', 'trigger_events'
            ),
            field_value_gets={
                'origin_state': {
                    'workflow': '{workflow.pk}',
                    'label': '{instance.origin_state.label}'
                },
                'destination_state': {
                    'workflow': '{workflow.pk}',
                    'label': '{instance.destination_state.label}'
                },
            }
        )
        ModelCopy(
            model=WorkflowTransitionTriggerEvent
        ).add_fields(
            field_names=('transition', 'event_type')
        )
        ModelCopy(
            model=WorkflowTransitionField
        ).add_fields(
            field_names=(
                'transition', 'field_type', 'name', 'label', 'help_text',
                'required', 'widget', 'widget_kwargs',
            )
        )
        ModelCopy(
            model=Workflow, bind_link=True, register_permission=True
        ).add_fields(
            field_names=(
                'auto_launch', 'internal_name', 'label', 'document_types',
                'states', 'transitions'
            ),
        )

        ModelEventType.register(
            event_types=(event_workflow_template_edited,), model=Workflow
        )

        ModelProperty(
            model=Document,
            name='workflow.< workflow internal name >.get_current_state',
            label=_('Current state of a workflow'), description=_(
                'Return the current state of the selected workflow.'
            )
        )
        ModelProperty(
            model=Document,
            name='workflow.< workflow internal name >.get_current_state.completion',
            label=_('Current state of a workflow'), description=_(
                'Return the completion value of the current state of the '
                'selected workflow.'
            )
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_workflow_instance_transition,
                permission_workflow_template_view,
                permission_workflow_tools
            )
        )
        ModelPermission.register(
            model=Workflow, permissions=(
                permission_error_log_view, permission_workflow_template_delete,
                permission_workflow_template_edit, permission_workflow_tools,
                permission_workflow_instance_transition,
                permission_workflow_template_view
            )
        )
        ModelPermission.register(
            model=WorkflowTransition,
            permissions=(permission_workflow_instance_transition,)
        )

        ModelPermission.register_inheritance(
            model=WorkflowInstance, related='workflow',
        )
        ModelPermission.register_inheritance(
            model=WorkflowInstanceLogEntry,
            related='workflow_instance__workflow',
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
            model=WorkflowTransitionField, related='transition',
        )
        ModelPermission.register_inheritance(
            model=WorkflowTransitionTriggerEvent,
            related='transition__workflow',
        )

        ModelField(model=WorkflowInstance, name='document')
        ModelField(model=WorkflowInstance, name='workflow')
        ModelReverseField(model=WorkflowInstance, name='log_entries')

        ModelProperty(
            description=_(
                'Return the last workflow instance log entry. The '
                'log entry itself has the following fields: datetime, '
                'transition, user, and comment.'
            ), label=_('Get last log entry'), model=WorkflowInstance,
            name='get_last_log_entry'
        )

        ModelProperty(
            description=_(
                'Return the current context dictionary which includes '
                'runtime data from the workflow transition fields.'
            ), label=_('Get the context'), model=WorkflowInstance,
            name='get_runtime_context'
        )

        ModelProperty(
            description=_(
                'Return the transition of the workflow instance.'
            ), label=_('Get last transition'), model=WorkflowInstance,
            name='get_last_transition'
        )

        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=Workflow
        )
        column_workflow_internal_name = SourceColumn(
            attribute='internal_name', include_label=True, is_sortable=True,
            source=Workflow
        )
        column_workflow_internal_name.add_exclude(source=WorkflowRuntimeProxy)
        column_workflow_get_initial_state = SourceColumn(
            attribute='get_initial_state', empty_value=_('None'),
            include_label=True, source=Workflow
        )
        column_workflow_get_initial_state.add_exclude(
            source=WorkflowRuntimeProxy
        )
        SourceColumn(
            attribute='get_current_state', include_label=True,
            label=_('Current state'), source=WorkflowInstance,
        )
        SourceColumn(
            func=lambda context: getattr(
                context['object'].get_last_log_entry(), 'user', _('None')
            ), include_label=True, label=_('User'), source=WorkflowInstance
        )
        SourceColumn(
            attribute='get_last_transition', include_label=True,
            label=_('Last transition'), source=WorkflowInstance
        )
        SourceColumn(
            func=lambda context: getattr(
                context['object'].get_last_log_entry(), 'datetime', _('None')
            ), include_label=True, label=_('Date and time'),
            source=WorkflowInstance
        )
        SourceColumn(
            func=lambda context: getattr(
                context['object'].get_current_state(), 'completion', _('None')
            ), include_label=True, label=_('Completion'),
            source=WorkflowInstance
        )

        SourceColumn(
            attribute='datetime', is_identifier=True, label=_('Date and time'),
            source=WorkflowInstanceLogEntry
        )
        SourceColumn(
            attribute='user', include_label=True, label=_('User'),
            source=WorkflowInstanceLogEntry
        )
        SourceColumn(
            attribute='transition__origin_state', include_label=True,
            is_sortable=True, source=WorkflowInstanceLogEntry
        )
        SourceColumn(
            attribute='transition', include_label=True, is_sortable=True,
            source=WorkflowInstanceLogEntry
        )
        SourceColumn(
            attribute='transition__destination_state', include_label=True,
            is_sortable=True, source=WorkflowInstanceLogEntry
        )
        SourceColumn(
            attribute='comment', include_label=True, is_sortable=True,
            source=WorkflowInstanceLogEntry
        )
        SourceColumn(
            attribute='get_extra_data', include_label=True,
            label=_('Additional details'), source=WorkflowInstanceLogEntry,
            widget=WorkflowLogExtraDataWidget
        )

        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=WorkflowState
        )
        SourceColumn(
            attribute='initial', include_label=True, is_sortable=True,
            source=WorkflowState, widget=TwoStateWidget
        )
        SourceColumn(
            attribute='completion', include_label=True, is_sortable=True,
            source=WorkflowState
        )

        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=WorkflowStateAction
        )
        SourceColumn(
            attribute='enabled', include_label=True, is_sortable=True,
            source=WorkflowStateAction, widget=TwoStateWidget
        )
        SourceColumn(
            attribute='get_when_display', include_label=True,
            label=_('When?'), source=WorkflowStateAction
        )
        SourceColumn(
            attribute='get_class_label', include_label=True,
            label=_('Action type'), source=WorkflowStateAction
        )
        SourceColumn(
            attribute='has_condition', include_label=True,
            source=WorkflowStateAction, widget=TwoStateWidget
        )

        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=WorkflowTransition,
        )
        SourceColumn(
            attribute='origin_state', include_label=True, is_sortable=True,
            source=WorkflowTransition
        )
        SourceColumn(
            attribute='destination_state', include_label=True, is_sortable=True,
            source=WorkflowTransition
        )
        SourceColumn(
            attribute='has_condition', include_label=True,
            source=WorkflowTransition, widget=TwoStateWidget
        )
        SourceColumn(
            attribute='get_field_display', include_label=True,
            source=WorkflowTransition
        )
        SourceColumn(
            func=lambda context: widget_transition_events(
                transition=context['object']
            ), help_text=_(
                'Triggers are system events that will cause the transition '
                'to be applied.'
            ), include_label=True, label=_('Triggers'),
            source=WorkflowTransition
        )

        SourceColumn(
            attribute='name', is_identifier=True, is_sortable=True,
            source=WorkflowTransitionField
        )
        SourceColumn(
            attribute='label', include_label=True, is_sortable=True,
            source=WorkflowTransitionField
        )
        SourceColumn(
            attribute='get_field_type_display', include_label=True,
            label=_('Type'), source=WorkflowTransitionField
        )
        SourceColumn(
            attribute='required', include_label=True, is_sortable=True,
            source=WorkflowTransitionField, widget=TwoStateWidget
        )
        SourceColumn(
            attribute='get_widget_display', include_label=True,
            label=_('Widget'), is_sortable=False,
            source=WorkflowTransitionField
        )
        SourceColumn(
            attribute='widget_kwargs', include_label=True, is_sortable=True,
            source=WorkflowTransitionField
        )

        SourceColumn(
            func=lambda context: context['object'].get_document_count(
                user=context['request'].user
            ), include_label=True, label=_('Documents'), order=99,
            source=WorkflowRuntimeProxy
        )
        SourceColumn(
            func=lambda context: context['object'].get_document_count(
                user=context['request'].user
            ), include_label=True, label=_('Documents'), order=99,
            source=WorkflowStateRuntimeProxy
        )

        menu_facet.bind_links(
            links=(link_workflow_instance_list,), sources=(Document,)
        )
        menu_secondary.bind_links(
            links=(link_document_single_workflow_templates_launch,),
            sources=(
                'document_states:document_multiple_workflow_templates_launch',
                'document_states:document_single_workflow_templates_launch',
                'document_states:workflow_instance_list', WorkflowInstance,
            )
        )

        menu_list_facet.bind_links(
            links=(
                link_acl_list, link_workflow_template_document_types,
                link_workflow_template_state_list,
                link_workflow_template_transition_list,
                link_workflow_template_preview
            ), sources=(Workflow,)
        )

        menu_list_facet.unbind_links(
            links=(
                link_acl_list, link_workflow_template_document_types,
                link_workflow_template_state_list,
                link_workflow_template_transition_list,
                link_workflow_template_preview
            ), sources=(WorkflowRuntimeProxy,)
        )

        menu_list_facet.bind_links(
            links=(
                link_document_type_workflow_templates,
            ), sources=(DocumentType,)
        )

        menu_main.bind_links(
            links=(link_workflow_runtime_proxy_list,), position=10
        )
        menu_multi_item.bind_links(
            links=(link_document_multiple_workflow_templates_launch,),
            sources=(Document,)
        )
        menu_multi_item.bind_links(
            links=(link_workflow_template_multiple_delete,),
            sources=(Workflow,)
        )
        menu_object.bind_links(
            links=(
                link_workflow_template_single_delete,
                link_workflow_template_edit,
                link_workflow_template_launch
            ), sources=(Workflow,)
        )
        menu_object.bind_links(
            links=(
                link_workflow_template_state_edit,
                link_workflow_template_state_action_list,
                link_workflow_template_state_delete
            ), sources=(WorkflowState,)
        )
        menu_object.bind_links(
            links=(
                link_workflow_template_transition_edit,
                link_workflow_template_transition_events,
                link_workflow_template_transition_field_list, link_acl_list,
                link_workflow_template_transition_delete
            ), sources=(WorkflowTransition,)
        )
        menu_object.bind_links(
            links=(
                link_workflow_template_transition_field_delete,
                link_workflow_template_transition_field_edit
            ), sources=(WorkflowTransitionField,)
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
                link_workflow_template_state_action_edit,
                link_workflow_template_state_action_delete,
            ), sources=(WorkflowStateAction,)
        )
        menu_related.bind_links(
            links=(link_workflow_template_list,),
            sources=(
                DocumentType, 'documents:document_type_list',
                'documents:document_type_create'
            )
        )
        menu_related.bind_links(
            links=(link_document_type_list,),
            sources=(
                Workflow, 'document_states:workflow_template_create',
                'document_states:workflow_template_list'
            )
        )
        menu_secondary.bind_links(
            links=(link_workflow_template_list, link_workflow_template_create),
            sources=(
                Workflow, 'document_states:workflow_template_create',
                'document_states:workflow_template_list'
            )
        )
        menu_secondary.bind_links(
            links=(link_workflow_template_transition_field_create,),
            sources=(
                WorkflowTransition,
            )
        )
        menu_secondary.bind_links(
            links=(link_workflow_template_state_action_selection,),
            sources=(
                WorkflowState,
            )
        )
        menu_secondary.bind_links(
            links=(
                link_workflow_template_transition_create,
            ), sources=(
                WorkflowTransition,
                'document_states:workflow_template_transition_create',
                'document_states:workflow_template_transition_list',
            )
        )
        menu_secondary.bind_links(
            links=(
                link_workflow_template_state_create,
            ), sources=(
                WorkflowState,
                'document_states:workflow_template_state_create',
                'document_states:workflow_template_state_list',
            )
        )

        menu_setup.bind_links(links=(link_workflow_template_list,))

        menu_tools.bind_links(links=(link_tool_launch_workflows,))

        post_save.connect(
            dispatch_uid='workflows_handler_launch_workflow',
            receiver=handler_launch_workflow,
            sender=Document
        )

        # Index updating

        post_migrate.connect(
            dispatch_uid='workflows_handler_create_workflow_image_cache',
            receiver=handler_create_workflow_image_cache,
        )
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
