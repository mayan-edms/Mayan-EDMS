from rest_framework import status

from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..permissions import permission_document_type_ocr_setup

from .mixins import DocumentTypeOCRSettingsAPIViewTestMixin


class DocumentTypeOCRSettingsAPIViewTestCase(
    DocumentTestMixin, DocumentTypeOCRSettingsAPIViewTestMixin,
    BaseAPITestCase
):
    auto_upload_test_document = False

    def test_document_type_ocr_settings_details_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_type_ocr_settings_details_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_ocr_settings_details_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_ocr_setup
        )

        self._clear_events()

        response = self._request_test_document_type_ocr_settings_details_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'auto_ocr': False})

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_ocr_settings_patch_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_type_ocr_settings_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_ocr_settings_patch_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_ocr_setup
        )

        self._clear_events()

        response = self._request_test_document_type_ocr_settings_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'auto_ocr': True})

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_ocr_settings_put_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_type_ocr_settings_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_ocr_settings_put_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_ocr_setup
        )

        self._clear_events()

        response = self._request_test_document_type_ocr_settings_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'auto_ocr': True})

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
