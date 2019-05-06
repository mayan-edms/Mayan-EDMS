from __future__ import unicode_literals

import logging

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import RedirectView

from mayan.apps.common.generics import SimpleView, SingleObjectListView

from .forms import SearchForm, AdvancedSearchForm
from .icons import icon_search_submit
from .mixins import SearchModelMixin

logger = logging.getLogger(__name__)


class ResultsView(SearchModelMixin, SingleObjectListView):
    def get_extra_context(self):
        context = {
            'hide_links': True,
            'list_as_items': True,
            'no_results_icon': icon_search_submit,
            'no_results_text': _(
                'Try again using different terms. '
            ),
            'no_results_title': _('No search results'),
            'search_model': self.search_model,
            'title': _('Search results for: %s') % self.search_model.label,
        }

        return context

    def get_source_queryset(self):
        self.search_model = self.get_search_model()

        if self.request.GET:
            # Only do search if there is user input, otherwise just render
            # the template with the extra_context

            if self.request.GET.get('_match_all', 'off') == 'on':
                global_and_search = True
            else:
                global_and_search = False

            queryset = self.search_model.search(
                global_and_search=global_and_search,
                query_string=self.request.GET, user=self.request.user
            )

            return queryset


class SearchView(SearchModelMixin, SimpleView):
    template_name = 'appearance/generic_form.html'
    title = _('Search')

    def get_extra_context(self):
        self.search_model = self.get_search_model()
        return {
            'form': self.get_form(),
            'form_action': reverse(
                viewname='search:results', kwargs={
                    'search_model': self.search_model.get_full_name()
                }
            ),
            'search_model': self.search_model,
            'submit_icon_class': icon_search_submit,
            'submit_label': _('Search'),
            'submit_method': 'GET',
            'title': _('Search for: %s') % self.search_model.label,
        }

    def get_form(self):
        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            query_string = self.request.GET['q']
            return SearchForm(initial={'q': query_string})
        else:
            return SearchForm()


class AdvancedSearchView(SearchView):
    title = _('Advanced search')

    def get_form(self):
        return AdvancedSearchForm(
            data=self.request.GET, search_model=self.get_search_model()
        )


class SearchAgainView(RedirectView):
    pattern_name = 'search:search_advanced'
    query_string = True
