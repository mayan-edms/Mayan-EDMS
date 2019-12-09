from __future__ import absolute_import, unicode_literals

from django import forms

from .widgets import WorkflowImageWidget


class WorfklowImageField(forms.fields.Field):
    widget = WorkflowImageWidget
