from __future__ import absolute_import

import logging
import urlparse

from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessEntry
from permissions.models import Permission

from .classes import SearchModel
from .forms import SearchForm, AdvancedSearchForm
from .models import RecentSearch
from .settings import LIMIT, SHOW_OBJECT_TYPE

logger = logging.getLogger(__name__)
document_search = SearchModel.get('documents.Document')


def results(request, extra_context=None):
    context = {
        'query_string': request.GET,
        'hide_links': True,
        'search_results_limit': LIMIT,
    }

    if request.GET:
        # Only do search if there is user input, otherwise just render
        # the template with the extra_context

        if 'q' in request.GET:
            # Simple query
            logger.debug('simple search')
            query_string = request.GET.get('q', u'').strip()
            queryset, ids, timedelta = document_search.simple_search(query_string)
        else:
            # Advanced search
            logger.debug('advanced search')
            queryset, ids, timedelta = document_search.advanced_search(request.GET)

        if document_search.permission:
            try:
                Permission.objects.check_permissions(request.user, [document_search.permission])
            except PermissionDenied:
                queryset = AccessEntry.objects.filter_objects_by_access(document_search.permission, request.user, queryset)

        # Update the context with the search results
        context.update({
            'object_list': queryset,
            'time_delta': timedelta,
            'title': _(u'Results'),
        })

        RecentSearch.objects.add_query_for_user(request.user, request.GET, len(ids))

    if extra_context:
        context.update(extra_context)

    if SHOW_OBJECT_TYPE:
        context.update({
            'extra_columns': [{'name': _(u'Type'), 'attribute': lambda x: x._meta.verbose_name[0].upper() + x._meta.verbose_name[1:]}]
        })

    return render_to_response('search_results.html', context,
                              context_instance=RequestContext(request))


def search(request, advanced=False):
    if advanced:
        form = AdvancedSearchForm(data=request.GET, search_model=document_search)
        return render_to_response(
            'main/generic_form.html',
            {
                'form': form,
                'title': _(u'Advanced search'),
                'form_action': reverse('search:results'),
                'submit_method': 'GET',
                'search_results_limit': LIMIT,
                'submit_label': _(u'Search'),
                'submit_icon_famfam': 'zoom',
            }, context_instance=RequestContext(request)
        )
    else:
        extra_context = {
            'submit_label': _(u'Search'),
            'submit_icon_famfam': 'zoom',
            'form_title': _(u'Search'),
            'form_hide_required_text': True,
        }
        if ('q' in request.GET) and request.GET['q'].strip():
            query_string = request.GET['q']
            form = SearchForm(initial={'q': query_string})
            extra_context.update({'form': form})
            return results(request, extra_context=extra_context)
        else:
            form = SearchForm()
            extra_context.update({'form': form})
            return results(request, extra_context=extra_context)


def search_again(request):
    query = urlparse.urlparse(request.META.get('HTTP_REFERER', reverse('main:home'))).query
    return HttpResponseRedirect('%s?%s' % (reverse('search:search_advanced'), query))
