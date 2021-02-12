from django import forms

from .widgets import AssetImageWidget


class AssetImageField(forms.fields.Field):
    widget = AssetImageWidget
