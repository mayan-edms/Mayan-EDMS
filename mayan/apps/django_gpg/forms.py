from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _


class KeySearchForm(forms.Form):
    term = forms.CharField(
        label=_('Term'),
        help_text=_('Name, e-mail, key ID or key fingerprint to look for.')
    )
