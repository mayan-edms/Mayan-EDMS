from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from common.utils import encapsulate
from navigation.api import register_links, register_model_list_columns
from project_setup.api import register_setup

from .models import Workflow, WorkflowState, WorkflowTransition
from .links import (link_setup_workflow_create, link_setup_workflow_delete,
                    link_setup_workflow_edit, link_setup_workflow_list,
                    link_setup_workflow_states, link_setup_workflow_states_create,
                    link_setup_workflow_transitions, link_setup_workflow_transitions_create)

register_setup(link_setup_workflow_list)

register_model_list_columns(Workflow, [
    {
        'name': _('Initial state'),
        'attribute': encapsulate(lambda workflow: workflow.get_initial_state() or _('None'))
    },
])

register_model_list_columns(WorkflowState, [
    {
        'name': _('Is initial state?'),
        'attribute': 'initial'
    },
])

register_model_list_columns(WorkflowTransition, [
    {
        'name': _('Origin state'),
        'attribute': 'origin_state'
    },
    {
        'name': _('Destination state'),
        'attribute': 'destination_state'
    },
])

register_links([Workflow, 'document_states:setup_workflow_create', 'document_states:setup_workflow_list'], [link_setup_workflow_list, link_setup_workflow_create], menu_name='secondary_menu')
register_links([Workflow], [link_setup_workflow_states, link_setup_workflow_transitions, link_setup_workflow_edit, link_setup_workflow_delete])
register_links([Workflow], [link_setup_workflow_states_create, link_setup_workflow_transitions_create], menu_name='sidebar')
