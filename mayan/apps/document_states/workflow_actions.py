from __future__ import absolute_import, unicode_literals

import logging
import json

import requests

from django.template import Template, Context
from django.utils.translation import ugettext_lazy as _

from .classes import WorkflowAction
from .exceptions import WorkflowStateActionError

logger = logging.getLogger(name=__name__)
DEFAULT_TIMEOUT = 4  # 4 seconds


class DocumentPropertiesEditAction(WorkflowAction):
    fields = {
        'document_label': {
            'label': _('Document label'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _(
                    'The new label to be assigned to the document. Can be a '
                    'string or a template.'
                ), 'required': False
            },
        }, 'document_description': {
            'label': _('Document description'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _(
                    'The new description to be assigned to the document. '
                    'Can be a string or a template.'
                ), 'required': False
            },
        },
    }
    field_order = ('document_label', 'document_description')
    label = _('Modify document properties')
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
            'help_text': _(
                'Time in seconds to wait for a response. Can be a static '
                'value or a template. '
            ),
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
            },
        }, 'username': {
            'label': _('Username'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _(
                    'Username to use for making the request with HTTP Basic '
                    'Auth. Can be a static value or a template. Templates '
                    'receive the workflow log entry instance as part of '
                    'their context via the variable "entry_log". '
                    'The "entry_log" in turn provides the '
                    '"workflow_instance", "datetime", "transition", "user", '
                    'and "comment" attributes.'
                ), 'max_length': 192, 'required': False
            },
        }, 'password': {
            'label': _('Password'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _(
                    'Password to use for making the request with HTTP Basic '
                    'Auth. Can be a static value or a template. Templates '
                    'receive the workflow log entry instance as part of '
                    'their context via the variable "entry_log". '
                    'The "entry_log" in turn provides the '
                    '"workflow_instance", "datetime", "transition", "user", '
                    'and "comment" attributes.'
                ), 'max_length': 192, 'required': False
            },
        }, 'headers': {
            'label': _('Headers'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _(
                    'Headers to send with the HTTP request. Must be in JSON '
                    'format. Can be a static value or a template. Templates '
                    'receive the workflow log entry instance as part of '
                    'their context via the variable "entry_log". '
                    'The "entry_log" in turn provides the '
                    '"workflow_instance", "datetime", "transition", "user", '
                    'and "comment" attributes.'
                ), 'required': False
            },
        }
    }
    field_order = (
        'url', 'username', 'password', 'headers', 'timeout', 'payload'
    )
    label = _('Perform a POST request')
    widgets = {
        'payload': {
            'class': 'django.forms.widgets.Textarea', 'kwargs': {
                'attrs': {'rows': '10'},
            }
        },
        'headers': {
            'class': 'django.forms.widgets.Textarea', 'kwargs': {
                'attrs': {'rows': '10'},
            }
        }
    }

    def render_load(self, field_name, context):
        """
        Method to perform a template render and subsequent JSON load.
        """
        render_result = self.render(
            field_name=field_name, context=context
        ) or '{}'

        try:
            load_result = json.loads(render_result, strict=False)
        except Exception as exception:
            raise WorkflowStateActionError(
                _('%(field_name)s JSON error: %(exception)s') % {
                    'field_name': field_name, 'exception': exception
                }
            )

        logger.debug('load result: %s', load_result)

        return load_result

    def render(self, field_name, context):
        try:
            result = Template(self.form_data.get(field_name, '')).render(
                context=Context(context)
            )
        except Exception as exception:
            raise WorkflowStateActionError(
                _('%(field_name)s template error: %(exception)s') % {
                    'field_name': field_name, 'exception': exception
                }
            )

        logger.debug('%s template result: %s', field_name, result)

        return result

    def execute(self, context):
        url = self.render(field_name='url', context=context)
        username = self.render(field_name='username', context=context)
        password = self.render(field_name='password', context=context)
        timeout = self.render(field_name='timeout', context=context)
        headers = self.render_load(field_name='headers', context=context)
        payload = self.render_load(field_name='payload', context=context)

        if '.' in timeout:
            timeout = float(timeout)
        elif timeout:
            timeout = int(timeout)
        else:
            timeout = None

        authentication = None
        if username or password:
            authentication = requests.auth.HTTPBasicAuth(
                username=username, password=password
            )

        requests.post(
            url=url, json=payload, timeout=timeout,
            auth=authentication, headers=headers
        )
