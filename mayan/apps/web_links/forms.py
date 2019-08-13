from __future__ import unicode_literals

from django import forms

from .models import WebLink


class WebLinkForm(forms.ModelForm):
    class Meta:
        fields = ('label', 'template', 'enabled')
        model = WebLink
