from __future__ import absolute_import, unicode_literals

from mayan.apps.appearance.classes import Icon
from mayan.apps.documents.icons import icon_document, icon_document_type

icon_workflow = Icon(driver_name='fontawesome', symbol='sitemap')

icon_tool_launch_workflows = icon_workflow

icon_document_type_workflow_list = icon_workflow
icon_workflow_template_create = Icon(
    driver_name='fontawesome-dual', primary_symbol='sitemap',
    secondary_symbol='plus'
)
icon_workflow_template_delete = Icon(
    driver_name='fontawesome', symbol='times'
)
icon_workflow_template_document_type_list = icon_document_type
icon_workflow_template_edit = Icon(
    driver_name='fontawesome', symbol='pencil-alt'
)
icon_workflow_template_launch = Icon(driver_name='fontawesome', symbol='play')
icon_workflow_template_list = icon_workflow
icon_workflow_template_preview = Icon(driver_name='fontawesome', symbol='eye')

# Workflow instances

icon_workflow_instance_detail = icon_workflow
icon_workflow_instance_list = icon_workflow
icon_workflow_instance_transition = Icon(
    driver_name='fontawesome', symbol='arrows-alt-h'
)

# Workflow runtime proxies

icon_workflow_runtime_proxy_document_list = icon_document
icon_workflow_runtime_proxy_list = icon_workflow
icon_workflow_runtime_proxy_state_document_list = icon_document
icon_workflow_runtime_proxy_state_list = Icon(
    driver_name='fontawesome', symbol='circle'
)

# Workflow transition states

icon_workflow_state_action_delete = Icon(
    driver_name='fontawesome', symbol='times'
)
icon_workflow_state_action_edit = Icon(
    driver_name='fontawesome', symbol='pencil-alt'
)
icon_workflow_state_action_list = Icon(
    driver_name='fontawesome', symbol='code'
)
icon_workflow_state = Icon(driver_name='fontawesome', symbol='circle')
icon_workflow_state_create = Icon(
    driver_name='fontawesome-dual', primary_symbol='circle',
    secondary_symbol='plus'
)
icon_workflow_state_delete = Icon(driver_name='fontawesome', symbol='times')
icon_workflow_state_edit = Icon(
    driver_name='fontawesome', symbol='pencil-alt'
)

# Workflow transition state actions

icon_workflow_state_action = Icon(driver_name='fontawesome', symbol='code')
icon_workflow_state_action_delete = Icon(
    driver_name='fontawesome', symbol='times'
)
icon_workflow_state_action_edit = Icon(
    driver_name='fontawesome', symbol='pencil-alt'
)
icon_workflow_state_action_selection = Icon(
    driver_name='fontawesome-dual', primary_symbol='code',
    secondary_symbol='plus'
)
icon_workflow_state_action_list = Icon(
    driver_name='fontawesome', symbol='code'
)

# Workflow transitions

icon_workflow_transition = Icon(
    driver_name='fontawesome', symbol='arrows-alt-h'
)
icon_workflow_transition_create = Icon(
    driver_name='fontawesome-dual', primary_symbol='arrows-alt-h',
    secondary_symbol='plus'
)
icon_workflow_transition_delete = Icon(
    driver_name='fontawesome', symbol='times'
)
icon_workflow_transition_edit = Icon(
    driver_name='fontawesome', symbol='pencil-alt'
)

# Workflow transition fields

icon_workflow_transition_field = Icon(
    driver_name='fontawesome', symbol='table'
)
icon_workflow_transition_field_delete = Icon(
    driver_name='fontawesome', symbol='times'
)
icon_workflow_transition_field_edit = Icon(
    driver_name='fontawesome', symbol='pencil-alt'
)
icon_workflow_transition_field_create = Icon(
    driver_name='fontawesome-dual', primary_symbol='table',
    secondary_symbol='plus'
)
icon_workflow_transition_field_list = Icon(
    driver_name='fontawesome', symbol='table'
)
icon_workflow_transition_triggers = Icon(
    driver_name='fontawesome', symbol='bolt'
)
