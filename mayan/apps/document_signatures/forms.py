from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _


class DetachedSignatureForm(forms.Form):
    file = forms.FileField(
        label=_('Signature file'),
    )
