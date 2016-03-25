from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from common.forms import DetailForm

from .models import SignatureBaseModel


class DetachedSignatureForm(forms.Form):
    file = forms.FileField(
        label=_('Signature file'),
    )


class DocumentVersionSignatureDetailForm(DetailForm):
    def __init__(self, *args, **kwargs):
        extra_fields = (
            {'label': _('Is embedded?'), 'field': 'is_embedded'},
            {'label': _('Date'), 'field': 'date'},
            {'label': _('Key ID'), 'field': 'key_id'},
        )

        kwargs['extra_fields'] = extra_fields
        super(DocumentVersionSignatureDetailForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ()
        model = SignatureBaseModel


"""
{
    'label': _('User ID'),
    'field': lambda x: escape(instance.user_id),
},
{
    'label': _('Creation date'), 'field': 'creation_date',
    'widget': forms.widgets.DateInput
},
{
    'label': _('Expiration date'),
    'field': lambda x: instance.expiration_date or _('None'),
    'widget': forms.widgets.DateInput
},
{'label': _('Fingerprint'), 'field': 'fingerprint'},
{'label': _('Length'), 'field': 'length'},
{'label': _('Algorithm'), 'field': 'algorithm'},
{'label': _('Type'), 'field': lambda x: instance.get_key_type_display()},
"""
