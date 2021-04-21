import logging
import json

import requests

from django.utils.translation import ugettext_lazy as _

from .classes import WorkflowAction
from .exceptions import WorkflowStateActionError
from .literals import DEFAULT_HTTP_ACTION_TIMEOUT
from .models import Workflow
from .tasks import task_launch_workflow_for

logger = logging.getLogger(name=__name__)


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
            new_label = self.render_field(
                field_name='document_label', context=context
            )

        if self.document_description:
            new_description = self.render_field(
                field_name='document_description', context=context
            )

        if new_label or new_description:
            document = context['document']
            document.label = new_label or document.label
            document.description = new_description or document.description

            document.save()


class DocumentWorkflowLaunchAction(WorkflowAction):
    fields = {
        'workflows': {
            'label': _('Workflows'),
            'class': 'django.forms.ModelMultipleChoiceField', 'kwargs': {
                'help_text': _(
                    'Additional workflows to launch for the document.'
                ), 'queryset': Workflow.objects.none()
            },
        },
    }
    field_order = ('workflows',)
    label = _('Launch workflows')
    widgets = {
        'workflows': {
            'class': 'django.forms.widgets.SelectMultiple', 'kwargs': {
                'attrs': {'class': 'select2'},
            }
        }
    }

    def get_form_schema(self, **kwargs):
        result = super().get_form_schema(**kwargs)

        workflows_union = Workflow.objects.filter(
            document_types__in=kwargs['workflow_state'].workflow.document_types.all()
        ).exclude(pk=kwargs['workflow_state'].workflow.pk).distinct()

        result['fields']['workflows']['kwargs']['queryset'] = workflows_union

        return result

    def execute(self, context):
        workflows = Workflow.objects.filter(
            pk__in=self.form_data.get('workflows', ())
        )

        for workflow in workflows:
            task_launch_workflow_for.apply_async(
                kwargs={
                    'document_id': context['document'].pk,
                    'workflow_id': workflow.pk
                }
            )


class HTTPAction(WorkflowAction):
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
            'class': 'django.forms.IntegerField',
            'default': DEFAULT_HTTP_ACTION_TIMEOUT,
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
        }, 'method': {
            'label': _('Method'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _(
                    'The HTTP method to use for the request. Typical choices '
                    'are OPTIONS, HEAD, POST, GET, PUT, PATCH, DELETE. '
                    'Can be a static value or a template that returns the '
                    'method text. Templates receive the workflow log entry '
                    'instance as part of their context via the '
                    'variable "entry_log". The "entry_log" in turn '
                    'provides the "workflow_instance", "datetime", '
                    '"transition", "user", and "comment" attributes.'
                ), 'required': True
            }
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
        'url', 'username', 'password', 'headers', 'timeout', 'method', 'payload'
    )
    label = _('Perform an HTTP request')
    previous_dotted_paths = (
        'mayan.apps.document_states.workflow_actions.HTTPPostAction',
    )
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

    def render_field_load(self, field_name, context):
        """
        Method to perform a template render and subsequent JSON load.
        """
        render_result = self.render_field(
            field_name=field_name, context=context
        ) or '{}'

        try:
            load_result = json.loads(s=render_result, strict=False)
        except Exception as exception:
            raise WorkflowStateActionError(
                _('%(field_name)s JSON error: %(exception)s') % {
                    'field_name': field_name, 'exception': exception
                }
            )

        logger.debug('load result: %s', load_result)

        return load_result

    def execute(self, context):
        headers = self.render_field_load(field_name='headers', context=context)
        method = self.render_field(field_name='method', context=context)
        password = self.render_field(field_name='password', context=context)
        payload = self.render_field_load(field_name='payload', context=context)
        timeout = self.render_field(field_name='timeout', context=context)
        url = self.render_field(field_name='url', context=context)
        username = self.render_field(field_name='username', context=context)

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

        requests.request(
            method=method, url=url, json=payload, timeout=timeout,
            auth=authentication, headers=headers
        )
