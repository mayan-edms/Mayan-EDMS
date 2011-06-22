from django import forms
from django.utils.translation import ugettext_lazy as _


class SearchForm(forms.Form):
    q = forms.CharField(max_length=128, label=_(u'Search terms'))


class AdvancedSearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        search_fields = kwargs.pop('search_fields')
        super(AdvancedSearchForm, self).__init__(*args, **kwargs)

        #Set form fields initial values
        for search_field in search_fields:
            self.fields[search_field['name']] = forms.CharField(
                label=search_field['title'],
                required=False
            )
