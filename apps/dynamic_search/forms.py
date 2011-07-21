from django import forms
from django.utils.translation import ugettext_lazy as _

from dynamic_search.api import registered_search_dict


class SearchForm(forms.Form):
    q = forms.CharField(max_length=128, label=_(u'Search terms'))
    source = forms.CharField(
        max_length=32,
        required=False,
        widget=forms.widgets.HiddenInput()
    )


class AdvancedSearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AdvancedSearchForm, self).__init__(*args, **kwargs)

        for model_name, values in registered_search_dict.items():
            for field in values['fields']:
                self.fields['%s__%s' % (model_name, field['name'])] = forms.CharField(
                    label=field['title'],
                    required=False
                )
