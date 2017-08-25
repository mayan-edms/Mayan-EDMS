from __future__ import absolute_import, unicode_literals

import logging
import json

import requests

from django.template import Template, Context
from django.utils.translation import ugettext_lazy as _

from .classes import WorkflowAction

__all__ = ('HTTPPostAction',)
logger = logging.getLogger(__name__)


class HTTPPostAction(WorkflowAction):
    fields = (
        {
            'name': 'url', 'label': _('URL'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _(
                    'Can be an IP address, a domain or a template. Templates '
                    'receive the workflow log entry instance as part of '
                    'their context via the variable "entry_log". '
                    'The "entry_log" in turn provides the '
                    '"workflow_instance", "datetime", "transition", "user", '
                    'and "comment" attributes.'
                ),
                'required': True
            },
        }, {
            'name': 'payload', 'label': _('Payload'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _(
                    'A JSON document to include in the request. Can also be '
                    'a template that return a JSON document. Templates '
                    'receive the workflow log entry instance as part of '
                    'their context via the variable "entry_log". '
                    'The "entry_log" in turn provides the '
                    '"workflow_instance", "datetime", "transition", "user", '
                    'and "comment" attributes.'
                ), 'required': False
            }

        },
    )
    label = _('Perform a POST request')
    widgets = {
        'payload': {
            'class': 'django.forms.widgets.Textarea', 'kwargs': {
                'attrs': {'rows': '10'},
            }
        }
    }

    def __init__(self, url=None, payload=None):
        self.url = url
        self.payload = payload

    def get_form_schema(self, request):
        return {
            'fields': self.fields,
            'widgets': self.widgets
        }

    def execute(self, context):
        try:
            url = Template(self.url).render(
                context=Context(context)
            )
        except Exception as exception:
            context['action'].error_logs.create(
                result='URL template error: {}'.format(exception)
            )
            return

        logger.debug('URL template result: %s', url)

        try:
            result = Template(self.payload or '{}').render(
                context=Context(context)
            )
        except Exception as exception:
            context['action'].error_logs.create(
                result='Payload template error: {}'.format(exception)
            )
            return

        logger.debug('payload template result: %s', result)

        try:
            payload = json.loads(result, strict=False)
        except Exception as exception:
            context['action'].error_logs.create(
                result='Payload JSON error: {}'.format(exception)
            )
            return

        logger.debug('payload json result: %s', payload)

        requests.post(url=url, data=payload)
