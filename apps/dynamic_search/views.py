import re

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.db.models import Q
from django.contrib import messages
from django.core.exceptions import FieldError


from api import search_list
from forms import SearchForm
from conf.settings import SHOW_OBJECT_TYPE

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
    query = None # Query to search for every search term        
    #terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def search(request):
    query_string = ''
    found_entries = {}
    object_list = []

    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        form = SearchForm(initial={'q':query_string})
        
        terms = normalize_query(query_string)
        
        for model, data in search_list.items():
            query = get_query(terms, data['fields'])            

            try:
                results = model.objects.filter(query).distinct()
                if results:
                    found_entries[data['text']] = results
                    for result in results:
                        object_list.append(result)
            except FieldError, e:
                if request.user.is_staff or request.user.is_superuser:
                    messages.error(request, _(u'Search error: %s') % e)
    else:
        form = SearchForm()
    
    context = {
        'query_string':query_string, 
        'found_entries':found_entries,
        'form':form,
        'object_list':object_list,
        'form_title':_(u'Search'),
        'hide_header':True,
        'title':_(u'results with: %s') % query_string
    }

    if SHOW_OBJECT_TYPE:
        context.update({'extra_columns':
            [{'name':_(u'type'), 'attribute':lambda x:x._meta.verbose_name[0].upper() + x._meta.verbose_name[1:]}]})
        
    return render_to_response('search_results.html', context,
                          context_instance=RequestContext(request))
