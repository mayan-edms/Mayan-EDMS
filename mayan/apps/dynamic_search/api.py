# original code from:
# http://www.julienphalip.com/blog/2008/08/16/adding-search-django-site-snap/
from __future__ import unicode_literals

import datetime
import re
import types

from django.db.models import Q

from .settings import LIMIT

registered_search_dict = {}


def register(model_name, model, title, fields):
    registered_search_dict.setdefault(model_name, {'model': model, 'fields': [], 'title': title})
    registered_search_dict[model_name]['fields'].extend(fields)


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    """
    Splits the query string in invidual keywords, getting rid of unecessary spaces
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
                comparison = 'icontains'
                field_name = field
            elif isinstance(field, types.DictType):
                comparison = field.get('comparison', 'icontains')
                field_name = field.get('field_name', '')

            if field_name:
                q = Q(**{'%s__%s' % (field_name, comparison): term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q

        queries.append(or_query)
    return queries


def perform_search(query_string, field_list=None):
    model_list = {}
    flat_list = []
    result_count = 0
    shown_result_count = 0
    elapsed_time = 0
    start_time = datetime.datetime.now()

    search_dict = {}

    if query_string:
        simple_query_string = query_string.get('q', '').strip()
        if simple_query_string:
            for model, values in registered_search_dict.items():
                search_dict.setdefault(values['model'], {'query_entries': [], 'title': values['title']})
                field_names = [field['name'] for field in values['fields']]
                # One entry, single set of terms for all fields names
                search_dict[values['model']]['query_entries'].append(
                    {
                        'field_name': field_names,
                        'terms': normalize_query(simple_query_string)
                    }
                )
        else:
            for key, value in query_string.items():
                try:
                    model, field_name = key.split('__', 1)
                    model_entry = registered_search_dict.get(model, {})
                    if model_entry:
                        for model_field in model_entry.get('fields', [{}]):
                            if model_field.get('name') == field_name:
                                search_dict.setdefault(model_entry['model'], {'query_entries': [], 'title': model_entry['title']})
                                search_dict[model_entry['model']]['query_entries'].append(
                                    {
                                        'field_name': [field_name],
                                        'terms': normalize_query(value.strip())
                                    }
                                )
                except ValueError:
                    pass

        for model, data in search_dict.items():
            title = data['title']
            queries = []

            for query_entry in data['query_entries']:
                queries.extend(get_query(query_entry['terms'], query_entry['field_name']))

            model_result_ids = None
            for query in queries:
                single_result_ids = set(model.objects.filter(query).values_list('pk', flat=True))
                # Convert queryset to python set and perform the
                # AND operation on the program and not as a query
                if not model_result_ids:
                    model_result_ids = single_result_ids
                else:
                    model_result_ids &= single_result_ids

            if not model_result_ids:
                model_result_ids = []

            result_count += len(model_result_ids)
            results = model.objects.in_bulk(list(model_result_ids)[: LIMIT]).values()
            shown_result_count += len(results)
            if results:
                model_list[title] = results
                for result in results:
                    if result not in flat_list:
                        flat_list.append(result)

        elapsed_time = unicode(datetime.datetime.now() - start_time).split(':')[2]

    return {
        'model_list': model_list,
        'flat_list': flat_list,
        'shown_result_count': shown_result_count,
        'result_count': result_count,
        'elapsed_time': elapsed_time
    }
