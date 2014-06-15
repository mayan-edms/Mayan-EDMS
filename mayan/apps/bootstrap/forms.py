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
        widgets = {
            'description': forms.widgets.Textarea(attrs={
                'rows': 5, 'cols': 80,
                }
            )
        }


class BootstrapSetupForm_view(DetailForm):
    class Meta:
        model = BootstrapSetup
        widgets = {
            'description': forms.widgets.Textarea(attrs={
                'rows': 5, 'cols': 80,
                }
            )
        }

class BootstrapSetupForm_edit(BootstrapSetupForm):
    class Meta(BootstrapSetupForm.Meta):
        model = BootstrapSetup
        exclude = ('type',)


class BootstrapSetupForm_dump(BootstrapSetupForm):
    class Meta(BootstrapSetupForm.Meta):
        model = BootstrapSetup
        exclude = ('fixture',)


class BootstrapFileImportForm(forms.Form):
    file = forms.FileField(
        label=_(u'Bootstrap setup file'),
    )


class BootstrapURLImportForm(forms.Form):
    url = forms.URLField(
        label=_(u'Bootstrap setup URL'),
    )
