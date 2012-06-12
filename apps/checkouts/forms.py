from __future__ import absolute_import

import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import DocumentCheckout


class DocumentCheckoutForm(forms.ModelForm):
    days = forms.IntegerField(min_value=0, label=_(u'Days'), help_text=_(u'Amount of time to hold the document checked out in days.'), required=False, widget=forms.widgets.TextInput(attrs={'maxlength': 3, 'style':'width: 5em;'}))
    hours = forms.IntegerField(min_value=0, label=_(u'Hours'), help_text=_(u'Amount of time to hold the document checked out in hours.'), required=False, widget=forms.widgets.TextInput(attrs={'maxlength': 4, 'style':'width: 5em;'}))
    minutes = forms.IntegerField(min_value=0, label=_(u'Minutes'), help_text=_(u'Amount of time to hold the document checked out in minutes.'), required=False, widget=forms.widgets.TextInput(attrs={'maxlength': 5, 'style':'width: 5em;'}))

    class Meta:
        model = DocumentCheckout
        exclude = ('expiration_datetime', 'document')

    def clean_expiration_datetime(self):
        data = self.cleaned_data['expiration_datetime']
        timedelta = datetime.timedelta(days=self.cleaned_data['days'], hours=self.cleaned_data['hours'], minutes=self.cleaned_data['minutes'])
        return datetime.datetime.now() + timedelta
        
        
