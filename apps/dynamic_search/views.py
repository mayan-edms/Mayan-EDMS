from __future__ import absolute_import

import urlparse
import logging

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.http import urlencode

from .conf.settings import SHOW_OBJECT_TYPE
from .conf.settings import LIMIT
from .forms import SearchForm, AdvancedSearchForm
from .models import RecentSearch
from .classes import SearchModel

logger = logging.getLogger(__name__)
document_search = SearchModel.get('documents.Document')


def results(request, extra_context=None):
    context = {
        'query_string': request.GET,
        #'hide_header': True,
        'hide_links': True,
        'multi_select_as_buttons': True,
        'search_results_limit': LIMIT,
    }

    if request.GET:
        # Only do search if there is user input, otherwise just render
        # the template with the extra_context

        if 'q' in request.GET:
            # Simple query
            logger.debug('simple search')
            query_string = request.GET.get('q', u'').strip()
            model_list, flat_list, shown_result_count, result_count, elapsed_time = document_search.simple_search(query_string)
        else:
            # Advanced search
            logger.debug('advanced search')
            model_list, flat_list, shown_result_count, result_count, elapsed_time = document_search.advanced_search(request.GET)
            
        if shown_result_count != result_count:
            title = _(u'results, (showing only %(shown_result_count)s out of %(result_count)s)') % {
                'shown_result_count': shown_result_count,
                'result_count': result_count}
                
        else:
            title = _(u'results')
        
        # Update the context with the search results
        context.update({
            'found_entries': model_list,
            'object_list': flat_list,
            'title': title,
            'time_delta': elapsed_time,
        })            

        RecentSearch.objects.add_query_for_user(request.user, request.GET, result_count)

    if extra_context:
        context.update(extra_context)

    if SHOW_OBJECT_TYPE:
        context.update({'extra_columns':
            [{'name': _(u'type'), 'attribute': lambda x: x._meta.verbose_name[0].upper() + x._meta.verbose_name[1:]}]})

    return render_to_response('search_results.html', context,
                          context_instance=RequestContext(request))


def search(request, advanced=False):
    if advanced:
        form = AdvancedSearchForm(data=request.GET, search_model=document_search)
        return render_to_response('generic_form.html',
            {
                'form': form,
                'title': _(u'advanced search'),
                'form_action': reverse('results'),
                'submit_method': 'GET',
                'search_results_limit': LIMIT,
                'submit_label': _(u'Search'),
                'submit_icon_famfam': 'zoom',
            },
            context_instance=RequestContext(request)
        )
    else:
        if request.GET.get('source') != 'sidebar':
            # Don't include a form a top of the results if the search
            # was originated from the sidebar search form
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
        else:
            # Already has a form with data, go to results
            return results(request)


def search_again(request):
    query = urlparse.urlparse(request.META.get('HTTP_REFERER', u'/')).query
    return HttpResponseRedirect('%s?%s' % (reverse('search_advanced'), query))
