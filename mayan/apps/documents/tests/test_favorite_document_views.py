from ..models import FavoriteDocument
from ..permissions import permission_document_view

from .base import GenericDocumentViewTestCase
from .mixins.favorite_document_mixins import (
    FavoriteDocumentTestMixin, FavoriteDocumentsViewTestMixin
)


class FavoriteDocumentsTestCase(
    FavoriteDocumentTestMixin, FavoriteDocumentsViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_document_favorite_add_view_no_permission(self):
        favorite_document_count = FavoriteDocument.valid.count()

        self._clear_events()

        response = self._request_test_document_favorite_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            FavoriteDocument.valid.count(), favorite_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_favorite_add_view_with_access(self):
        favorite_document_count = FavoriteDocument.valid.count()

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_document_favorite_add_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            FavoriteDocument.valid.count(), favorite_document_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_favorite_add_view_with_access(self):
        favorite_document_count = FavoriteDocument.valid.count()

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_favorite_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            FavoriteDocument.valid.count(), favorite_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_favorite_list_view_no_permission(self):
        self._test_document_favorite_add()

        self._clear_events()

        response = self._request_test_document_favorites_list_view()
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_favorite_list_view_with_access(self):
        self._test_document_favorite_add()
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_document_favorites_list_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_favorite_list_view_with_access(self):
        self._test_document_favorite_add()

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_favorites_list_view()

        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_favorite_remove_view_no_permission(self):
        self._test_document_favorite_add()

        favorite_document_count = FavoriteDocument.valid.count()

        self._clear_events()

        response = self._request_test_document_favorite_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            FavoriteDocument.valid.count(), favorite_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_favorite_remove_view_with_access(self):
        self._test_document_favorite_add()

        favorite_document_count = FavoriteDocument.valid.count()
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_document_favorite_remove_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            FavoriteDocument.valid.count(), favorite_document_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_favorite_remove_view_with_access(self):
        self._test_document_favorite_add()

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self.test_document.delete()

        favorite_document_count = FavoriteDocument.valid.count()

        self._clear_events()

        response = self._request_test_document_favorite_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            FavoriteDocument.valid.count(), favorite_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
