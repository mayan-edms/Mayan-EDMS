from django.test import override_settings

from rest_framework import status

from mayan.apps.documents.tests.literals import TEST_HYBRID_DOCUMENT
from mayan.apps.documents.tests.mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..permissions import (
    permission_content_view, permission_document_type_parsing_setup
)

from .literals import TEST_DOCUMENT_CONTENT
from .mixins import (
    DocumentParsingAPITestMixin, DocumentTypeParsingSettingsAPIViewTestMixin
)


@override_settings(DOCUMENT_PARSING_AUTO_PARSING=True)
class DocumentParsingAPITestCase(
    DocumentParsingAPITestMixin, DocumentTestMixin, BaseAPITestCase
):
    test_document_filename = TEST_HYBRID_DOCUMENT

    def test_get_document_version_page_content_no_permission(self):
        response = self._request_document_page_content_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_document_version_page_content_with_access(self):
        self.grant_access(
            permission=permission_content_view, obj=self.test_document
        )

        response = self._request_document_page_content_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(
            TEST_DOCUMENT_CONTENT in response.data['content']
        )


class DocumentTypeParsingSettingsAPIViewTestCase(
    DocumentTestMixin, DocumentTypeParsingSettingsAPIViewTestMixin,
    BaseAPITestCase
):
    auto_upload_test_document = False

    def test_document_type_parsing_settings_details_api_view_no_permission(self):
        response = self._request_document_type_parsing_settings_details_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_type_parsing_settings_details_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_parsing_setup
        )

        response = self._request_document_type_parsing_settings_details_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'auto_parsing': False})

    def test_document_type_parsing_settings_patch_api_view_no_permission(self):
        response = self._request_document_type_parsing_settings_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_type_parsing_settings_patch_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_parsing_setup
        )

        response = self._request_document_type_parsing_settings_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'auto_parsing': True})

    def test_document_type_parsing_settings_put_api_view_no_permission(self):
        response = self._request_document_type_parsing_settings_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_type_parsing_settings_put_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_parsing_setup
        )

        response = self._request_document_type_parsing_settings_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'auto_parsing': True})
