from __future__ import absolute_import, unicode_literals

from django import forms

from .widgets import TemplateWidget


class TemplateField(forms.CharField):
    widget = TemplateWidget

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model')
        self.model_variable = kwargs.pop('model_variable')
        super(TemplateField, self).__init__(*args, **kwargs)
