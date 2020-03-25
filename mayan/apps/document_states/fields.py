from django import forms

from .widgets import WorkflowImageWidget


class WorfklowImageField(forms.fields.Field):
    widget = WorkflowImageWidget
