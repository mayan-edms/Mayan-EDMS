from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Redaction


class RedactionCoordinatesForm(forms.ModelForm):
    class Meta:
        fields = ('arguments',)
        model = Redaction
        widgets = {
            'arguments': forms.widgets.Textarea(attrs={'class': 'hidden'}),
        }
