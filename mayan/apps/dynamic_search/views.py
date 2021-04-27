import logging

from django.conf import settings
from django.contrib import messages
from django.template import RequestContext
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import RedirectView

from mayan.apps.views.generics import (
    ConfirmView, SimpleView, SingleObjectListView
)
from mayan.apps.views.literals import LIST_MODE_CHOICE_ITEM

from .classes import SearchBackend, SearchModel
from .exceptions import DynamicSearchException
from .forms import SearchForm, AdvancedSearchForm
from .icons import icon_search_submit
from .links import link_search_again
from .permissions import permission_search_tools
from .tasks import task_index_search_model
from .view_mixins import SearchModelViewMixin

logger = logging.getLogger(name=__name__)


class ResultsView(SearchModelViewMixin, SingleObjectListView):
    def get_extra_context(self):
        context = {
            'hide_object': True,
            'no_results_icon': icon_search_submit,
            'no_results_main_link': link_search_again.resolve(
                context=RequestContext(
                    request=self.request, dict_={
                        'search_model': self.search_model
                    }
                )
            ),
            'no_results_text': _(
                'Try again using different terms. '
            ),
            'no_results_title': _('No search results'),
            'search_model': self.search_model,
            'title': _('Search results for: %s') % self.search_model.label,
        }

        if self.search_model.list_mode == LIST_MODE_CHOICE_ITEM:
            context['list_as_items'] = True

        return context

    def get_source_queryset(self):
        if self.request.GET:
            # Only do search if there is user input, otherwise just render
            # the template with the extra_context

            if self.request.GET.get('_match_all', 'off') == 'on':
                global_and_search = True
            else:
                global_and_search = False

            try:
                queryset = SearchBackend.get_instance().search(
                    global_and_search=global_and_search,
                    search_model=self.search_model,
                    query_string=self.request.GET, user=self.request.user
                )
            except DynamicSearchException as exception:
                if settings.DEBUG or settings.TESTING:
                    raise

                messages.error(message=exception, request=self.request)
                return self.search_model.model._meta.default_manager.none()
            else:
                return queryset


class SearchAgainView(RedirectView):
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            self.pattern_name = 'search:search'
        else:
            self.pattern_name = 'search:search_advanced'

        return super().get_redirect_url(*args, **kwargs)


class SearchBackendReindexView(ConfirmView):
    extra_context = {
        'message': _(
            'This tool is required only for some search backends. '
            'Search results will be affected while the backend is '
            'being reindexed.'
        ),
        'title': _('Reindex search backend'),
        'subtitle': _(
            'This tool erases and populates the search backend\'s '
            'internal index.'
        ),
    }
    view_permission = permission_search_tools

    def get_post_action_redirect(self):
        return reverse(viewname='common:tools_list')

    def view_action(self):
        for search_model in SearchModel.all():
            task_index_search_model.apply_async(
                kwargs={
                    'search_model_full_name': search_model.get_full_name(),
                }
            )

        messages.success(
            message=_('Search backend reindexing queued.'),
            request=self.request
        )


class SearchView(SearchModelViewMixin, SimpleView):
    template_name = 'appearance/generic_form.html'
    title = _('Search')

    def get_extra_context(self):
        self.search_model = self.get_search_model()
        return {
            'form': self.get_form(),
            'form_action': reverse(
                viewname='search:results', kwargs={
                    'search_model_name': self.search_model.get_full_name()
                }
            ),
            'search_model': self.search_model,
            'submit_icon': icon_search_submit,
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
