from rest_framework import status

from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..permissions import (
    permission_document_file_content_view,
    permission_document_type_parsing_setup
)

from .mixins import (
    DocumentFilePageContentAPITestMixin,
    DocumentTypeParsingSettingsAPIViewTestMixin
)


class DocumentFilePageContentAPITestCase(
    DocumentFilePageContentAPITestMixin, DocumentTestMixin, BaseAPITestCase
):
    def test_document_file_page_content_api_view_no_permission(self):
        self._clear_events()

        response = self._request_document_file_page_content_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_page_content_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_content_view
        )

        self._clear_events()

        response = self._request_document_file_page_content_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_file_page_content_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_content_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_document_file_page_content_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentTypeParsingSettingsAPIViewTestCase(
    DocumentTestMixin, DocumentTypeParsingSettingsAPIViewTestMixin,
    BaseAPITestCase
):
    auto_upload_test_document = False

    def test_document_type_parsing_settings_details_api_view_no_permission(self):
        self._clear_events()

        response = self._request_document_type_parsing_settings_details_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_parsing_settings_details_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_parsing_setup
        )

        self._clear_events()

        response = self._request_document_type_parsing_settings_details_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'auto_parsing': False})

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_parsing_settings_patch_api_view_no_permission(self):
        self._clear_events()

        response = self._request_document_type_parsing_settings_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_parsing_settings_patch_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_parsing_setup
        )

        self._clear_events()

        response = self._request_document_type_parsing_settings_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'auto_parsing': True})

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_parsing_settings_put_api_view_no_permission(self):
        self._clear_events()

        response = self._request_document_type_parsing_settings_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_parsing_settings_put_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_parsing_setup
        )

        self._clear_events()

        response = self._request_document_type_parsing_settings_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'auto_parsing': True})

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
