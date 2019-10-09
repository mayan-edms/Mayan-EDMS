from __future__ import absolute_import, unicode_literals

import logging

from django.apps import apps
from django.db.models import Q
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.module_loading import import_string
from django.utils.translation import ugettext as _

from mayan.apps.common.literals import LIST_MODE_CHOICE_LIST

from .literals import (
    QUERY_OPERATION_AND, QUERY_OPERATION_OR, TERM_NEGATION_CHARACTER,
    TERM_OPERATION_OR, TERM_OPERATIONS, TERM_QUOTES, TERM_SPACE_CHARACTER
)

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class FieldQuery(object):
    def __init__(self, search_field, search_term_collection):
        query_operation = QUERY_OPERATION_AND
        self.query = None
        self.parts = []

        for term in search_term_collection.terms:
            if term.is_meta:
                # It is a meta term, modifies the query operation
                # and is not searched
                if term.string == TERM_OPERATION_OR:
                    query_operation = QUERY_OPERATION_OR
            else:
                if search_field.transformation_function:
                    term_string = search_field.transformation_function(
                        term_string=term.string
                    )
                else:
                    term_string = term.string

                q_object = Q(
                    **{'%s__%s' % (search_field.field, 'icontains'): term_string}
                )
                if term.negated:
                    q_object = ~q_object

                if self.query is None:
                    self.query = q_object
                else:
                    if query_operation == QUERY_OPERATION_AND:
                        self.query = self.query & q_object
                    else:
                        self.query = self.query | q_object

            if not term.is_meta:
                self.parts.append(force_text(search_field.label))
                self.parts.append(force_text(term))
            else:
                self.parts.append(term.string)

    def __str__(self):
        return ' '.join(self.parts)


class SearchField(object):
    """
    Search for terms in fields that directly belong to the parent SearchModel
    """
    def __init__(self, search_model, field, label, transformation_function=None):
        self.search_model = search_model
        self.field = field
        self.label = label
        self.transformation_function = transformation_function

    def get_full_name(self):
        return self.field

    def get_model(self):
        return self.search_model.model


@python_2_unicode_compatible
class SearchModel(object):
    _registry = {}

    @classmethod
    def all(cls):
        return sorted(list(cls._registry.values()), key=lambda x: x.label)

    @classmethod
    def as_choices(cls):
        return cls._registry

    @classmethod
    def get(cls, name):
        try:
            result = cls._registry[name]
        except KeyError:
            raise KeyError(_('No search model matching the query'))
        if not hasattr(result, 'serializer'):
            result.serializer = import_string(result.serializer_path)

        return result

    def __init__(
        self, app_label, model_name, serializer_path, label=None,
        list_mode=None, permission=None, queryset=None
    ):
        self.app_label = app_label
        self.list_mode = list_mode or LIST_MODE_CHOICE_LIST
        self.model_name = model_name
        self.search_fields = []
        self._model = None  # Lazy
        self._label = label
        self.serializer_path = serializer_path
        self.permission = permission
        self.queryset = queryset
        self.__class__._registry[self.get_full_name()] = self

    def __str__(self):
        return force_text(self.label)

    def add_model_field(self, *args, **kwargs):
        """
        Add a search field that directly belongs to the parent SearchModel
        """
        search_field = SearchField(self, *args, **kwargs)
        self.search_fields.append(search_field)

    def get_fields_simple_list(self):
        """
        Returns a list of the fields for the SearchModel
        """
        result = []
        for search_field in self.search_fields:
            result.append((search_field.get_full_name(), search_field.label))

        return result

    def get_full_name(self):
        return '%s.%s' % (self.app_label, self.model_name)

    def get_queryset(self):
        if self.queryset:
            return self.queryset()
        else:
            return self.model.objects.all()

    def get_search_field(self, full_name):
        try:
            return self.search_fields[full_name]
        except KeyError:
            raise KeyError('No search field named: %s' % full_name)

    def get_search_query(self, query_string, global_and_search=False):
        return SearchQuery(
            query_string=query_string, search_model=self,
            global_and_search=global_and_search
        )

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

    def search(self, query_string, user, global_and_search=False):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )

        search_query = self.get_search_query(
            query_string=query_string, global_and_search=global_and_search
        )

        try:
            queryset = self.get_queryset().filter(search_query.query).distinct()
        except Exception:
            logger.error(
                'Error filtering model %s with queryset: %s', self.model,
                search_query.query
            )
            raise

        if self.permission:
            queryset = AccessControlList.objects.restrict_queryset(
                permission=self.permission, queryset=queryset, user=user
            )

        return queryset


@python_2_unicode_compatible
class SearchQuery(object):
    def __init__(self, query_string, search_model, global_and_search=False):
        self.query = None
        self.text = []

        for search_field in search_model.search_fields:
            search_term_collection = SearchTermCollection(
                text=query_string.get(
                    search_field.field, query_string.get('q', '')
                ).strip()
            )

            field_query = FieldQuery(
                search_field=search_field,
                search_term_collection=search_term_collection
            )

            if field_query.query:
                self.text.append('({})'.format(force_text(field_query)))

                if global_and_search:
                    self.text.append('AND')
                else:
                    self.text.append('OR')

                if self.query is None:
                    self.query = field_query.query
                else:
                    if global_and_search:
                        self.query = self.query & field_query.query
                    else:
                        self.query = self.query | field_query.query

        self.query = self.query or Q()

    def __str__(self):
        return ' '.join(self.text[:-1])


@python_2_unicode_compatible
class SearchTerm(object):
    def __init__(self, negated, string, is_meta):
        self.negated = negated
        self.string = string
        self.is_meta = is_meta

    def __str__(self):
        if self.is_meta:
            return ''
        else:
            return '{}contains "{}"'.format(
                'does not ' if self.negated else '', self.string
            )


@python_2_unicode_compatible
class SearchTermCollection(object):
    def __init__(self, text):
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
        inside_quotes = False
        negated = False
        term_letters = []
        self.terms = []

        for letter in text:
            if letter in TERM_QUOTES:
                if inside_quotes:
                    if term_letters:
                        term_string = ''.join(term_letters)
                        negated = False
                        if term_string.startswith(TERM_NEGATION_CHARACTER):
                            term_string = term_string[1:]
                            negated = True

                        self.terms.append(
                            SearchTerm(
                                is_meta=False, negated=negated,
                                string=term_string
                            )
                        )
                        negated = False
                        term_letters = []

                inside_quotes = not inside_quotes
            else:
                if not inside_quotes and letter == TERM_SPACE_CHARACTER:
                    if term_letters:
                        term_string = ''.join(term_letters)
                        if term_string in TERM_OPERATIONS:
                            is_meta = True
                        else:
                            is_meta = False

                        if is_meta:
                            negated = False
                        else:
                            negated = False
                            if term_string.startswith(TERM_NEGATION_CHARACTER):
                                term_string = term_string[1:]
                                negated = True

                        self.terms.append(
                            SearchTerm(
                                is_meta=is_meta, negated=negated,
                                string=term_string
                            )
                        )
                        negated = False
                        term_letters = []
                else:
                    term_letters.append(letter)

        if term_letters:
            term_string = ''.join(term_letters)
            negated = False
            if term_string.startswith(TERM_NEGATION_CHARACTER):
                term_string = term_string[1:]
                negated = True

            self.terms.append(
                SearchTerm(
                    is_meta=False, negated=negated,
                    string=term_string
                )
            )

    def __str__(self):
        result = []
        for term in self.terms:
            if term.is_meta:
                result.append(term.string)
            else:
                result.append(force_text(term))

        return ' '.join(result)
