from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..models.document_models import RecentlyCreatedDocument
from ..permissions import permission_document_view

from .mixins.document_mixins import DocumentTestMixin
from .mixins.recently_created_document_mixins import (
    RecentlyCreatedDocumentAPIViewTestMixin
)


class RecentlyCreatedDocumentAPIViewTestCase(
    DocumentTestMixin, RecentlyCreatedDocumentAPIViewTestMixin,
    BaseAPITestCase
):
    _test_event_object_name = 'test_document'

    def test_recently_created_document_api_list_view_no_permission(self):
        recently_created_document_count = RecentlyCreatedDocument.objects.count()

        self._clear_events()

        response = self._request_recently_created_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['count'], recently_created_document_count - 1
        )

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_recently_created_document_api_list_view_with_access(self):
        recently_created_document_count = RecentlyCreatedDocument.objects.count()

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_recently_created_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['count'], recently_created_document_count
        )
        self.assertEqual(
            response.data['results'][0]['id'], self.test_document.pk
        )

        event = self._get_test_object_event()
        self.assertEqual(event, None)
