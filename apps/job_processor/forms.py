from __future__ import absolute_import

from django import forms

from .models import JobProcessingConfig


class JobProcessingConfigForm(forms.ModelForm):
    class Meta:
        model = JobProcessingConfig
