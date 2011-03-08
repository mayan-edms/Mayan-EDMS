import datetime
import re

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.db.models import Q
from django.contrib import messages
from django.core.exceptions import FieldError


from api import search_list
from forms import SearchForm
from conf.settings import SHOW_OBJECT_TYPE, LIMIT

#original code from:
#http://www.julienphalip.com/blog/2008/08/16/adding-search-django-site-snap/

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(terms, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    queries = []
    for term in terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{'%s__icontains' % field_name:term})        
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
            
        queries.append(or_query)
    return queries

def search(request):
    query_string = ''
    found_entries = {}
    object_list = []

    start_time = datetime.datetime.now()
    
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        form = SearchForm(initial={'q':query_string})
        
        terms = normalize_query(query_string)
        
        for model, data in search_list.items():
            queries = get_query(terms, data['fields'])

            try:
                model_results = None
                for query in queries:
                    single_results = set(model.objects.filter(query).values_list('pk', flat=True))
                    #Convert queryset to python set and perform the 
                    #AND operation on the program and not as a query
                    if model_results == None:
                        model_results = single_results
                    else:
                        model_results &= single_results
                    
                    results = model.objects.filter(pk__in=model_results)[:LIMIT]
                if results:
                    found_entries[data['text']] = results
                    for result in results:
                        if result not in object_list:
                            object_list.append(result)
            except FieldError, e:
                if request.user.is_staff or request.user.is_superuser:
                    messages.error(request, _(u'Search error: %s') % e)
    else:
        form = SearchForm()
    
    if LIMIT and len(model_results) > LIMIT:
        title = _(u'results with: %s (showing only %s out of %s)') % (query_string, LIMIT, len(model_results))
    else:
        title = _(u'results with: %s') % query_string
    
    context = {
        'query_string':query_string, 
        'found_entries':found_entries,
        'form':form,
        'object_list':object_list,
        'form_title':_(u'Search'),
        'hide_header':True,
        'title':title,
        'time_delta':str(datetime.datetime.now() - start_time).split(':')[2]
    }

    if SHOW_OBJECT_TYPE:
        context.update({'extra_columns':
            [{'name':_(u'type'), 'attribute':lambda x:x._meta.verbose_name[0].upper() + x._meta.verbose_name[1:]}]})
        
    return render_to_response('search_results.html', context,
                          context_instance=RequestContext(request))
