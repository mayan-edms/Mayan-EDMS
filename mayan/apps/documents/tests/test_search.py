from ..permissions import (
    permission_document_file_view, permission_document_view,
    permission_document_version_view
)

from .base import GenericDocumentViewTestCase
from .mixins.document_mixins import DocumentSearchTestMixin
from .mixins.document_file_mixins import (
    DocumentFileSearchTestMixin, DocumentFilePageSearchTestMixin
)
from .mixins.document_version_mixins import (
    DocumentVersionSearchTestMixin, DocumentVersionPageSearchTestMixin
)


class DocumentSearchTestCase(
    DocumentSearchTestMixin, GenericDocumentViewTestCase
):
    def test_document_search_no_permission(self):
        queryset = self._perform_document_search()
        self.assertFalse(self.test_document in queryset)

    def test_document_search_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self._perform_document_search()
        self.assertTrue(self.test_document in queryset)

    def test_trashed_document_search_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self.test_document.delete()

        queryset = self._perform_document_search()
        self.assertFalse(self.test_document in queryset)


class DocumentFileSearchTestCase(
    DocumentFileSearchTestMixin, GenericDocumentViewTestCase
):
    def test_document_file_search_no_permission(self):
        queryset = self._perform_document_file_search()
        self.assertFalse(self.test_document.file_latest in queryset)

    def test_document_file_search_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        queryset = self._perform_document_file_search()
        self.assertTrue(self.test_document.file_latest in queryset)

    def test_trashed_document_file_search_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self.test_document.delete()

        queryset = self._perform_document_file_search()
        self.assertFalse(self.test_document.file_latest in queryset)


class DocumentFilePageSearchTestCase(
    DocumentFilePageSearchTestMixin, GenericDocumentViewTestCase
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

    def test_trashed_document_file_page_search_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self.test_document.delete()

        queryset = self._perform_document_file_page_search()
        self.assertFalse(
            self.test_document.file_latest.pages.first() in queryset
        )


class DocumentVersionSearchTestCase(
    DocumentVersionSearchTestMixin, GenericDocumentViewTestCase
):
    def test_document_version_search_no_permission(self):
        queryset = self._perform_document_version_search()
        self.assertFalse(self.test_document.version_active in queryset)

    def test_document_version_search_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_view
        )

        queryset = self._perform_document_version_search()
        self.assertTrue(self.test_document.version_active in queryset)

    def test_trashed_document_version_search_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_view
        )

        self.test_document.delete()

        queryset = self._perform_document_version_search()
        self.assertFalse(self.test_document.version_active in queryset)


class DocumentVersionPageSearchTestCase(
    DocumentVersionPageSearchTestMixin, GenericDocumentViewTestCase
):
    def test_document_version_page_search_no_permission(self):
        queryset = self._perform_document_version_page_search()
        self.assertFalse(
            self.test_document.version_active.pages.first() in queryset
        )

    def test_document_version_page_search_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_view
        )

        queryset = self._perform_document_version_page_search()
        self.assertTrue(
            self.test_document.version_active.pages.first() in queryset
        )

    def test_trashed_document_version_page_search_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_view
        )
        self.test_document.delete()

        queryset = self._perform_document_version_page_search()
        self.assertFalse(
            self.test_document.version_active.pages.first() in queryset
        )
