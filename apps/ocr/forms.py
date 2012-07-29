"""
from __future__ import absolute_import

from django import forms

from .models import QueueTransformation


class QueueTransformationForm(forms.ModelForm):
    class Meta:
        model = QueueTransformation

    def __init__(self, *args, **kwargs):
        super(QueueTransformationForm, self).__init__(*args, **kwargs)
        self.fields['content_type'].widget = forms.HiddenInput()
        self.fields['object_id'].widget = forms.HiddenInput()


class QueueTransformationForm_create(forms.ModelForm):
    class Meta:
        model = QueueTransformation
        exclude = ('content_type', 'object_id')
"""
