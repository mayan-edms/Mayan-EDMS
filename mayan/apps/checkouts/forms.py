from __future__ import unicode_literals

from django import forms

from .models import DocumentCheckout
from .widgets import SplitTimeDeltaWidget


class DocumentCheckoutForm(forms.ModelForm):
    class Meta:
        fields = ('expiration_datetime', 'block_new_version')
        model = DocumentCheckout
        widgets = {
            'expiration_datetime': SplitTimeDeltaWidget()
        }
