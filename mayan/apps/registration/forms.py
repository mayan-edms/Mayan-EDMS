from __future__ import unicode_literals

import logging

from django import forms
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


class RegistrationForm(forms.Form):
    name = forms.CharField(
        label=_('Your name:'),
        required=True
    )

    email = forms.CharField(
        label=_('Your email:'),
        required=True
    )

    company = forms.CharField(
        label=_('Company name:'),
        required=False
    )

    industry = forms.CharField(
        label=_('Industry:'),
        required=False
    )

    website = forms.CharField(
        label=_('Company website:'),
        required=False
    )

    country = forms.CharField(
        label=_('Country:'),
        required=False
    )

    other = forms.CharField(
        widget=forms.widgets.Textarea(
            attrs={'rows': 2},
        ),
        label=_('Other information:'),
        required=False
    )
