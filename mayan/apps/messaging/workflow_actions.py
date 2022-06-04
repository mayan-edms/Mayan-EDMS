import logging

from django.utils.text import format_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.document_states.classes import WorkflowAction
from mayan.apps.document_states.literals import BASE_WORKFLOW_TEMPLATE_STATE_ACTION_HELP_TEXT
from mayan.apps.document_states.models.workflow_instance_models import WorkflowInstance
from mayan.apps.user_management.querysets import get_user_queryset

from .models import Message

logger = logging.getLogger(name=__name__)


class WorkflowActionMessageSend(WorkflowAction):
    fields = {
        'username_list': {
            'label': _('Username list'),
            'class': 'mayan.apps.templating.fields.ModelTemplateField',
            'kwargs': {
                'initial_help_text': _(
                    format_lazy(
                        '{}. {}',
                        _(
                            'Comma separated list of username that will '
                            'receive the message.'
                        ),
                        BASE_WORKFLOW_TEMPLATE_STATE_ACTION_HELP_TEXT
                    )
                ),
                'model': WorkflowInstance,
                'model_variable': 'workflow_instance',
                'required': True
            },
        },
        'subject': {
            'label': _('Subject'),
            'class': 'mayan.apps.templating.fields.ModelTemplateField',
            'kwargs': {
                'initial_help_text': _(
                    format_lazy(
                        '{}. {}',
                        _(
                            'Topic of the message to be sent.'
                        ), BASE_WORKFLOW_TEMPLATE_STATE_ACTION_HELP_TEXT
                    )
                ),
                'model': WorkflowInstance,
                'model_variable': 'workflow_instance',
                'required': True
            },
        },
        'body': {
            'label': _('Body'),
            'class': 'mayan.apps.templating.fields.ModelTemplateField',
            'kwargs': {
                'initial_help_text': _(
                    format_lazy(
                        '{}. {}',
                        _(
                            'The actual text to send.'
                        ), BASE_WORKFLOW_TEMPLATE_STATE_ACTION_HELP_TEXT
                    )
                ),
                'model': WorkflowInstance,
                'model_variable': 'workflow_instance',
                'required': True
            },
        },
    }
    field_order = ('username_list', 'subject', 'body')
    label = _('Send user message')

    def execute(self, context):
        username_list = self.render_field(
            field_name='username_list', context=context
        ) or ''
        username_list = username_list.split(',')

        subject = self.render_field(
            field_name='subject', context=context
        ) or ''

        body = self.render_field(
            field_name='body', context=context
        ) or ''

        for user in get_user_queryset().filter(username__in=username_list):
            Message.objects.create(
                user=user, body=body, subject=subject
            )
