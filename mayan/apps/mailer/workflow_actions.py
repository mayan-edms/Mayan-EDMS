import logging

from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.document_states.classes import WorkflowAction

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
        'cc': {
            'label': _('CC'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _(
                    'Address used in the "Bcc" header when sending the '
                    'email. Can be multiple addresses '
                    'separated by comma or semicolon. A template can be used '
                    'to reference properties of the document.'
                ),
                'required': False
            }
        },
        'bcc': {
            'label': _('BCC'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _(
                    'Address used in the "Bcc" header when sending the '
                    'email. Can be multiple addresses '
                    'separated by comma or semicolon. A template can be used '
                    'to reference properties of the document.'
                ),
                'required': False
            }
        },
        'reply_to': {
            'label': _('Reply to'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _(
                    'Address used in the "Reply-To" header when sending the '
                    'email. Can be multiple addresses '
                    'separated by comma or semicolon. A template can be used '
                    'to reference properties of the document.'
                ),
                'required': False
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
        'attachment': {
            'label': _('Attachment'),
            'class': 'django.forms.BooleanField', 'default': False,
            'help_text': _(
                'Attach the document to the mail.'
            ),
            'required': False
        },
    }
    field_order = (
        'mailing_profile', 'recipient', 'cc', 'bcc', 'reply_to', 'subject',
        'body', 'attachment'
    )
    label = _('Send email')
    widgets = {
        'body': {
            'class': 'django.forms.widgets.Textarea', 'kwargs': {}
        }
    }
    permission = permission_user_mailer_use

    def execute(self, context):
        recipient = self.render_field(
            field_name='recipient', context=context
        )
        cc = self.render_field(
            field_name='cc', context=context
        )
        bcc = self.render_field(
            field_name='bcc', context=context
        )
        reply_to = self.render_field(
            field_name='reply_to', context=context
        )
        subject = self.render_field(
            field_name='subject', context=context
        )
        body = self.render_field(
            field_name='body', context=context
        )
        user_mailer = self.get_user_mailer()

        kwargs = {
            'bcc': bcc, 'cc': cc, 'body': body, 'reply_to': reply_to,
            'subject': subject, 'to': recipient
        }

        if self.form_data.get('attachment', False):
            kwargs.update(
                {
                    'as_attachment': True,
                    'document': context['document']
                }
            )
            user_mailer.send_document(**kwargs)
        else:
            user_mailer.send(**kwargs)

    def get_form_schema(self, **kwargs):
        result = super().get_form_schema(**kwargs)

        queryset = AccessControlList.objects.restrict_queryset(
            permission=self.permission, queryset=UserMailer.objects.all(),
            user=kwargs['request'].user
        )

        result['fields']['mailing_profile']['kwargs']['queryset'] = queryset

        return result

    def get_user_mailer(self):
        return UserMailer.objects.get(pk=self.form_data['mailing_profile'])
