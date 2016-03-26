from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from common.forms import DetailForm
from django_gpg.models import Key

from .models import SignatureBaseModel


class DetachedSignatureForm(forms.Form):
    file = forms.FileField(
        label=_('Signature file'),
    )


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
        super(DocumentVersionSignatureDetailForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ()
        model = SignatureBaseModel
