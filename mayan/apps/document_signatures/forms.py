from __future__ import absolute_import, unicode_literals

import logging

from django import forms
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.forms import DetailForm, FilteredSelectionForm
from mayan.apps.django_gpg.models import Key
from mayan.apps.django_gpg.permissions import permission_key_sign

from .models import SignatureBaseModel

logger = logging.getLogger(name=__name__)


class DocumentVersionSignatureCreateForm(FilteredSelectionForm):
    key = forms.ModelChoiceField(
        label=_('Key'), queryset=Key.objects.none()
    )

    passphrase = forms.CharField(
        help_text=_(
            'The passphrase to unlock the key and allow it to be used to '
            'sign the document version.'
        ), label=_('Passphrase'), required=False,
        widget=forms.widgets.PasswordInput
    )

    class Meta:
        allow_multiple = False
        field_name = 'key'
        label = _('Key')
        help_text = _(
            'Private key that will be used to sign this document version.'
        )
        permission = permission_key_sign
        queryset = Key.objects.private_keys()
        required = True
        widget_attributes = {'class': 'select2'}


class DocumentVersionSignatureDetailForm(DetailForm):
    def __init__(self, *args, **kwargs):
        extra_fields = (
            {'label': _('Signature is embedded?'), 'field': 'is_embedded'},
            {
                'label': _('Signature date'), 'field': 'date',
                'widget': forms.widgets.DateInput
            },
            {'label': _('Signature key ID'), 'field': 'key_id'},
            {
                'label': _('Signature key present?'),
                'field': lambda x: x.public_key_fingerprint is not None
            },
        )

        if kwargs['instance'].public_key_fingerprint:
            key = Key.objects.get(
                fingerprint=kwargs['instance'].public_key_fingerprint
            )

            extra_fields += (
                {'label': _('Signature ID'), 'field': 'signature_id'},
                {
                    'label': _('Key fingerprint'),
                    'field': lambda x: key.fingerprint
                },
                {
                    'label': _('Key creation date'),
                    'field': lambda x: key.creation_date,
                    'widget': forms.widgets.DateInput
                },
                {
                    'label': _('Key expiration date'),
                    'field': lambda x: key.expiration_date or _('None'),
                    'widget': forms.widgets.DateInput
                },
                {
                    'label': _('Key length'),
                    'field': lambda x: key.length
                },
                {
                    'label': _('Key algorithm'),
                    'field': lambda x: key.algorithm
                },
                {
                    'label': _('Key user ID'),
                    'field': lambda x: key.user_id
                },
                {
                    'label': _('Key type'),
                    'field': lambda x: key.get_key_type_display()
                },
            )

        kwargs['extra_fields'] = extra_fields
        super(
            DocumentVersionSignatureDetailForm, self
        ).__init__(*args, **kwargs)

    class Meta:
        fields = ()
        model = SignatureBaseModel
