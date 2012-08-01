from __future__ import absolute_import

from django import forms

from .models import ClusteringConfig


class ClusteringConfigForm(forms.ModelForm):
    class Meta:
        model = ClusteringConfig
