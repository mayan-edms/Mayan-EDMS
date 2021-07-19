from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.search import document_search
from mayan.apps.documents.tests.literals import DEFAULT_DOCUMENT_STUB_LABEL
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.tags.tests.mixins import TagTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from ..classes import SearchBackend
from ..exceptions import DynamicSearchException


class QueryStringDecodeTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.search_backend = SearchBackend.get_instance()

    def test_decode_default_scope(self):
        query = {
            'test_field': 'test_value'
        }

        self.assertEqual(
            self.search_backend.decode_query(query=query), {
                'operators': {}, 'result_scope': '0',
                'scopes': {
                    '0': {
                        'match_all': False, 'query': {
                            'test_field': 'test_value'
                        }
                    }
                }
            }
        )

    def test_decode_default_scope_with_explicit_scope(self):
        query = {
            'test_field': 'test_value',
            '__1_test_field': 'test_value',
        }

        self.assertEqual(
            self.search_backend.decode_query(query=query), {
                'operators': {}, 'result_scope': '0',
                'scopes': {
                    '0': {
                        'match_all': False, 'query': {
                            'test_field': 'test_value'
                        }
                    },
                    '1': {
                        'match_all': False, 'query': {
                            'test_field': 'test_value'
                        }
                    }
                }
            }
        )

    def test_decode_scope_0_match_all(self):
        query = {
            '__0_test_field': 'test_value',
            '__0_match_all': 'true',
            '__1_test_field': 'test_value',
        }

        self.assertEqual(
            self.search_backend.decode_query(query=query), {
                'operators': {}, 'result_scope': '0',
                'scopes': {
                    '0': {
                        'match_all': True, 'query': {
                            'test_field': 'test_value'
                        }
                    },
                    '1': {
                        'match_all': False, 'query': {
                            'test_field': 'test_value'
                        }
                    }
                }
            }
        )

    def test_decode_scope_1_match_all(self):
        query = {
            '__0_test_field': 'test_value',
            '__0_match_all': 'false',
            '__1_test_field': 'test_value',
            '__1_match_all': 'true',
        }

        self.assertEqual(
            self.search_backend.decode_query(query=query), {
                'operators': {}, 'result_scope': '0',
                'scopes': {
                    '0': {
                        'match_all': False, 'query': {
                            'test_field': 'test_value'
                        }
                    },
                    '1': {
                        'match_all': True, 'query': {
                            'test_field': 'test_value'
                        }
                    }
                }
            }
        )


class ScopedSearchTestCase(DocumentTestMixin, TagTestMixin, BaseTestCase):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self.search_backend = SearchBackend.get_instance()

        self._create_test_document_stub()
        self._create_test_tag()
        self._create_test_tag()

        self.test_tags[0].documents.add(self.test_document)
        self.test_tags[1].documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

    def test_missing_scope_query(self):
        query = {
            '__a_match_all': 'true',
            '__operator_a_b': 'OR_c',
            '__b_label': self.test_documents[0].label,
            '__result': 'c'
        }
        with self.assertRaises(expected_exception=DynamicSearchException):
            self.search_backend.search(
                search_model=document_search, query=query,
                user=self._test_case_user
            )

    def test_AND_scope(self):
        query = {
            '__0_tags__label': self.test_tags[0].label,
            '__operator_0_1': 'AND_901',
            '__result': '901',
            '__1_tags__label': self.test_tags[1].label
        }
        queryset = self.search_backend.search(
            search_model=document_search, query=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)

        self.test_tags[1].documents.remove(self.test_document)

        query = {
            '__0_tags__label': self.test_tags[0].label,
            '__operator_0_1': 'AND_901',
            '__result': '901',
            '__1_tags__label': self.test_tags[1].label
        }
        queryset = self.search_backend.search(
            search_model=document_search, query=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

    def test_OR_scope(self):
        query = {
            '__0_tags__label': self.test_tags[0].label,
            '__operator_0_1': 'OR_901',
            '__result': '901',
            '__1_tags__label': self.test_tags[1].label
        }
        queryset = self.search_backend.search(
            search_model=document_search, query=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)

    def test_letter_scopes(self):
        query = {
            '__a_tags__label': self.test_tags[0].label,
            '__operator_a_b': 'OR_c',
            '__result': 'c',
            '__b_tags__label': self.test_tags[1].label
        }
        queryset = self.search_backend.search(
            search_model=document_search, query=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)

    def test_multi_letter_scopes(self):
        query = {
            '__ab_tags__label': self.test_tags[0].label,
            '__operator_ab_bc': 'OR_cc',
            '__result': 'cc',
            '__bc_tags__label': self.test_tags[1].label
        }
        queryset = self.search_backend.search(
            search_model=document_search, query=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)

    def test_single_scope(self):
        query = {
            '__ab_tags__label': self.test_tags[0].label,
            '__operator_ab_bc': 'OR_cc',
            '__result': 'ab',
            '__bc_tags__label': self.test_tags[1].label
        }
        queryset = self.search_backend.search(
            search_model=document_search, query=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_documents[0] in queryset)

    def test_scoped_and_non_scoped(self):
        query = {
            '__0_match_all': 'TRUE',
            '__0_tags__label': self.test_tags[0].label,
            '__0_tags__color': 'FFFFFF',
            '__operator_0_bc': 'AND_cc',
            '__bc_tags__label': self.test_tags[1].label,
            '__bc_tags__color': '000000',
            '__result': 'cc'
        }
        queryset = self.search_backend.search(
            search_model=document_search, query=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_documents[0] in queryset)


class ScopeOperatorSearchTestCase(DocumentTestMixin, BaseTestCase):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self.search_backend = SearchBackend.get_instance()

        self._create_test_document_stub()
        self._create_test_document_stub()

        self.grant_access(
            obj=self.test_documents[0], permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_documents[1], permission=permission_document_view
        )

    def test_and_operator_both_scopes_with_data(self):
        query = {
            '__0_label': DEFAULT_DOCUMENT_STUB_LABEL,
            '__operator_0_1': 'AND_2',
            '__1_label': DEFAULT_DOCUMENT_STUB_LABEL,
            '__result': '2'
        }
        queryset = self.search_backend.search(
            search_model=document_search, query=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 2)

    def test_and_operator_scope_1_with_data(self):
        query = {
            '__0_label': DEFAULT_DOCUMENT_STUB_LABEL,
            '__operator_0_1': 'AND_2',
            '__1_label': 'invalid',
            '__result': '2'
        }
        queryset = self.search_backend.search(
            search_model=document_search, query=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

    def test_and_operator_scope_2_with_data(self):
        query = {
            '__0_label': 'invalid',
            '__operator_0_1': 'AND_2',
            '__1_label': DEFAULT_DOCUMENT_STUB_LABEL,
            '__result': '2'
        }
        queryset = self.search_backend.search(
            search_model=document_search, query=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)
