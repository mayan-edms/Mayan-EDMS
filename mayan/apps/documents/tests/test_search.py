from __future__ import unicode_literals

from mayan.apps.common.tests import BaseTestCase
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.search import document_search, document_page_search
from mayan.apps.documents.tests import DocumentTestMixin


class DocumentSearchTestCase(DocumentTestMixin, BaseTestCase):
    def _perform_document_page_search(self):
        return document_page_search.search(
            query_string={'q': self.test_document.label}, user=self._test_case_user
        )

    def _perform_document_search(self):
        return document_search.search(
            query_string={'q': self.test_document.label}, user=self._test_case_user
        )

    def test_document_page_search_no_access(self):
        queryset = self._perform_document_page_search()
        self.assertFalse(self.test_document.pages.first() in queryset)

    def test_document_page_search_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        queryset = self._perform_document_page_search()
        self.assertTrue(self.test_document.pages.first() in queryset)

    def test_document_search_no_access(self):
        queryset = self._perform_document_search()
        self.assertFalse(self.test_document in queryset)

    def test_document_search_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        queryset = self._perform_document_search()
        self.assertTrue(self.test_document in queryset)
