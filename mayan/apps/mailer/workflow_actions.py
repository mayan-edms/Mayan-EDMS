import logging

from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.document_states.classes import WorkflowAction

from .literals import MODEL_SEND_FUNCTION_DOTTED_PATH
from .models import UserMailer
from .permissions import permission_user_mailer_use

__all__ = ('DocumentEmailAction',)
logger = logging.getLogger(name=__name__)


class ObjectEmailActionMixin:
    fields = {
        'mailing_profile': {
            'label': _('Mailing profile'),
            'class': 'django.forms.ModelChoiceField', 'kwargs': {
                'help_text': _(
                    'Mailing profile to use when sending the email.'
                ), 'queryset': UserMailer.objects.none(), 'required': True
            }
        },
        'recipient': {
            'label': _('Recipient'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _(
                    'Email address of the recipient. Can be multiple '
                    'addresses separated by comma or semicolon. A template '
                    'can be used to reference properties of the document.'
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
                    'separated by comma or semicolon. A template can be '
                    'used to reference properties of the document.'
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
                    'separated by comma or semicolon. A template can be '
                    'used to reference properties of the document.'
                ),
                'required': False
            }
        },
        'reply_to': {
            'label': _('Reply to'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _(
                    'Address used in the "Reply-To" header when sending '
                    'the email. Can be multiple addresses separated by '
                    'comma or semicolon. A template can be used to '
                    'reference properties of the document.'
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
                    'Body of the email to send. Can be a string or '
                    'a template.'
                ),
                'required': True
            }
        },
        'attachment': {
            'label': _('Attachment'),
            'class': 'django.forms.BooleanField', 'default': False,
            'help_text': _(
                'Attach an object to the email.'
            ),
            'required': False
        },
    }
    field_order = (
        'mailing_profile', 'recipient', 'cc', 'bcc', 'reply_to', 'subject',
        'body'
    )
    label = _('Send object via email')
    widgets = {
        'body': {
            'class': 'django.forms.widgets.Textarea', 'kwargs': {}
        }
    }
    permission = permission_user_mailer_use

    def execute(self, context):
        user_mailer = self.get_user_mailer()
        user_mailer.send_object(**self.get_execute_data(context=context))

    def get_execute_data(self, context):
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

        kwargs = {
            'bcc': bcc, 'cc': cc, 'body': body,
            'obj': self.get_object(context=context), 'reply_to': reply_to,
            'subject': subject, 'to': recipient
        }

        return kwargs

    def get_form_schema(self, **kwargs):
        result = super().get_form_schema(**kwargs)

        queryset = AccessControlList.objects.restrict_queryset(
            permission=self.permission,
            queryset=UserMailer.objects.filter(enabled=True),
            user=kwargs['request'].user
        )

        result['fields']['mailing_profile']['kwargs']['queryset'] = queryset

        return result

    def get_object(self, context):
        return NotImplementedError

    def get_user_mailer(self):
        return UserMailer.objects.get(pk=self.form_data['mailing_profile'])


class DocumentEmailAction(ObjectEmailActionMixin, WorkflowAction):
    fields = ObjectEmailActionMixin.fields.copy()
    fields.update(
        {
            'attachment': {
                'label': _('Attachment'),
                'class': 'django.forms.BooleanField', 'default': False,
                'help_text': _(
                    'Attach the exported document version to the email.'
                ),
                'required': False
            },
        }
    )
    field_order = list(
        ObjectEmailActionMixin.field_order
    ).append('attachment')
    label = _('Send document via email')

    def get_execute_data(self, context):
        result = super().get_execute_data(context=context)
        document = self.get_object(context=context)

        if self.form_data.get('attachment', False):
            if document.version_active:
                # Document must have a version active in order to be able
                # to export and attach.
                obj = document.version_active
                result.update(
                    {
                        'as_attachment': True,
                        'obj': obj
                    }
                )
                result.update(
                    MODEL_SEND_FUNCTION_DOTTED_PATH.get(
                        obj._meta.model, {}
                    )
                )

        return result

    def get_object(self, context):
        return context['document']


class EmailAction(DocumentEmailAction):
    """
    Sub class for backwards compatibility with existing workflow state
    actions.
    """
