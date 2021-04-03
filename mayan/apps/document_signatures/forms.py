import logging

from django import forms
from django.utils.translation import ugettext_lazy as _

from mayan.apps.django_gpg.models import Key
from mayan.apps.django_gpg.permissions import permission_key_sign
from mayan.apps.views.forms import DetailForm, FilteredSelectionForm

from .models import SignatureBaseModel

logger = logging.getLogger(name=__name__)


class DocumentFileSignatureCreateForm(FilteredSelectionForm):
    key = forms.ModelChoiceField(
        label=_('Key'), queryset=Key.objects.none()
    )

    passphrase = forms.CharField(
        help_text=_(
            'The passphrase to unlock the key and allow it to be used to '
            'sign the document file.'
        ), label=_('Passphrase'), required=False,
        widget=forms.widgets.PasswordInput
    )

    class Meta:
        allow_multiple = False
        field_name = 'key'
        label = _('Key')
        help_text = _(
            'Private key that will be used to sign this document file.'
        )
        permission = permission_key_sign
        queryset = Key.objects.private_keys()
        required = True
        widget_attributes = {'class': 'select2'}


class DocumentFileSignatureDetailForm(DetailForm):
    def __init__(self, *args, **kwargs):
        extra_fields = (
            {'label': _('Signature is embedded?'), 'field': 'is_embedded'},
            {
                'label': _('Signature date'), 'field': 'date_time',
                'widget': forms.widgets.DateTimeInput
            },
            {'label': _('Signature key ID'), 'field': 'key_id'},
            {
                'label': _('Signature key present?'),
                'field': lambda x: x.public_key_fingerprint is not None
            },
        )

        key = kwargs['instance'].key

        if key:
            extra_fields += (
                {'label': _('Signature ID'), 'field': 'signature_id'},
                {
                    'label': _('Key fingerprint'),
                    'field': lambda x: key.fingerprint
                },
                {
                    'label': _('Key creation date'),
                    'field': 'key_creation_date',
                    'widget': forms.widgets.DateTimeInput
                },
                {
                    'label': _('Key expiration date'),
                    'field': lambda x: key.expiration_date or _('None'),
                    'widget': forms.widgets.DateTimeInput
                },
                {
                    'label': _('Key length'),
                    'field': 'key_length'
                },
                {
                    'label': _('Key algorithm'),
                    'field': 'key_algorithm'
                },
                {
                    'label': _('Key user ID'),
                    'field': 'key_user_id'
                },
                {
                    'label': _('Key type'),
                    'field': lambda x: key.get_key_type_display()
                },
            )

        kwargs['extra_fields'] = extra_fields
        super().__init__(*args, **kwargs)

    class Meta:
        fields = ()
        model = SignatureBaseModel
