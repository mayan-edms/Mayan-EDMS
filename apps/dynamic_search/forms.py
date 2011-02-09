from django import forms 
from django.utils.translation import ugettext_lazy as _


class SearchForm(forms.Form):
    q = forms.CharField(max_length=128, label=_(u'Search term'))
    
