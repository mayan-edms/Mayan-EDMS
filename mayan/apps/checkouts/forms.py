from __future__ import unicode_literals

from django import forms

from .models import DocumentCheckout
from .widgets import SplitTimeDeltaWidget


class DocumentCheckoutForm(forms.ModelForm):
    class Meta:
        model = DocumentCheckout
        exclude = ('document', 'checkout_datetime', 'user')
        widgets = {
            'expiration_datetime': SplitTimeDeltaWidget()
        }
