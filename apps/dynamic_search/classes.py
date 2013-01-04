from __future__ import absolute_import

import re
import types
import logging
import datetime

from django.db.models import Q
from django.db.models.loading import get_model

from .conf.settings import LIMIT

logger = logging.getLogger(__name__)


class SearchModel(object):
    registry = {}

    @classmethod
    def get_all(cls):
        return cls.registry.values()

    def __init__(self, app_label, model_name, label=None):
        self.app_label = app_label
        self.model_name = model_name
        self.search_fields = []
        self.model = get_model(app_label, model_name)
        self.label = label or self.model._meta.verbose_name
        self.__class__.registry[id(self)] = self

    def get_fields_simple_list(self):
        """
        Returns a list of the fields for the SearchModel
        """
        result = []
        for search_field in self.search_fields:
            result.append((search_field.get_full_name(), search_field.label))

        return result

    def add_model_field(self, *args, **kwargs):
        """
        Add a search field that directly belongs to the parent SearchModel
        """
        self.search_fields.append(SearchField(self, *args, **kwargs))
    
    def add_related_field(self, *args, **kwargs):
        """
        Add a search field that will search content in a related field in
        a separate model
        """
        self.search_fields.append(RelatedSearchField(self, *args, **kwargs))

    def normalize_query(self, query_string,
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

    def simple_search(self, query_string):
        search_dict = {}
        model_list = {}
        flat_list = []
        result_count = 0
        shown_result_count = 0
        elapsed_time = 0
        start_time = datetime.datetime.now()

        for search_field in self.search_fields:
            search_dict.setdefault(search_field.get_model(), {
                'query_entries': [],
                'label': search_field.label,
                'return_value': search_field.return_value
            })
            search_dict[search_field.get_model()]['query_entries'].append(
                {
                    'field_name': [search_field.field],
                    'terms': self.normalize_query(query_string)
                }
            )        
        
        logger.debug('search_dict: %s' % search_dict)

        for model, data in search_dict.items():
            label = data['label']
            queries = []

            for query_entry in data['query_entries']:
                queries.extend(self.assemble_query(query_entry['terms'], query_entry['field_name']))

            # Initialize per SearchFiel model id result list
            model_result_ids = set()
        
            for query in queries:
                logger.debug('query: %s' % query)
                
                # Get results per search field
                field_result_ids = set(model.objects.filter(query).values_list(data['return_value'], flat=True))
                
                # Convert the QuerySet to a Python set and perform the
                # AND operation on the program and not as a query.
                # This operation ANDs all the SearchField results
                # belonging to a single model, making sure to only include
                # results in the model result variable if all the terms
                # are found in a single field
                if not model_result_ids:
                    model_result_ids = field_result_ids
                else:
                    model_result_ids &= field_result_ids

                logger.debug('field_result_ids: %s' % field_result_ids)
                logger.debug('model_result_ids: %s' % model_result_ids)

            # Update the search result total count
            result_count += len(model_result_ids)

            # Search the field results return values (PK) in the SearchModel's model
            results = self.model.objects.in_bulk(list(model_result_ids)[: LIMIT]).values()

            # Update the search result visible count (limited by LIMIT config option)
            shown_result_count += len(results)

            if results:
                model_list[label] = results
                for result in results:
                    if result not in flat_list:
                        flat_list.append(result)
            
            logger.debug('model_list: %s' % model_list)
            logger.debug('flat_list: %s' % flat_list)

        elapsed_time = unicode(datetime.datetime.now() - start_time).split(':')[2]

        return model_list, flat_list, shown_result_count, result_count, elapsed_time
                
    def advanced_search(self, dictionary):
        for key, value in dictionary.items():
            try:
                model, field_name = key.split('__', 1)
                model_entry = registered_search_dict.get(model, {})
                if model_entry:
                    for model_field in model_entry.get('fields', [{}]):
                        if model_field.get('name') == field_name:
                            search_dict.setdefault(model_entry['model'], {'query_entries': [], 'label': model_entry['label']})
                            search_dict[model_entry['model']]['query_entries'].append(
                                {
                                    'field_name': [field_name],
                                    'terms': normalize_query(value.strip())
                                }
                            )
            except ValueError:
                pass

    def assemble_query(self, terms, search_fields):
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


# SearchField classes
class SearchField(object):
    """
    Search for terms in fields that directly belong to the parent SearchModel
    """
    def __init__(self, search_model, field, label):
        self.search_model = search_model
        self.field = field
        self.label = label
        self.return_value = 'pk'

    def get_full_name(self):
        return self.field

    def get_model(self):
        return self.search_model.model


class RelatedSearchField(object):
    """
    Search for terms in fields that are related to the parent SearchModel
    """
    def __init__(self, search_model, app_label, model_name, field, return_value, label):
        self.search_model = search_model
        self.app_label = app_label
        self.model_name = model_name
        self.field = field
        self.return_value = return_value
        self.model = get_model(app_label, model_name)
        self.label = label

    def get_full_name(self):
        return '%s.%s.%s' % (self.app_label, self.model_name, self.field)

    def get_model(self):
        return self.model
