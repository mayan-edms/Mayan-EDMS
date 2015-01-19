from __future__ import unicode_literals

from django import forms

from .models import DocumentCheckout
from .widgets import SplitTimeDeltaField


class DocumentCheckoutForm(forms.ModelForm):
    expiration_datetime = SplitTimeDeltaField()

    class Meta:
        model = DocumentCheckout
        exclude = ('document', 'checkout_datetime', 'user_content_type', 'user_object_id')
