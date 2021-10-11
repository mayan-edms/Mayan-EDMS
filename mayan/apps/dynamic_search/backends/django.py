import logging

from django.db.models import Q
from django.utils.encoding import force_text

from ..classes import SearchBackend

from .literals import (
    QUERY_OPERATION_AND, QUERY_OPERATION_OR, TERM_NEGATION_CHARACTER,
    TERM_OPERATION_OR, TERM_OPERATIONS, TERM_QUOTES, TERM_SPACE_CHARACTER
)
logger = logging.getLogger(name=__name__)


class DjangoSearchBackend(SearchBackend):
    def _search(
        self, query, search_model, user, global_and_search=False,
        ignore_limit=False
    ):
        search_query = self.get_search_query(
            global_and_search=global_and_search, query=query,
            search_model=search_model
        )

        return search_model.get_queryset().filter(
            search_query.django_query
        ).distinct()

    def deindex_instance(self, instance):
        """This backend doesn't remove instances."""

    def index_instance(self, instance):
        """
        This backend doesn't index instances. Searches query the
        database directly.
        """

    def get_search_query(
        self, query, search_model, global_and_search=False
    ):
        return SearchQuery(
            global_and_search=global_and_search, query=query,
            search_model=search_model
        )


class FieldQuery:
    def __init__(self, search_field, search_term_collection):
        query_operation = QUERY_OPERATION_AND
        self.django_query = None
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

                if self.django_query is None:
                    self.django_query = q_object
                else:
                    if query_operation == QUERY_OPERATION_AND:
                        self.django_query &= q_object
                    else:
                        self.django_query |= q_object

            if not term.is_meta:
                self.parts.append(force_text(s=search_field.label))
                self.parts.append(force_text(s=term))
            else:
                self.parts.append(term.string)

    def __str__(self):
        return ' '.join(self.parts)


class SearchQuery:
    def __init__(self, query, search_model, global_and_search=False):
        self.django_query = None
        self.text = []

        for search_field in search_model.search_fields:
            search_term_collection = SearchTermCollection(
                text=query.get(search_field.field, '').strip()
            )

            field_query = FieldQuery(
                search_field=search_field,
                search_term_collection=search_term_collection
            )

            if field_query.django_query:
                self.text.append('({})'.format(force_text(s=field_query)))

                if global_and_search:
                    self.text.append('AND')
                else:
                    self.text.append('OR')

                if self.django_query is None:
                    self.django_query = field_query.django_query
                else:
                    if global_and_search:
                        self.django_query &= field_query.django_query
                    else:
                        self.django_query |= field_query.django_query

        self.django_query = self.django_query or Q()

    def __str__(self):
        return ' '.join(self.text[:-1])


class SearchTerm:
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


class SearchTermCollection:
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
                result.append(force_text(s=term))

        return ' '.join(result)
