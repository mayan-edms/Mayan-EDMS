from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.documents.permissions import (
    permission_document_version_view, permission_document_view
)
from mayan.apps.documents.search import (
    document_version_page_search, document_search, document_version_search
)
from mayan.apps.dynamic_search.tests.mixins import SearchTestMixin

from .mixins import DocumentVersionOCRTestMixin


class DocumentOCRSearchTestCase(
    DocumentVersionOCRTestMixin, SearchTestMixin, GenericDocumentViewTestCase
):
    auto_create_test_document_version_ocr_content = True

    def _do_test_search(self):
        return self.search_backend.search(
            search_model=document_search, query={
                'versions__version_pages__ocr_content__content': self.test_document_version_page.ocr_content.content
            }, user=self._test_case_user
        )

    def test_document_search_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search()
        self.assertTrue(self.test_document not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_search_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        queryset = self._do_test_search()
        self.assertTrue(self.test_document in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_search_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search()
        self.assertTrue(self.test_document not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentVersionOCRSearchTestCase(
    DocumentVersionOCRTestMixin, SearchTestMixin, GenericDocumentViewTestCase
):
    auto_create_test_document_version_ocr_content = True

    def _do_test_search(self):
        return self.search_backend.search(
            search_model=document_version_search, query={
                'version_pages__ocr_content__content': self.test_document_version_page.ocr_content.content
            }, user=self._test_case_user
        )

    def test_document_version_search_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search()
        self.assertTrue(self.test_document_version not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_search_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_view
        )

        self._clear_events()

        queryset = self._do_test_search()
        self.assertTrue(self.test_document_version in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_version_search_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search()
        self.assertTrue(self.test_document_version not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentVersionPageOCRSearchTestCase(
    DocumentVersionOCRTestMixin, SearchTestMixin, GenericDocumentViewTestCase
):
    auto_create_test_document_version_ocr_content = True

    def _do_test_search(self):
        return self.search_backend.search(
            search_model=document_version_page_search, query={
                'ocr_content__content': self.test_document_version_page.ocr_content.content
            }, user=self._test_case_user
        )

    def test_document_version_search_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search()
        self.assertTrue(self.test_document_version_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_search_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_view
        )

        self._clear_events()

        queryset = self._do_test_search()
        self.assertTrue(self.test_document_version_page in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_version_search_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search()
        self.assertTrue(self.test_document_version_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
