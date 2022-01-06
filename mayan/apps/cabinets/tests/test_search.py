from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.search import document_search
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.dynamic_search.tests.mixins import SearchTestMixin

from ..permissions import permission_cabinet_view
from ..search import cabinet_search

from .mixins import CabinetTestMixin


class CabinetSearchTestCase(
    CabinetTestMixin, SearchTestMixin, GenericDocumentViewTestCase
):
    auto_create_test_cabinet = True
    test_cabinet_add_test_document = True

    def _do_test_search(self):
        return self.search_backend.search(
            search_model=cabinet_search, query={
                'documents__label': self.test_document.label
            }, user=self._test_case_user
        )

    def test_cabinet_search_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search()
        self.assertTrue(self.test_cabinet not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_search_with_access(self):
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view
        )

        self._clear_events()

        queryset = self._do_test_search()
        self.assertTrue(self.test_cabinet in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_cabinet_search_with_access(self):
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search()
        self.assertTrue(self.test_cabinet in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentCabinetSearchTestCase(
    CabinetTestMixin, SearchTestMixin, GenericDocumentViewTestCase
):
    auto_create_test_cabinet = True
    test_cabinet_add_test_document = True

    def _do_test_search(self):
        return self.search_backend.search(
            search_model=document_search, query={
                'cabinets__label': self.test_cabinet.label
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
