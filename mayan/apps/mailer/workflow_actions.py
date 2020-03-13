from __future__ import absolute_import, unicode_literals

import logging

from django.template import Template, Context
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.document_states.classes import WorkflowAction
from mayan.apps.document_states.exceptions import WorkflowStateActionError

from .models import UserMailer
from .permissions import permission_user_mailer_use

__all__ = ('EmailAction',)
logger = logging.getLogger(name=__name__)


class EmailAction(WorkflowAction):
    fields = {
        'mailing_profile': {
            'label': _('Mailing profile'),
            'class': 'django.forms.ModelChoiceField', 'kwargs': {
                'help_text': _('Mailing profile to use when sending the email.'),
                'queryset': UserMailer.objects.none(), 'required': True
            }
        },
        'recipient': {
            'label': _('Recipient'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _(
                    'Email address of the recipient. Can be multiple addresses '
                    'separated by comma or semicolon. A template can be used '
                    'to reference properties of the document.'
                ),
                'required': True
            }
        },
        'subject': {
            'label': _('Subject'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _(
                    'Subject of the email. Can be a string or a template.'
                ),
                'required': True
            }
        },
        'body': {
            'label': _('Body'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _(
                    'Body of the email to send. Can be a string or a template.'
                ),
                'required': True
            }
        },
    }
    field_order = ('mailing_profile', 'recipient', 'subject', 'body')
    label = _('Send email')
    widgets = {
        'body': {
            'class': 'django.forms.widgets.Textarea', 'kwargs': {}
        }
    }
    permission = permission_user_mailer_use

    def execute(self, context):
        try:
            recipient = Template(self.form_data['recipient']).render(
                context=Context(context)
            )
        except Exception as exception:
            raise WorkflowStateActionError(
                _('Recipient template error: %s') % exception
            )
        else:
            logger.debug('Recipient result: %s', recipient)

        try:
            subject = Template(self.form_data['subject']).render(
                context=Context(context)
            )
        except Exception as exception:
            raise WorkflowStateActionError(
                _('Subject template error: %s') % exception
            )
        else:
            logger.debug('Subject result: %s', subject)

        try:
            body = Template(self.form_data['body']).render(
                context=Context(context)
            )
        except Exception as exception:
            raise WorkflowStateActionError(
                _('Body template error: %s') % exception
            )
        else:
            logger.debug('Body result: %s', body)

        user_mailer = self.get_user_mailer()
        user_mailer.send(
            to=recipient, subject=subject, body=body,
        )

    def get_form_schema(self, request):
        user = request.user
        logger.debug('user: %s', user)

        queryset = AccessControlList.objects.restrict_queryset(
            permission=self.permission, queryset=UserMailer.objects.all(),
            user=user
        )

        self.fields['mailing_profile']['kwargs']['queryset'] = queryset

        return {
            'field_order': self.field_order,
            'fields': self.fields,
            'widgets': self.widgets
        }

    def get_user_mailer(self):
        return UserMailer.objects.get(pk=self.form_data['mailing_profile'])
