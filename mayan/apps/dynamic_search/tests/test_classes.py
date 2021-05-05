from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.search import document_search
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.tags.tests.mixins import TagTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from ..classes import SearchBackend


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

    def test_AND_scope(self):
        query = {
            '__0_tags__label': self.test_tags[0].label,
            '__operator_0_1': 'AND_901',
            '__result': '901',
            '__1_tags__label': self.test_tags[1].label
        }
        queryset = self.search_backend.search(
            search_model=document_search, query_string=query,
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
            search_model=document_search, query_string=query,
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
            search_model=document_search, query_string=query,
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
            search_model=document_search, query_string=query,
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
            search_model=document_search, query_string=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)
