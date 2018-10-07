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

QUERY_OPERATION_AND = 1
QUERY_OPERATION_OR = 2

TERM_OPERATION_AND = 'AND'
TERM_OPERATION_OR = 'OR'
TERM_OPERATIONS = [TERM_OPERATION_AND, TERM_OPERATION_OR]


class SearchModel(object):
    _registry = {}

    @classmethod
    def all(cls):
        return list(cls._registry.values())

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
        term_letters = []
        terms = []

        for letter in text:
            if not inside_quotes and letter == NEGATION_CHARACTER:
                negated = True
            else:
                if letter in QUOTES:
                    if inside_quotes:
                        if term_letters:
                            terms.append(
                                {
                                    'meta': False,
                                    'negated': negated,
                                    'string': ''.join(term_letters)
                                }
                            )
                            negated = False
                            term_letters = []

                    inside_quotes = not inside_quotes
                else:
                    if not inside_quotes and letter == SPACE_CHARACTER:
                        if term_letters:
                            term_string = ''.join(term_letters)
                            if term_string in TERM_OPERATIONS:
                                meta = True
                            else:
                                meta = False

                            terms.append(
                                {
                                    'meta': meta,
                                    'negated': negated,
                                    'string': term_string
                                }
                            )
                            negated = False
                            term_letters = []
                    else:
                        term_letters.append(letter)

        if term_letters:
            terms.append(
                {
                    'meta': False,
                    'negated': negated,
                    'string': ''.join(term_letters)
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

        result = None
        for search_field in self.get_all_search_fields():

            terms = self.get_terms(
                query_string.get(
                    search_field.field, query_string.get('q', '')
                ).strip()
            )

            field_query = search_field.get_query(terms=terms)
            if field_query:
                if result is None:
                    result = field_query
                else:
                    if global_and_search:
                        result = result & field_query
                    else:
                        result = result | field_query

        elapsed_time = force_text(
            datetime.datetime.now() - start_time
        ).split(':')[2]

        logger.debug('elapsed_time: %s', elapsed_time)

        pk_list = set(self.model.objects.filter(result or Q()).values_list('pk', flat=True)[:setting_limit.value])
        queryset = self.model.objects.filter(pk__in=pk_list)

        if self.permission:
            queryset = AccessControlList.objects.filter_by_access(
                permission=self.permission, user=user, queryset=queryset
            )

        return queryset, elapsed_time


class SearchField(object):
    """
    Search for terms in fields that directly belong to the parent SearchModel
    """
    def __init__(self, search_model, field, label):
        self.search_model = search_model
        self.field = field
        self.label = label

    def get_full_name(self):
        return self.field

    def get_model(self):
        return self.search_model.model

    def get_query(self, terms):
        query_operation = QUERY_OPERATION_AND
        result = None

        for term in terms:
            if term['meta']:
                # It is a meta term, modifies the query operation
                # and is not searched
                if term['string'] == TERM_OPERATION_OR:
                    query_operation = QUERY_OPERATION_OR
            else:
                q_object = Q(
                    **{'%s__%s' % (self.field, 'icontains'): term['string']}
                )
                if term['negated']:
                    q_object = ~q_object

            if result is None:
                result = q_object
            else:
                if query_operation == QUERY_OPERATION_AND:
                    result = result & q_object
                else:
                    result = result | q_object

        return result
