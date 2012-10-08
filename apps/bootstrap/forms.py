from __future__ import absolute_import

import logging

from django import forms
from django.utils.translation import ugettext_lazy as _

from common.forms import DetailForm

from .models import BootstrapSetup

logger = logging.getLogger(__name__)


class BootstrapSetupForm(forms.ModelForm):
    class Meta:
        model = BootstrapSetup


class BootstrapSetupForm_view(DetailForm):
    class Meta:
        model = BootstrapSetup


class BootstrapSetupForm_edit(forms.ModelForm):
    class Meta:
        model = BootstrapSetup
        exclude = ('type',)


class BootstrapSetupForm_dump(forms.ModelForm):
    class Meta:
        model = BootstrapSetup
        exclude = ['fixture']
