from ..permissions import (
    permission_document_file_view, permission_document_view
)

from .base import GenericDocumentViewTestCase
from .mixins.document_mixins import DocumentSearchTestMixin


class DocumentSearchTestCase(
    DocumentSearchTestMixin, GenericDocumentViewTestCase
):
    def test_document_file_page_search_no_permission(self):
        queryset = self._perform_document_file_page_search()
        self.assertFalse(
            self.test_document.file_latest.pages.first() in queryset
        )

    def test_document_file_page_search_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )
        queryset = self._perform_document_file_page_search()
        self.assertTrue(
            self.test_document.file_latest.pages.first() in queryset
        )

    def test_document_search_no_permission(self):
        queryset = self._perform_document_search()
        self.assertFalse(self.test_document in queryset)

    def test_document_search_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        queryset = self._perform_document_search()
        self.assertTrue(self.test_document in queryset)
