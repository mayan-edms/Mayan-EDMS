from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..models.recently_accessed_document_models import RecentlyAccessedDocument
from ..permissions import permission_document_view

from .mixins.document_mixins import DocumentTestMixin
from .mixins.recently_accessed_document_mixins import (
    RecentlyAccessedDocumentAPIViewTestMixin
)


class RecentlyAccessedDocumentAPIViewTestCase(
    DocumentTestMixin, RecentlyAccessedDocumentAPIViewTestMixin,
    BaseAPITestCase
):
    def test_recently_accessed_document_api_list_view_no_activity(self):
        recently_accessed_document_count = RecentlyAccessedDocument.objects.count()

        self._clear_events()

        response = self._request_recently_accessed_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        self.assertEqual(
            RecentlyAccessedDocument.objects.count(),
            recently_accessed_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_recently_accessed_document_api_list_view_with_activity_no_permission(self):
        recently_accessed_document_count = RecentlyAccessedDocument.objects.count()

        self.test_document.add_as_recent_document_for_user(
            user=self._test_case_user
        )

        self._clear_events()

        response = self._request_recently_accessed_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        self.assertEqual(
            RecentlyAccessedDocument.objects.count(),
            recently_accessed_document_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_recently_accessed_document_api_list_view_with_activity_with_access(self):
        recently_accessed_document_count = RecentlyAccessedDocument.objects.count()

        self.test_document.add_as_recent_document_for_user(
            user=self._test_case_user
        )

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_recently_accessed_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['document']['id'], self.test_document.pk
        )

        self.assertEqual(
            RecentlyAccessedDocument.objects.count(),
            recently_accessed_document_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
