from __future__ import absolute_import, unicode_literals

import logging

from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.document_states.classes import WorkflowAction

from .models import UserMailer
from .permissions import permission_user_mailer_use

__all__ = ('EmailAction',)
logger = logging.getLogger(__name__)


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
                    'separated by comma or semicolon.'
                ),
                'required': True
            }
        },
        'subject': {
            'label': _('Subject'),
            'class': 'django.forms.CharField', 'kwargs': {
                'required': True
            }
        },
        'body': {
            'label': _('Body'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _('Body of the email to send.'),
                'required': True
            }
        },
    }
    label = _('Send email')
    widgets = {
        'body': {
            'class': 'django.forms.widgets.Textarea', 'kwargs': {}
        }
    }
    permission = permission_user_mailer_use

    def execute(self, context):
        user_mailer = self.get_user_mailer()
        user_mailer.send(
            to=self.form_data['recipient'], subject=self.form_data['subject'],
            body=self.form_data['body'],
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
            'fields': self.fields,
            'widgets': self.widgets
        }

    def get_user_mailer(self):
        return UserMailer.objects.get(pk=self.form_data['mailing_profile'])
