# original code from:
# http://www.julienphalip.com/blog/2008/08/16/adding-search-django-site-snap/

import re
import types
import datetime

from django.db.models import Q

from dynamic_search.conf.settings import LIMIT

search_list = {}


def register(model, text, field_list):
    if model in search_list:
        search_list[model]['fields'].append(field_list)
    else:
        search_list[model] = {'fields': field_list, 'text': text}


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    """ Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    """
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(terms, search_fields):
    """
        Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
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
                field_name = field.get('field_name', u'')

            if field_name:
                q = Q(**{'%s__%s' % (field_name, comparison): term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q

        queries.append(or_query)
    return queries


def perform_search(query_string):
    model_list = {}
    flat_list = []
    result_count = 0
    shown_result_count = 0
    elapsed_time = 0

    if query_string:
        start_time = datetime.datetime.now()
        terms = normalize_query(query_string)

        for model, data in search_list.items():
            queries = get_query(terms, data['fields'])

            model_result_ids = None
            for query in queries:
                single_result_ids = set(model.objects.filter(query).values_list('pk', flat=True))
                #Convert queryset to python set and perform the
                #AND operation on the program and not as a query
                if model_result_ids == None:
                    model_result_ids = single_result_ids
                else:
                    model_result_ids &= single_result_ids

            result_count += len(model_result_ids)
            results = model.objects.in_bulk(list(model_result_ids)[: LIMIT]).values()
            shown_result_count += len(results)
            if results:
                model_list[data['text']] = results
                for result in results:
                    if result not in flat_list:
                        flat_list.append(result)
        elapsed_time = unicode(datetime.datetime.now() - start_time).split(':')[2]

    return model_list, flat_list, shown_result_count, result_count, elapsed_time
