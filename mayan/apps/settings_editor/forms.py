from __future__ import absolute_import

import logging

from django import forms
#from django.utils.translation import ugettext_lazy as _

#from common.forms import DetailForm

logger = logging.getLogger(__name__)


class SettingsForm(forms.Form):
    content = forms.CharField(widget=forms.widgets.Textarea(attrs={'rows': 5, 'cols': 80}))
