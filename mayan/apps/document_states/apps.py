from __future__ import unicode_literals

from django import apps
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from common import (
    menu_facet, menu_object, menu_secondary, menu_setup, menu_sidebar
)
from common.utils import encapsulate
from documents.models import Document
from navigation.api import register_model_list_columns

from .handlers import launch_workflow
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


class DocumentStatesApp(apps.AppConfig):
    name = 'document_states'
    verbose_name = _('Document states')

    def ready(self):
        menu_facet.bind_links(links=[link_document_workflow_instance_list], sources=[Document])
        menu_object.bind_links(links=[link_setup_workflow_states, link_setup_workflow_transitions, link_setup_workflow_document_types, link_setup_workflow_edit, link_setup_workflow_delete], sources=[Workflow])
        menu_object.bind_links(links=[link_setup_workflow_state_edit, link_setup_workflow_state_delete], sources=[WorkflowState])
        menu_object.bind_links(links=[link_setup_workflow_transition_edit, link_setup_workflow_transition_delete], sources=[WorkflowTransition])
        menu_object.bind_links(links=[link_workflow_instance_detail, link_workflow_instance_transition], sources=[WorkflowInstance])
        menu_secondary.bind_links(links=[link_setup_workflow_list, link_setup_workflow_create], sources=[Workflow, 'document_states:setup_workflow_create', 'document_states:setup_workflow_list'])
        menu_setup.bind_links(links=[link_setup_workflow_list])
        menu_sidebar.bind_links(links=[link_setup_workflow_state_create, link_setup_workflow_transition_create], sources=[Workflow])

        register_model_list_columns(Workflow, [
            {
                'name': _('Initial state'),
                'attribute': encapsulate(lambda workflow: workflow.get_initial_state() or _('None'))
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

        register_model_list_columns(WorkflowState, [
            {
                'name': _('Is initial state?'),
                'attribute': 'initial'
            },
            {
                'name': _('Completion'),
                'attribute': 'completion'
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

        post_save.connect(launch_workflow, dispatch_uid='launch_workflow', sender=Document)
