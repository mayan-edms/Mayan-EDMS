from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..models.favorite_document_models import FavoriteDocument
from ..permissions import permission_document_view

from .mixins.document_mixins import DocumentTestMixin
from .mixins.favorite_document_mixins import (
    FavoriteDocumentAPIViewTestMixin, FavoriteDocumentTestMixin
)


class FavoriteDocumentAPIViewTestCase(
    FavoriteDocumentAPIViewTestMixin, FavoriteDocumentTestMixin,
    DocumentTestMixin, BaseAPITestCase
):
    def test_favorite_document_create_api_view_no_permission(self):
        favorite_document_count = FavoriteDocument.objects.count()

        self._clear_events()

        response = self._request_test_favorite_document_create_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            FavoriteDocument.objects.count(), favorite_document_count
        )
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_favorite_document_create_api_view_with_access(self):
        favorite_document_count = FavoriteDocument.objects.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_favorite_document_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            FavoriteDocument.objects.count(), favorite_document_count + 1
        )
        self.assertEqual(
            self.test_favorite_document.document.pk, self.test_document.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_favorite_document_delete_api_view_no_permission(self):
        self._test_document_favorite_add()

        favorite_document_count = FavoriteDocument.objects.count()

        self._clear_events()

        response = self._request_test_favorite_document_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            FavoriteDocument.objects.count(), favorite_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_favorite_document_delete_api_view_with_access(self):
        self._test_document_favorite_add()

        favorite_document_count = FavoriteDocument.objects.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_favorite_document_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(
            FavoriteDocument.objects.count(), favorite_document_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_favorite_document_detail_api_view_no_permission(self):
        self._test_document_favorite_add()

        self._clear_events()

        response = self._request_test_favorite_document_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_favorite_document_detail_api_view_with_access(self):
        self._test_document_favorite_add()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_favorite_document_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['document']['label'],
            self.test_document.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_favorite_document_list_api_view_no_permission(self):
        self._test_document_favorite_add()

        favorite_document_count = FavoriteDocument.objects.count()

        self._clear_events()

        response = self._request_test_favorite_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], favorite_document_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_favorite_document_list_api_view_with_access(self):
        self._test_document_favorite_add()

        favorite_document_count = FavoriteDocument.objects.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_favorite_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], favorite_document_count)
        self.assertEqual(
            response.data['results'][0]['document']['label'],
            self.test_document.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
