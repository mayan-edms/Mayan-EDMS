from __future__ import unicode_literals

from django.apps import apps
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from kombu import Exchange, Queue

from common import (
    MayanAppConfig, menu_facet, menu_main, menu_object, menu_secondary,
    menu_setup, menu_sidebar, menu_tools
)
from common.widgets import two_state_template
from mayan.celery import app
from navigation import SourceColumn
from rest_api.classes import APIEndPoint

from .handlers import launch_workflow
from .links import (
    link_document_workflow_instance_list, link_setup_workflow_document_types,
    link_setup_workflow_create, link_setup_workflow_delete,
    link_setup_workflow_edit, link_setup_workflow_list,
    link_setup_workflow_states, link_setup_workflow_state_create,
    link_setup_workflow_state_delete, link_setup_workflow_state_edit,
    link_setup_workflow_transitions, link_setup_workflow_transition_create,
    link_setup_workflow_transition_delete, link_setup_workflow_transition_edit,
    link_tool_launch_all_workflows, link_workflow_instance_detail,
    link_workflow_instance_transition, link_workflow_document_list,
    link_workflow_list, link_workflow_state_document_list,
    link_workflow_state_list
)


class DocumentStatesApp(MayanAppConfig):
    app_url = 'states'
    name = 'document_states'
    test = True
    verbose_name = _('Document states')

    def ready(self):
        super(DocumentStatesApp, self).ready()

        APIEndPoint(app=self, version_string='1')

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        Workflow = self.get_model('Workflow')
        WorkflowInstance = self.get_model('WorkflowInstance')
        WorkflowInstanceLogEntry = self.get_model('WorkflowInstanceLogEntry')
        WorkflowRuntimeProxy = self.get_model('WorkflowRuntimeProxy')
        WorkflowState = self.get_model('WorkflowState')
        WorkflowStateRuntimeProxy = self.get_model('WorkflowStateRuntimeProxy')
        WorkflowTransition = self.get_model('WorkflowTransition')

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

        app.conf.CELERY_QUEUES.extend(
            (
                Queue(
                    'document_states', Exchange('document_states'),
                    routing_key='converter'
                ),
            )
        )

        app.conf.CELERY_ROUTES.update(
            {
                'document_states.tasks.task_launch_all_workflows': {
                    'queue': 'document_states'
                },
            }
        )

        menu_facet.bind_links(
            links=(link_document_workflow_instance_list,), sources=(Document,)
        )
        menu_main.bind_links(links=(link_workflow_list,), position=10)
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
        menu_object.bind_links(
            links=(
                link_workflow_document_list, link_workflow_state_list,
            ), sources=(WorkflowRuntimeProxy,)
        )
        menu_object.bind_links(
            links=(
                link_workflow_state_document_list,
            ), sources=(WorkflowStateRuntimeProxy,)
        )
        menu_secondary.bind_links(
            links=(link_setup_workflow_list, link_setup_workflow_create),
            sources=(
                Workflow, 'document_states:setup_workflow_create',
                'document_states:setup_workflow_list'
            )
        )
        menu_secondary.bind_links(
            links=(link_workflow_list,),
            sources=(
                WorkflowRuntimeProxy,
            )
        )
        menu_setup.bind_links(links=(link_setup_workflow_list,))
        menu_sidebar.bind_links(
            links=(
                link_setup_workflow_state_create,
                link_setup_workflow_transition_create
            ), sources=(Workflow,)
        )
        menu_tools.bind_links(links=(link_tool_launch_all_workflows,))

        post_save.connect(
            launch_workflow, dispatch_uid='launch_workflow', sender=Document
        )
