from __future__ import unicode_literals

import logging
import urlparse

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from common.generics import SimpleView, SingleObjectListView

from .classes import SearchModel
from .forms import SearchForm, AdvancedSearchForm
from .settings import setting_limit, setting_show_object_type

logger = logging.getLogger(__name__)


class ResultsView(SingleObjectListView):
    def get_extra_context(self):
        context = {
            'hide_links': True,
            'search_results_limit': setting_limit.value,
            'title': _('Search results'),
        }

        if setting_show_object_type.value:
            context.update({
                'extra_columns': (
                    {
                        'name': _('Type'),
                        'attribute': lambda x: x._meta.verbose_name[0].upper() + x._meta.verbose_name[1:]
                    },
                )
            })

        return context

    def get_queryset(self):
        document_search = SearchModel.get('documents.Document')

        if self.request.GET:
            # Only do search if there is user input, otherwise just render
            # the template with the extra_context

            queryset, ids, timedelta = document_search.search(
                self.request.GET, self.request.user
            )

            return queryset


class SearchView(SimpleView):
    template_name = 'appearance/generic_form.html'
    title = _('Search')

    def get_form(self):
        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            query_string = self.request.GET['q']
            return SearchForm(initial={'q': query_string})
        else:
            return SearchForm()

    def get_extra_context(self):
        return {
            'form': self.get_form(),
            'form_action': reverse('search:results'),
            'submit_icon': 'fa fa-search',
            'submit_label': _('Search'),
            'submit_method': 'GET',
            'title': self.title,
        }


class AdvancedSearchView(SearchView):
    title = _('Advanced search')

    def get_form(self):
        document_search = SearchModel.get('documents.Document')

        return AdvancedSearchForm(
            data=self.request.GET, search_model=document_search
        )


def search_again(request):
    query = urlparse.urlparse(
        request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))
    ).query
    return HttpResponseRedirect(
        '{}?{}'.format(reverse('search:search_advanced'), query)
    )
