from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.conf import settings


from api import perform_search
from forms import SearchForm
from conf.settings import SHOW_OBJECT_TYPE


def results(request, form=None):
    query_string = ''
    context = {}
        
    result_count = 0
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        try:
            model_list, flat_list, shown_result_count, total_result_count, elapsed_time = perform_search(query_string)
            if shown_result_count != total_result_count:
                title = _(u'results with: %(query_string)s (showing only %(shown_result_count)s out of %(total_result_count)s)') % {
                    'query_string':query_string, 'shown_result_count':shown_result_count,
                    'total_result_count':total_result_count}
            else:
                title = _(u'results with: %s') % query_string
            context.update({
                'found_entries': model_list,
                'object_list':flat_list,
                'title':title,
                'time_delta':elapsed_time,
            })
                
        except Exception, e:
            if settings.DEBUG:
                raise
            elif request.user.is_staff or request.user.is_superuser:
                messages.error(request, _(u'Search error: %s') % e)

    context.update({
        'query_string':query_string, 
        'form':form,
        'form_title':_(u'Search'),
        'hide_header':True,
        'form_hide_required_text':True,
    })

    if SHOW_OBJECT_TYPE:
        context.update({'extra_columns':
            [{'name':_(u'type'), 'attribute':lambda x:x._meta.verbose_name[0].upper() + x._meta.verbose_name[1:]}]})
        
    return render_to_response('search_results.html', context,
                          context_instance=RequestContext(request))
                          
                          
                          
def search(request):
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        form = SearchForm(initial={'q':query_string})
        return results(request, form=form)
    else:
        form = SearchForm()
        return results(request, form=form)
"""
def search(request):
    query_string = ''
    context = {}
        
    result_count = 0
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        form = SearchForm(initial={'q':query_string})
        try:
            model_list, flat_list, shown_result_count, total_result_count, elapsed_time = perform_search(query_string)
            if shown_result_count != total_result_count:
                title = _(u'results with: %s (showing only %s out of %s)') % (query_string, shown_result_count, total_result_count)
            else:
                title = _(u'results with: %s') % query_string
            context.update({
                'found_entries': model_list,
                'object_list':flat_list,
                'title':title,
                'time_delta':elapsed_time,
            })
                
        except Exception, e:
            if settings.DEBUG:
                raise
            elif request.user.is_staff or request.user.is_superuser:
                messages.error(request, _(u'Search error: %s') % e)
    else:
        form = SearchForm()
   
    context.update({
        'query_string':query_string, 
        'form':form,
        'form_title':_(u'Search'),
        'hide_header':True,
    })

    if SHOW_OBJECT_TYPE:
        context.update({'extra_columns':
            [{'name':_(u'type'), 'attribute':lambda x:x._meta.verbose_name[0].upper() + x._meta.verbose_name[1:]}]})
        
    return render_to_response('search_results.html', context,
                          context_instance=RequestContext(request))
"""
