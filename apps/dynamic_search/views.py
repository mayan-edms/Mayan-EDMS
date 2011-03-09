import datetime
import re
import types

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.db.models import Q
from django.contrib import messages
from django.core.exceptions import FieldError
from django.conf import settings


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


def get_query(query_string, terms, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    """
    queries = []
    for term in terms:
        or_query = None
        for field in search_fields:
            if isinstance(field, types.StringTypes):
                comparison = u'icontains'
                field_name = field
            elif isinstance(field, types.DictType):
                comparison = field.get('comparison', u'icontains')
                field_name = field.get('field_name', '')
            
            if field:
                q = Q(**{'%s__%s' % (field_name, comparison):term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            
        queries.append(or_query)
    """
    queries = []
    queries_full = []
    #for field in search_fields:
    for term in terms:
        or_query = None
        #for term in terms:
        for field in search_fields:
            if isinstance(field, types.StringTypes):
                comparison = u'icontains'
                field_name = field
            elif isinstance(field, types.DictType):
                comparison = field.get('comparison', u'icontains')
                field_name = field.get('field_name', '')
                
            print 'field', field
            print 'term', term
            
            if field_name:
                q = Q(**{'%s__%s' % (field_name, comparison):term})
                print '%s__%s' % (field_name, comparison)
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            
        queries.append(or_query)
        print 'or_query', or_query
    print 'queries', queries

    or_query = None
    for field in search_fields:
        if isinstance(field, types.StringTypes):
            comparison = u'icontains'
            field_name = field
        elif isinstance(field, types.DictType):
            comparison = field.get('comparison', u'icontains')
            field_name = field.get('field_name', '')        

        if field_name:
            q = Q(**{'%s__%s' % (field_name, comparison):query_string})
            print '%s__%s' % (field_name, comparison)
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
               
    print '2nd', or_query            
    return queries, or_query


def perform_search(query_string):
    model_list = {}
    flat_list = []
    result_count = 0    

    if query_string:
        terms = normalize_query(query_string)
        
        for model, data in search_list.items():
            queries, query_full = get_query(query_string, terms, data['fields'])

            model_result_ids = None
            for query in queries:
                single_result_ids = set(model.objects.filter(query).values_list('pk', flat=True))
                #Convert queryset to python set and perform the 
                #AND operation on the program and not as a query
                if model_result_ids == None:
                    model_result_ids = single_result_ids
                else:
                    model_result_ids &= single_result_ids
                
            model_results = model.objects.filter(pk__in=model_result_ids)[:LIMIT]

            if model_results:
                model_list[data['text']] = model_results
                for result in model_results:
                    if result not in flat_list:
                        flat_list.append(result)
            
            full_result_ids = set(model.objects.filter(query_full).values_list('pk', flat=True))
            full_results = model.objects.filter(pk__in=full_result_ids)[:LIMIT]
            result_count += len(full_result_ids | model_result_ids)
            if full_results:
                model_list[data['text']] |= full_results
                for result in full_results:
                    if result not in flat_list:
                        flat_list.append(result)                
            
            print 'full_results', full_results

    return model_list, flat_list, result_count


def search(request):
    model_list = {}
    flat_list = []
    result_count = 0
            
    start_time = datetime.datetime.now()
    result_count = 0
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        form = SearchForm(initial={'q':query_string})
        try:
            model_list, flat_list, result_count = perform_search(query_string)
        except Exception, e:
            if settings.DEBUG:
                raise
            elif request.user.is_staff or request.user.is_superuser:
                messages.error(request, _(u'Search error: %s') % e)
    else:
        form = SearchForm()

    if LIMIT and result_count > LIMIT:
        title = _(u'results with: %s (showing only %s out of %s)') % (query_string, LIMIT, result_count)
    else:
        title = _(u'results with: %s') % query_string
    
    context = {
        'query_string':query_string, 
        'found_entries':model_list,
        'form':form,
        'object_list':flat_list,
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
