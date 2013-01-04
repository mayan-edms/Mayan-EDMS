from __future__ import absolute_import

from django import forms
from django.utils.translation import ugettext_lazy as _


class SearchForm(forms.Form):
    q = forms.CharField(max_length=128, label=_(u'Search terms'))
    source = forms.CharField(
        max_length=32,
        required=False,
        widget=forms.widgets.HiddenInput()
    )


class AdvancedSearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.search_model = kwargs.pop('search_model')
        super(AdvancedSearchForm, self).__init__(*args, **kwargs)

        for name, label in self.search_model.get_fields_simple_list():
            self.fields[name] = forms.CharField(
                label=label,
                required=False
            )
