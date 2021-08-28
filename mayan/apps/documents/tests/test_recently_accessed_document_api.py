from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..permissions import permission_document_view

from .mixins.document_mixins import DocumentTestMixin
from .mixins.recently_accessed_document_mixins import (
    RecentlyAccessedDocumentAPIViewTestMixin
)


class RecentlyAccessedDocumentAPIViewTestCase(
    DocumentTestMixin, RecentlyAccessedDocumentAPIViewTestMixin,
    BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_recently_accessed_document_api_list_view_no_activity(self):
        self._clear_events()

        response = self._request_recently_accessed_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_recently_accessed_document_api_list_view_with_activity_no_permission(self):
        self.test_document.add_as_recent_document_for_user(
            user=self._test_case_user
        )

        self._clear_events()

        response = self._request_recently_accessed_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_recently_accessed_document_api_list_view_with_activity_with_access(self):
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
            response.data['results'][0]['document']['id'],
            self.test_document.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_recently_accessed_document_api_list_view_with_activity_with_access(self):
        self.test_document.add_as_recent_document_for_user(
            user=self._test_case_user
        )

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_recently_accessed_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
