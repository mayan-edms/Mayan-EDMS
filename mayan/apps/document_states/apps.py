from __future__ import unicode_literals

from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from common import (
    MayanAppConfig, menu_facet, menu_object, menu_secondary, menu_setup,
    menu_sidebar
)
from common.widgets import two_state_template
from documents.models import Document
from navigation import SourceColumn

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


class DocumentStatesApp(MayanAppConfig):
    app_url = 'states'
    name = 'document_states'
    test = True
    verbose_name = _('Document states')

    def ready(self):
        super(DocumentStatesApp, self).ready()

        SourceColumn(
            source=Workflow, label=_('Initial state'),
            func=lambda context: context['object'].get_initial_state() or _('None')
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
            source=WorkflowState, label=_('Is initial state?'),
            func=lambda context: two_state_template(context['object'].initial)
        )
        SourceColumn(
            source=WorkflowState, label=_('Completion'), attribute='completion'
        )

        SourceColumn(
            source=WorkflowTransition, label=_('Origin state'),
            attribute='origin_state'
        )
        SourceColumn(
            source=WorkflowTransition, label=_('Destination state'),
            attribute='destination_state'
        )

        menu_facet.bind_links(
            links=(link_document_workflow_instance_list,), sources=(Document,)
        )
        menu_object.bind_links(
            links=(
                link_setup_workflow_states, link_setup_workflow_transitions,
                link_setup_workflow_document_types, link_setup_workflow_edit,
                link_setup_workflow_delete
            ), sources=(Workflow,)
        )
        menu_object.bind_links(
            links=(
                link_setup_workflow_state_edit,
                link_setup_workflow_state_delete
            ), sources=(WorkflowState,)
        )
        menu_object.bind_links(
            links=(
                link_setup_workflow_transition_edit,
                link_setup_workflow_transition_delete
            ), sources=(WorkflowTransition,)
        )
        menu_object.bind_links(
            links=(
                link_workflow_instance_detail,
                link_workflow_instance_transition
            ), sources=(WorkflowInstance,)
        )
        menu_secondary.bind_links(
            links=(link_setup_workflow_list, link_setup_workflow_create),
            sources=(
                Workflow, 'document_states:setup_workflow_create',
                'document_states:setup_workflow_list'
            )
        )
        menu_setup.bind_links(links=(link_setup_workflow_list,))
        menu_sidebar.bind_links(
            links=(
                link_setup_workflow_state_create,
                link_setup_workflow_transition_create
            ), sources=(Workflow,)
        )

        post_save.connect(
            launch_workflow, dispatch_uid='launch_workflow', sender=Document
        )
