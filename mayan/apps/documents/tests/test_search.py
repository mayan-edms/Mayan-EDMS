from django.utils.module_loading import import_string

from ..permissions import permission_document_view
from ..search import document_search, document_page_search

from .base import GenericDocumentViewTestCase


class DocumentSearchTestMixin:
    search_backend = import_string(
        dotted_path='mayan.apps.dynamic_search.backends.django.DjangoSearchBackend'
    )()

    def _perform_document_page_search(self):
        return self.search_backend.search(
            search_model=document_page_search, query_string={'q': self.test_document.label},
            user=self._test_case_user
        )

    def _perform_document_search(self):
        return self.search_backend.search(
            search_model=document_search, query_string={'q': self.test_document.label},
            user=self._test_case_user
        )


class DocumentSearchTestCase(
    DocumentSearchTestMixin, GenericDocumentViewTestCase
):
    def test_document_page_search_no_permission(self):
        queryset = self._perform_document_page_search()
        self.assertFalse(self.test_document.pages.first() in queryset)

    def test_document_page_search_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        queryset = self._perform_document_page_search()
        self.assertTrue(self.test_document.pages.first() in queryset)

    def test_document_search_no_permission(self):
        queryset = self._perform_document_search()
        self.assertFalse(self.test_document in queryset)

    def test_document_search_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        queryset = self._perform_document_search()
        self.assertTrue(self.test_document in queryset)
