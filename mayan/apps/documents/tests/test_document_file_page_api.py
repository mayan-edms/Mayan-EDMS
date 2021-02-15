from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..permissions import permission_document_file_view

from .mixins.document_mixins import DocumentTestMixin
from .mixins.document_file_mixins import DocumentFilePageAPIViewTestMixin


class DocumentFilePageAPIViewTestCase(
    DocumentFilePageAPIViewTestMixin, DocumentTestMixin, BaseAPITestCase
):
    def test_document_file_page_detail_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_file_page_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_page_detail_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_file,
            permission=permission_document_file_view
        )

        self._clear_events()

        response = self._request_test_document_file_page_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_page_image_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_file_page_image_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_page_image_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self._clear_events()

        response = self._request_test_document_file_page_image_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_page_list_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_file_page_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_page_list_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_file,
            permission=permission_document_file_view
        )

        self._clear_events()

        response = self._request_test_document_file_page_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['results'][0]['id'],
            self.test_document_file_page.id
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
