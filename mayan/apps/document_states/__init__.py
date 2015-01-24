from __future__ import unicode_literals

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _

from common.utils import encapsulate
from documents.models import Document
from navigation.api import register_links, register_model_list_columns
from project_setup.api import register_setup

from .models import (
    Workflow, WorkflowInstance, WorkflowInstanceLogEntry, WorkflowState,
    WorkflowTransition
)
from .links import (
    link_document_workflow_instance_list, link_setup_workflow_document_types,
    link_setup_workflow_create, link_setup_workflow_delete,
    link_setup_workflow_edit, link_setup_workflow_list,
    link_setup_workflow_states, link_setup_workflow_state_create,
    link_setup_workflow_state_delete, link_setup_workflow_state_edit,
    link_setup_workflow_transitions, link_setup_workflow_transition_create,
    link_setup_workflow_transition_delete, link_setup_workflow_transition_edit,
    link_workflow_instance_detail, link_workflow_instance_transition
)


@receiver(post_save, dispatch_uid='launch_workflow', sender=Document)
def launch_workflow(sender, instance, created, **kwargs):
    if created:
        Workflow.objects.launch_for(instance)


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

register_model_list_columns(WorkflowInstance, [
    {
        'name': _('Current state'),
        'attribute': 'get_current_state'
    },
    {
        'name': _('User'),
        'attribute': encapsulate(lambda workflow: getattr(workflow.get_last_log_entry(), 'user', _('None')))
    },
    {
        'name': _('Last transition'),
        'attribute': 'get_last_transition'
    },
    {
        'name': _('Date and time'),
        'attribute': encapsulate(lambda workflow: getattr(workflow.get_last_log_entry(), 'datetime', _('None')))
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

register_model_list_columns(WorkflowInstanceLogEntry, [
    {
        'name': _('Date and time'),
        'attribute': 'datetime'
    },
    {
        'name': _('User'),
        'attribute': 'user'
    },
    {
        'name': _('Transition'),
        'attribute': 'transition'
    },
    {
        'name': _('Comment'),
        'attribute': 'comment'
    },
])

register_links([Document], [link_document_workflow_instance_list], menu_name='form_header')
register_links([WorkflowInstance], [link_workflow_instance_detail, link_workflow_instance_transition])
register_links([Workflow, 'document_states:setup_workflow_create', 'document_states:setup_workflow_list'], [link_setup_workflow_list, link_setup_workflow_create], menu_name='secondary_menu')
register_links([Workflow], [link_setup_workflow_states, link_setup_workflow_transitions, link_setup_workflow_document_types, link_setup_workflow_edit, link_setup_workflow_delete])
register_links([Workflow], [link_setup_workflow_state_create, link_setup_workflow_transition_create], menu_name='sidebar')
register_links([WorkflowState], [link_setup_workflow_state_edit, link_setup_workflow_state_delete])
register_links([WorkflowTransition], [link_setup_workflow_transition_edit, link_setup_workflow_transition_delete])
