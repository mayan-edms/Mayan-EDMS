from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.conf import settings

from dynamic_search.api import perform_search, registered_search_dict
from dynamic_search.forms import SearchForm, AdvancedSearchForm
from dynamic_search.conf.settings import SHOW_OBJECT_TYPE
from dynamic_search.conf.settings import LIMIT


def results(request, extra_context=None):
    query_string = ''
    context = {}

    context.update({
        'query_string': request.GET,
        'form_title': _(u'Search'),
        #'hide_header': True,
        'form_hide_required_text': True,
        'hide_links': True,
        'multi_select_as_buttons': True,
        'submit_label': _(u'Search'),
        'submit_icon_famfam': 'zoom',
        'search_results_limit': LIMIT,
    })
    
    if extra_context:
        context.update(extra_context)

    try:
        response = perform_search(request.GET)
        if response['shown_result_count'] != response['result_count']:
            title = _(u'results, (showing only %(shown_result_count)s out of %(result_count)s)') % {
                'shown_result_count': response['shown_result_count'],
                'result_count': response['result_count']}
        else:
            title = _(u'results')
        context.update({
            'found_entries': response['model_list'],
            'object_list': response['flat_list'],
            'title': title,
            'time_delta': response['elapsed_time'],
        })

    except Exception, e:
        if settings.DEBUG:
            raise
        elif request.user.is_staff or request.user.is_superuser:
            messages.error(request, _(u'Search error: %s') % e)

    if SHOW_OBJECT_TYPE:
        context.update({'extra_columns':
            [{'name': _(u'type'), 'attribute': lambda x: x._meta.verbose_name[0].upper() + x._meta.verbose_name[1:]}]})

    return render_to_response('search_results.html', context,
                          context_instance=RequestContext(request))


def search(request, advanced=False):
    if advanced:
        search_fields = []
        for model_name, values in registered_search_dict.items():
            for field in values['fields']:
                search_fields.append(
                    {
                        'title': field['title'],
                        'name': '%s__%s' % (model_name, field['name'])
                    }
                )
        form = AdvancedSearchForm(
            search_fields=search_fields,
            data=request.GET
        )

        return results(request, extra_context={
                'form': form,
                'form_title': _(u'advanced search')
            }
        )
    else:
        if ('q' in request.GET) and request.GET['q'].strip():
            query_string = request.GET['q']
            form = SearchForm(initial={'q': query_string})
            return results(request, extra_context={
                    'form': form
                }
            )
        else:
            form = SearchForm()
            return results(request, extra_context={
                    'form': form
                }
            )
