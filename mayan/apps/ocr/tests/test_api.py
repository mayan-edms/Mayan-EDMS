from rest_framework import status

from mayan.apps.documents.tests.mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..permissions import (
    permission_document_type_ocr_setup, permission_ocr_document,
    permission_ocr_content_view
)

from .literals import TEST_DOCUMENT_CONTENT
from .mixins import (
    DocumentTypeOCRSettingsAPIViewTestMixin, OCRAPIViewTestMixin
)


class DocumentTypeOCRSettingsAPIViewTestCase(
    DocumentTestMixin, DocumentTypeOCRSettingsAPIViewTestMixin,
    BaseAPITestCase
):
    auto_upload_test_document = False

    def test_document_type_ocr_settings_details_api_view_no_permission(self):
        response = self._request_document_type_ocr_settings_details_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_type_ocr_settings_details_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_ocr_setup
        )

        response = self._request_document_type_ocr_settings_details_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'auto_ocr': False})

    def test_document_type_ocr_settings_patch_api_view_no_permission(self):
        response = self._request_document_type_ocr_settings_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_type_ocr_settings_patch_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_ocr_setup
        )

        response = self._request_document_type_ocr_settings_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'auto_ocr': True})

    def test_document_type_ocr_settings_put_api_view_no_permission(self):
        response = self._request_document_type_ocr_settings_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_type_ocr_settings_put_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_ocr_setup
        )

        response = self._request_document_type_ocr_settings_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'auto_ocr': True})


class OCRAPIViewTestCase(
    DocumentTestMixin, OCRAPIViewTestMixin, BaseAPITestCase
):
    def test_submit_document_api_view_no_permission(self):
        response = self._request_document_ocr_submit_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertFalse(
            hasattr(self.test_document.pages.first(), 'ocr_content')
        )

    def test_submit_document_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_ocr_document
        )
        response = self._request_document_ocr_submit_view()
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.assertTrue(
            hasattr(self.test_document.pages.first(), 'ocr_content')
        )

    def test_submit_document_version_api_view_no_permission(self):
        response = self._request_document_version_ocr_submit_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertFalse(
            hasattr(self.test_document.pages.first(), 'ocr_content')
        )

    def test_submit_document_version_api_view_with_access(self):
        self.grant_access(
            permission=permission_ocr_document, obj=self.test_document
        )
        response = self._request_document_version_ocr_submit_view()
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.assertTrue(
            hasattr(self.test_document.pages.first(), 'ocr_content')
        )

    def test_get_document_version_page_content_api_view_no_permission(self):
        response = self._request_document_page_content_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_document_version_page_content_api_view_with_access(self):
        self.test_document.submit_for_ocr()
        self.grant_access(
            permission=permission_ocr_content_view, obj=self.test_document
        )
        response = self._request_document_page_content_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            TEST_DOCUMENT_CONTENT in response.data['content']
        )
