from __future__ import absolute_import, unicode_literals

import logging

from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.django_gpg.models import Key
from mayan.apps.django_gpg.permissions import permission_key_sign
from mayan.apps.document_states.classes import WorkflowAction

from .models import DetachedSignature, EmbeddedSignature

logger = logging.getLogger(__name__)


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
            document_version=context['document'].latest_version,
            key=self.form_data['key'],
            passphrase=self.form_data.get('passphrase'),
        )


class DocumentSignatureEmbeddedAction(DocumentSignatureDetachedAction):
    label = _('Sign document (embedded)')

    def execute(self, context):
        EmbeddedSignature.objects.sign_document_version(
            document_version=context['document'].latest_version,
            key=self.form_data['key'],
            passphrase=self.form_data.get('passphrase'),
        )
