from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.permissions import permission_document_type_edit
from mayan.apps.navigation.classes import Link
from mayan.apps.navigation.utils import get_cascade_condition

from .permissions import (
    permission_workflow_create, permission_workflow_delete,
    permission_workflow_edit, permission_workflow_tools,
    permission_workflow_view,
)

# Workflow templates

link_document_type_workflow_templates = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_document_type_workflow_list',
    permissions=(permission_document_type_edit,), text=_('Workflows'),
    view='document_states:document_type_workflow_templates',
)
link_workflow_template_create = Link(
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_template_create',
    permissions=(permission_workflow_create,),
    text=_('Create workflow'), view='document_states:workflow_template_create'
)
link_workflow_template_delete = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_template_delete',
    permissions=(permission_workflow_delete,),
    tags='dangerous', text=_('Delete'),
    view='document_states:workflow_template_delete',
)
link_workflow_template_document_types = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_template_document_type_list',
    permissions=(permission_workflow_edit,), text=_('Document types'),
    view='document_states:workflow_template_document_types',
)
link_workflow_template_edit = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_template_edit',
    permissions=(permission_workflow_edit,),
    text=_('Edit'), view='document_states:workflow_template_edit',
)
link_workflow_template_launch = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_template_launch',
    permissions=(permission_workflow_tools,),
    text=_('Launch workflow'),
    view='document_states:workflow_template_launch'
)
link_workflow_template_list = Link(
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_template_list',
    permissions=(permission_workflow_view,), text=_('Workflows'),
    view='document_states:workflow_template_list'
)
link_workflow_template_preview = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_template_preview',
    permissions=(permission_workflow_view,),
    text=_('Preview'), view='document_states:workflow_template_preview'
)

# Workflow template state actions

link_workflow_template_state_action_delete = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_state_action_delete',
    permissions=(permission_workflow_edit,),
    tags='dangerous', text=_('Delete'),
    view='document_states:workflow_template_state_action_delete',
)
link_workflow_template_state_action_edit = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_state_action_edit',
    permissions=(permission_workflow_edit,),
    text=_('Edit'), view='document_states:workflow_template_state_action_edit',
)
link_workflow_template_state_action_list = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_state_action_list',
    permissions=(permission_workflow_edit,),
    text=_('Actions'),
    view='document_states:workflow_template_state_action_list',
)
link_workflow_template_state_action_selection = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_state_action',
    permissions=(permission_workflow_edit,), text=_('Create action'),
    view='document_states:workflow_template_state_action_selection',
)

# Workflow template states

link_workflow_template_state_create = Link(
    args='workflow.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_state_create',
    permissions=(permission_workflow_edit,), text=_('Create state'),
    view='document_states:workflow_template_state_create',
)
link_workflow_template_state_delete = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_state_delete',
    permissions=(permission_workflow_edit,),
    tags='dangerous', text=_('Delete'),
    view='document_states:workflow_template_state_delete',
)
link_workflow_template_state_edit = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_state_edit',
    permissions=(permission_workflow_edit,),
    text=_('Edit'), view='document_states:workflow_template_state_edit',
)
link_workflow_template_state_list = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_state',
    permissions=(permission_workflow_view,), text=_('States'),
    view='document_states:workflow_template_state_list',
)

# Workflow template transitions

link_workflow_template_transition_create = Link(
    args='workflow.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_transition_create',
    permissions=(permission_workflow_edit,), text=_('Create transition'),
    view='document_states:workflow_template_transition_create',
)
link_workflow_template_transition_delete = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_transition_delete',
    permissions=(permission_workflow_edit,),
    tags='dangerous', text=_('Delete'),
    view='document_states:workflow_template_transition_delete',
)
link_workflow_template_transition_edit = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_transition_edit',
    permissions=(permission_workflow_edit,),
    text=_('Edit'), view='document_states:workflow_template_transition_edit',
)
link_workflow_template_transition_events = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_transition_triggers',
    permissions=(permission_workflow_edit,),
    text=_('Transition triggers'),
    view='document_states:workflow_template_transition_events'
)
link_workflow_template_transition_list = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_transition',
    permissions=(permission_workflow_view,), text=_('Transitions'),
    view='document_states:workflow_template_transition_list',
)

# Workflow transition fields

link_workflow_template_transition_field_create = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_transition_field',
    permissions=(permission_workflow_edit,), text=_('Create field'),
    view='document_states:workflow_template_transition_field_create',
)
link_workflow_template_transition_field_delete = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_transition_field_delete',
    permissions=(permission_workflow_edit,),
    tags='dangerous', text=_('Delete'),
    view='document_states:workflow_template_transition_field_delete',
)
link_workflow_template_transition_field_edit = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_transition_field_edit',
    permissions=(permission_workflow_edit,),
    text=_('Edit'), view='document_states:workflow_template_transition_field_edit',
)
link_workflow_template_transition_field_list = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_transition_field_list',
    permissions=(permission_workflow_edit,),
    text=_('Fields'),
    view='document_states:workflow_template_transition_field_list',
)

# Document workflow instances

link_workflow_instance_detail = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_instance_detail',
    permissions=(permission_workflow_view,),
    text=_('Detail'), view='document_states:workflow_instance_detail',
)
link_workflow_instance_list = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_instance_list',
    permissions=(permission_workflow_view,), text=_('Workflows'),
    view='document_states:workflow_instance_list',
)
link_workflow_instance_transition = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_instance_transition',
    text=_('Transition'),
    view='document_states:workflow_instance_transition_selection',
)

# Runtime proxies

link_workflow_runtime_proxy_document_list = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_runtime_proxy_document_list',
    permissions=(permission_workflow_view,),
    text=_('Workflow documents'),
    view='document_states:workflow_runtime_proxy_document_list',
)
link_workflow_runtime_proxy_list = Link(
    condition=get_cascade_condition(
        app_label='document_states', model_name='WorkflowRuntimeProxy',
        object_permission=permission_workflow_view,
    ), icon_class_path='mayan.apps.document_states.icons.icon_workflow_runtime_proxy_list',
    text=_('Workflows'), view='document_states:workflow_runtime_proxy_list'
)
link_workflow_runtime_proxy_state_document_list = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_runtime_proxy_state_document_list',
    permissions=(permission_workflow_view,),
    text=_('State documents'),
    view='document_states:workflow_runtime_proxy_state_document_list',
)
link_workflow_runtime_proxy_state_list = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_states.icons.icon_workflow_runtime_proxy_state_list',
    permissions=(permission_workflow_view,),
    text=_('States'), view='document_states:workflow_runtime_proxy_state_list',
)

# Tools

link_tool_launch_workflows = Link(
    icon_class_path='mayan.apps.document_states.icons.icon_tool_launch_workflows',
    permissions=(permission_workflow_tools,),
    text=_('Launch all workflows'),
    view='document_states:tool_launch_workflows'
)
