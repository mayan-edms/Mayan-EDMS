import logging

from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.django_gpg.models import Key
from mayan.apps.django_gpg.permissions import permission_key_sign
from mayan.apps.document_states.classes import WorkflowAction
from mayan.apps.document_states.exceptions import WorkflowStateActionError

from .models import DetachedSignature, EmbeddedSignature

logger = logging.getLogger(name=__name__)


class DocumentSignatureDetachedAction(WorkflowAction):
    fields = {
        'key': {
            'label': _('Key'),
            'class': 'django.forms.ModelChoiceField', 'kwargs': {
                'help_text': _(
                    'Private key that will be used to sign the document '
                    'version.'
                ), 'queryset': Key.objects.none(),
            },
        }, 'passphrase': {
            'label': _('Passphrase'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _(
                    'The passphrase to unlock the key and allow it to be '
                    'used to sign the document version.'
                ), 'required': False
            },
        },
    }
    field_order = ('key', 'passphrase')
    label = _('Sign document (detached)')
    widgets = {
        'passphrase': {
            'class': 'django.forms.widgets.PasswordInput',
        }
    }

    def get_arguments(self, context):
        latest_version = context['document'].latest_version
        if not latest_version:
            raise WorkflowStateActionError(
                _(
                    'Document has no version to sign. You might be trying to '
                    'use this action in an initial state before the created '
                    'document is yet to be processed.'
                )
            )

        return {
            'document_version': latest_version,
            'key': Key.objects.get(pk=self.form_data['key']),
            'passphrase': self.form_data.get('passphrase')
        }

    def get_form_schema(self, request):
        user = request.user
        logger.debug('user: %s', user)

        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_key_sign, queryset=Key.objects.all(),
            user=user
        )

        self.fields['key']['kwargs']['queryset'] = queryset
        return super(DocumentSignatureDetachedAction, self).get_form_schema(
            request=request
        )

    def execute(self, context):
        DetachedSignature.objects.sign_document_version(
            **self.get_arguments(context=context)
        )


class DocumentSignatureEmbeddedAction(DocumentSignatureDetachedAction):
    label = _('Sign document (embedded)')

    def execute(self, context):
        EmbeddedSignature.objects.sign_document_version(
            **self.get_arguments(context=context)
        )
