from __future__ import absolute_import, unicode_literals

import logging
import json

import requests

from django.template import Template, Context
from django.utils.translation import ugettext_lazy as _

from .classes import WorkflowAction
from .exceptions import WorkflowStateActionError

__all__ = ('DocumentPropertiesEditAction', 'HTTPPostAction',)
logger = logging.getLogger(__name__)
DEFAULT_TIMEOUT = 4  # 4 seconds


class DocumentPropertiesEditAction(WorkflowAction):
    fields = {
        'document_label': {
            'label': _('Label'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _(
                    'The new label to be assigned to the document. Can be a '
                    'string or a template.'
                ), 'required': False
            },
        }, 'document_description': {
            'label': _('Description'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _(
                    'The new description to be assigned to the document. '
                    'Can be a string or a template.'
                ), 'required': False
            },
        },
    }
    field_order = ('document_label', 'document_description')
    label = _('Modify the properties of the document')
    widgets = {
        'document_description': {
            'class': 'django.forms.widgets.Textarea', 'kwargs': {
                'attrs': {'rows': '10'},
            }
        }
    }

    def execute(self, context):
        self.document_label = self.form_data.get('document_label')
        self.document_description = self.form_data.get('document_description')
        new_label = None
        new_description = None

        if self.document_label:
            try:
                new_label = Template(self.document_label).render(
                    context=Context(context)
                )
            except Exception as exception:
                raise WorkflowStateActionError(
                    _('Document label template error: %s') % exception
                )

            logger.debug('Document label result: %s', new_label)

        if self.document_description:
            try:
                new_description = Template(self.document_description or '{}').render(
                    context=Context(context)
                )
            except Exception as exception:
                raise WorkflowStateActionError(
                    _('Document description template error: %s') % exception
                )

            logger.debug('Document description template result: %s', new_description)

        if new_label or new_description:
            document = context['document']
            document.label = new_label or document.label
            document.description = new_description or document.description

            document.save()


class HTTPPostAction(WorkflowAction):
    fields = {
        'url': {
            'label': _('URL'),
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
        }, 'timeout': {
            'label': _('Timeout'),
            'class': 'django.forms.IntegerField', 'default': DEFAULT_TIMEOUT,
            'help_text': _('Time in seconds to wait for a response.'),
            'required': True

        }, 'payload': {
            'label': _('Payload'),
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
    }
    field_order = ('url', 'timeout', 'payload')
    label = _('Perform a POST request')
    widgets = {
        'payload': {
            'class': 'django.forms.widgets.Textarea', 'kwargs': {
                'attrs': {'rows': '10'},
            }
        }
    }

    def execute(self, context):
        self.url = self.form_data.get('url')
        self.payload = self.form_data.get('payload')

        try:
            url = Template(self.url).render(
                context=Context(context)
            )
        except Exception as exception:
            raise WorkflowStateActionError(
                _('URL template error: %s') % exception
            )

        logger.debug('URL template result: %s', url)

        try:
            result = Template(self.payload or '{}').render(
                context=Context(context)
            )
        except Exception as exception:
            raise WorkflowStateActionError(
                _('Payload template error: %s') % exception
            )

        logger.debug('payload template result: %s', result)

        try:
            payload = json.loads(result, strict=False)
        except Exception as exception:
            raise WorkflowStateActionError(
                _('Payload JSON error: %s') % exception
            )

        logger.debug('payload json result: %s', payload)

        requests.post(url=url, data=payload, timeout=self.form_data['timeout'])
