from mayan.apps.dynamic_search.tests.mixins import SearchTestMixin

from ..permissions import (
    permission_document_file_view, permission_document_view,
    permission_document_version_view
)
from ..search import (
    document_file_page_search, document_file_search,
    document_search, document_version_page_search, document_version_search
)

from .base import GenericDocumentViewTestCase


class DocumentSearchTestCase(SearchTestMixin, GenericDocumentViewTestCase):
    _test_search_index_object_name = 'test_document'
    _test_search_model = document_search

    def test_document_search_no_permission(self):
        self._clear_events()

        queryset = self.do_test_search(terms=self.test_document.label)
        self.assertFalse(self.test_document in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_search_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        queryset = self.do_test_search(terms=self.test_document.label)
        self.assertTrue(self.test_document in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_search_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self.do_test_search(terms=self.test_document.label)
        self.assertTrue(self.test_document not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentFileSearchTestCase(
    SearchTestMixin, GenericDocumentViewTestCase
):
    _test_search_index_object_name = 'test_document_file'
    _test_search_model = document_file_search

    def test_document_file_search_no_permission(self):
        self._clear_events()

        queryset = self.do_test_search(terms=self.test_document.label)
        self.assertTrue(self.test_document_file not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_search_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self._clear_events()

        queryset = self.do_test_search(terms=self.test_document.label)
        self.assertTrue(self.test_document_file in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_file_search_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self.do_test_search(terms=self.test_document.label)
        self.assertTrue(self.test_document_file not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentFilePageSearchTestCase(
    SearchTestMixin, GenericDocumentViewTestCase
):
    _test_search_index_object_name = 'test_document_file_page'
    _test_search_model = document_file_page_search

    def test_document_file_page_search_no_permission(self):
        self._clear_events()

        queryset = self.do_test_search(terms=self.test_document.label)
        self.assertTrue(self.test_document_file_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_page_search_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self._clear_events()

        queryset = self.do_test_search(terms=self.test_document.label)
        self.assertTrue(self.test_document_file_page in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_file_page_search_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self.do_test_search(terms=self.test_document.label)
        self.assertTrue(self.test_document_file_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentVersionSearchTestCase(
    SearchTestMixin, GenericDocumentViewTestCase
):
    _test_search_index_object_name = 'test_document_version'
    _test_search_model = document_version_search

    def test_document_version_search_no_permission(self):
        self._clear_events()

        queryset = self.do_test_search(terms=self.test_document.label)
        self.assertTrue(self.test_document_version not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_search_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_view
        )

        self._clear_events()

        queryset = self.do_test_search(terms=self.test_document.label)
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

        queryset = self.do_test_search(terms=self.test_document.label)
        self.assertTrue(self.test_document_version not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentVersionPageSearchTestCase(
    SearchTestMixin, GenericDocumentViewTestCase
):
    _test_search_index_object_name = 'test_document_version_page'
    _test_search_model = document_version_page_search

    def test_document_version_page_search_no_permission(self):
        self._clear_events()

        queryset = self.do_test_search(terms=self.test_document.label)
        self.assertTrue(self.test_document_version_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_page_search_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_view
        )

        self._clear_events()

        queryset = self.do_test_search(terms=self.test_document.label)
        self.assertTrue(self.test_document_version_page in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_version_page_search_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_view
        )
        self.test_document.delete()

        self._clear_events()

        queryset = self.do_test_search(terms=self.test_document.label)
        self.assertTrue(self.test_document_version_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
