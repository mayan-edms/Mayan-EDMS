from __future__ import absolute_import

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import DocumentCheckout


class DocumentCheckoutForm(forms.ModelForm):
    days = forms.IntegerField(min_value=0, label=_(u'Days'), help_text=_(u'Amount of time to hold the document checked out in days.'), required=False, widget=forms.widgets.TextInput(attrs={'maxlength': 3, 'style':'width: 10em;'}))
    hours = forms.IntegerField(min_value=0, label=_(u'Hours'), help_text=_(u'Amount of time to hold the document checked out in hours.'), required=False, widget=forms.widgets.TextInput(attrs={'maxlength': 3, 'style':'width: 10em;'}))
    minutes = forms.IntegerField(min_value=0, label=_(u'Minutes'), help_text=_(u'Amount of time to hold the document checked out in minutes.'), required=False, widget=forms.widgets.TextInput(attrs={'maxlength': 3, 'style':'width: 10em;'}))

    class Meta:
        model = DocumentCheckout
        exclude = ('expiration_datetime', )
        #fields = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'last_login', 'date_joined', 'groups')

    #def clean(self):
        
        
