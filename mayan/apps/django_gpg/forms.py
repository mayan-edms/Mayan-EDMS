from django import forms
from django.utils.translation import ugettext_lazy as _


class KeySearchForm(forms.Form):
    term = forms.CharField(
        label=_(u'Term'),
        help_text=_(u'Name, e-mail, key ID or key fingerprint to look for.')
    )
