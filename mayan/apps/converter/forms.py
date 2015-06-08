from __future__ import unicode_literals

from django import forms

from .models import Transformation


class TransformationForm(forms.ModelForm):
    class Meta:
        fields = ('order', 'name', 'arguments')
        model = Transformation
