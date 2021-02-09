from rest_framework import status

from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from .mixins import (
    DuplicatedDocumentAPIViewTestMixin, DuplicatedDocumentTestMixin
)


class DuplicatedDocumentAPIViewTestCase(
    DocumentTestMixin, DuplicatedDocumentAPIViewTestMixin,
    DuplicatedDocumentTestMixin, BaseAPITestCase
):
    _test_event_object_name = 'test_document'

    def setUp(self):
        super().setUp()
        self._upload_duplicate_document()

    def test_duplicated_document_list_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_duplicated_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_duplicated_document_list_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_duplicated_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['id'],
            self.test_document.pk
        )

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_document_duplicates_list_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_duplicates_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_document_duplicates_list_api_view_with_source_document_access(self):
        self.grant_access(
            obj=self.test_documents[0], permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_document_duplicates_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_document_duplicates_list_api_view_with_target_document_access(self):
        self.grant_access(
            obj=self.test_documents[1], permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_document_duplicates_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_document_duplicates_list_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_documents[0], permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_documents[1], permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_document_duplicates_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['id'],
            self.test_documents[1].pk
        )

        event = self._get_test_object_event()
        self.assertEqual(event, None)
