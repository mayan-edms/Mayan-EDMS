from __future__ import absolute_import

import logging

from django import forms
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


class RegistrationForm(forms.Form):
    name = forms.CharField(
        label=_(u'Your name:'),
        required=True
    )

    email = forms.CharField(
        label=_(u'Your email:'),
        required=True
    )

    company = forms.CharField(
        label=_(u'Company name:'),
        required=False
    )

    industry = forms.CharField(
        label=_(u'Industry:'),
        required=False
    )

    website = forms.CharField(
        label=_(u'Company website:'),
        required=False
    )

    country = forms.CharField(
        label=_(u'Country:'),
        required=False
    )

    other = forms.CharField(
        widget=forms.widgets.Textarea(
            attrs={'rows': 2},
        ),
        label=_(u'Other information:'),
        required=False
    )
