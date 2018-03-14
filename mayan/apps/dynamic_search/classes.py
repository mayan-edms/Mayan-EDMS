from __future__ import absolute_import, unicode_literals

import datetime
import logging

from django.apps import apps
from django.db.models import Q
from django.utils.encoding import force_text
from django.utils.module_loading import import_string
from django.utils.translation import ugettext as _

from .settings import setting_limit

logger = logging.getLogger(__name__)


class SearchModel(object):
    _registry = {}

    @classmethod
    def all(cls):
        return cls._registry.values()

    @classmethod
    def as_choices(cls):
        return cls._registry

    @classmethod
    def get(cls, full_name):
        try:
            result = cls._registry[full_name]
        except KeyError:
            raise KeyError(_('No search model matching the query'))
        if not hasattr(result, 'serializer'):
            result.serializer = import_string(result.serializer_string)

        return result

    @staticmethod
    def get_terms(text):
        """
        Takes a text string and returns a list of dictionaries.
        Each dictionary has two key "negated" and "string"

        String 'a "b c" d "e" \'f g\' h -i -"j k" l -\'m n\' o OR p'

        Results in:
        [
            {'negated': False, 'string': 'a'}, {'negated': False, 'string': 'b c'},
            {'negated': False, 'string': 'd'}, {'negated': False, 'string': 'e'},
            {'negated': False, 'string': 'f g'}, {'negated': False, 'string': 'h'},
            {'negated': True, 'string': 'i'}, {'negated': True, 'string': 'j k'},
            {'negated': False, 'string': 'l'}, {'negated': True, 'string': 'm n'},
            {'negated': False, 'string': 'o'}, {'negated': False, 'string': 'OR'},
            {'negated': False, 'string': 'p'}
        ]
        """
        QUOTES = ['"', '\'']
        NEGATION_CHARACTER = '-'
        SPACE_CHARACTER = ' '

        inside_quotes = False
        negated = False
        term = []
        terms = []

        for letter in text:
            if not inside_quotes and letter == NEGATION_CHARACTER:
                negated = True
            else:
                if letter in QUOTES:
                    if inside_quotes:
                        if term:
                            terms.append(
                                {
                                    'meta': False,
                                    'negated': negated,
                                    'string': ''.join(term)
                                }
                            )
                            negated = False
                            term = []

                    inside_quotes = not inside_quotes
                else:
                    if not inside_quotes and letter == SPACE_CHARACTER:
                        if term:
                            if term == ['O', 'R']:
                                meta = True
                            else:
                                meta = False

                            terms.append(
                                {
                                    'meta': meta,
                                    'negated': negated,
                                    'string': ''.join(term)
                                }
                            )
                            negated = False
                            term = []
                    else:
                        term.append(letter)

        if term:
            terms.append(
                {
                    'meta': False,
                    'negated': negated,
                    'string': ''.join(term)
                }
            )

        return terms

    def __init__(self, app_label, model_name, serializer_string, label=None, permission=None):
        self.app_label = app_label
        self.model_name = model_name
        self.search_fields = []
        self._model = None  # Lazy
        self._label = label
        self.serializer_string = serializer_string
        self.permission = permission
        self.__class__._registry[self.get_full_name()] = self

    @property
    def label(self):
        if not self._label:
            self._label = self.model._meta.verbose_name
        return self._label

    @property
    def model(self):
        if not self._model:
            self._model = apps.get_model(self.app_label, self.model_name)
        return self._model

    @property
    def pk(self):
        return self.get_full_name()

    def add_model_field(self, *args, **kwargs):
        """
        Add a search field that directly belongs to the parent SearchModel
        """
        search_field = SearchField(self, *args, **kwargs)
        self.search_fields.append(search_field)

    def assemble_query(self, terms, search_fields):
        """
        Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search
        fields.
        """
        queries = []

        for term in terms:
            query = None
            if term['string'] != 'OR':
                for field in search_fields:
                    q = Q(**{'%s__%s' % (field, 'icontains'): term['string']})

                    if term['negated']:
                        q = ~q

                    if query is None:
                        query = q
                    else:
                        query = query | q

            queries.append(query)
        return queries

    def get_all_search_fields(self):
        return self.search_fields

    def get_full_name(self):
        return '%s.%s' % (self.app_label, self.model_name)

    def get_fields_simple_list(self):
        """
        Returns a list of the fields for the SearchModel
        """
        result = []
        for search_field in self.get_all_search_fields():
            result.append((search_field.get_full_name(), search_field.label))

        return result

    def get_search_field(self, full_name):
        try:
            return self.search_fields[full_name]
        except KeyError:
            raise KeyError('No search field named: %s' % full_name)

    def search(self, query_string, user, global_and_search=False):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )

        elapsed_time = 0
        start_time = datetime.datetime.now()
        result_set = set()
        search_dict = {}

        if 'q' in query_string:
            # Simple search
            for search_field in self.get_all_search_fields():
                search_dict.setdefault(search_field.get_model(), {
                    'searches': [],
                    'label': search_field.label,
                    'return_value': search_field.return_value
                })
                search_dict[search_field.get_model()]['searches'].append(
                    {
                        'field_name': [search_field.field],
                        'terms': SearchModel.get_terms(
                            query_string.get('q', '').strip()
                        )
                    }
                )
        else:
            for search_field in self.get_all_search_fields():
                if search_field.field in query_string and query_string[search_field.field]:
                    search_dict.setdefault(search_field.get_model(), {
                        'searches': [],
                        'label': search_field.label,
                        'return_value': search_field.return_value
                    })
                    search_dict[search_field.get_model()]['searches'].append(
                        {
                            'field_name': [search_field.field],
                            'terms': SearchModel.get_terms(
                                query_string[search_field.field]
                            )
                        }
                    )

        for model, data in search_dict.items():
            logger.debug('model: %s', model)

            # Initialize per model result set
            model_result_set = set()

            for query_entry in data['searches']:
                # Fashion a list of queries for a field for each term
                field_query_list = self.assemble_query(
                    query_entry['terms'], query_entry['field_name']
                )

                logger.debug('field_query_list: %s', field_query_list)

                # Initialize per field result set
                field_result_set = set()

                # Get results per search field
                intersection = True
                for query in field_query_list:
                    logger.debug('query: %s', query)

                    if query:
                        term_query_result_set = set(
                            model.objects.filter(query).values_list(
                                data['return_value'], flat=True
                            )
                        )

                        # Convert the QuerySet to a Python set and perform the
                        # AND operation on the program and not as a query.
                        # This operation ANDs all the field term results
                        # belonging to a single model, making sure to only include
                        # results in the final field result variable if all the
                        # terms are found in a single field.
                        if not field_result_set:
                            field_result_set = term_query_result_set
                        else:
                            if intersection:
                                field_result_set &= term_query_result_set
                            else:
                                field_result_set |= term_query_result_set

                        logger.debug(
                            'term_query_result_set: %s', len(term_query_result_set)
                        )
                        logger.debug('field_result_set: %s', len(field_result_set))

                        intersection = True
                    else:
                        intersection = False

                if global_and_search:
                    if not model_result_set:
                        model_result_set = field_result_set
                    else:
                        model_result_set &= field_result_set
                else:
                    model_result_set |= field_result_set

            result_set = result_set | model_result_set

        elapsed_time = force_text(
            datetime.datetime.now() - start_time
        ).split(':')[2]

        logger.debug('elapsed_time: %s', elapsed_time)

        queryset = self.model.objects.filter(
            pk__in=list(result_set)[:setting_limit.value]
        )

        if self.permission:
            queryset = AccessControlList.objects.filter_by_access(
                permission=self.permission, user=user, queryset=queryset
            )

        return queryset, elapsed_time


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
