from __future__ import absolute_import

from django import forms
from django.utils.translation import ugettext_lazy as _

from haystack.forms import SearchForm

from .api import registered_search_dict


class AdvancedSearchForm(SearchForm):
    def __init__(self, *args, **kwargs):
        super(AdvancedSearchForm, self).__init__(*args, **kwargs)

        for model_name, values in registered_search_dict.items():
            for field in values['fields']:
                self.fields['%s__%s' % (model_name, field['name'])] = forms.CharField(
                    label=field['title'],
                    required=False
                )

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        #if not self.cleaned_data.get('q'):
        #    return self.no_query_found()
        for field in self.fields:
            print 'field', field
        #sqs = self.searchqueryset.auto_query(self.cleaned_data['q'])

        if self.load_all:
            sqs = sqs.load_all()

        return sqs

    def search(self):
        sqs = super(ModelSearchForm, self).search()
        return sqs.models(*self.get_models())
