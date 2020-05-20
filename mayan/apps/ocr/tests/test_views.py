from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..models import DocumentPageOCRContent
from ..permissions import (
    permission_ocr_content_view, permission_ocr_document,
    permission_document_type_ocr_setup
)
from ..utils import get_instance_ocr_content

from .literals import TEST_DOCUMENT_CONTENT
from .mixins import DocumentOCRViewTestMixin, DocumentTypeOCRViewTestMixin


class DocumentOCRViewsTestCase(
    DocumentOCRViewTestMixin, GenericDocumentViewTestCase
):
    # PyOCR's leak descriptor in get_available_languages and image_to_string
    # Disable descriptor leak test until fixed in upstream
    _skip_file_descriptor_test = True

    def test_document_content_view_no_permissions(self):
        self.test_document.submit_for_ocr()

        response = self._request_document_content_view()
        self.assertEqual(response.status_code, 404)

    def test_document_content_view_with_access(self):
        self.test_document.submit_for_ocr()
        self.grant_access(
            obj=self.test_document, permission=permission_ocr_content_view
        )

        response = self._request_document_content_view()
        self.assertContains(
            response=response, text=TEST_DOCUMENT_CONTENT, status_code=200
        )

    def test_document_content_delete_view_no_permissions(self):
        self.test_document.submit_for_ocr()

        response = self._request_document_content_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            DocumentPageOCRContent.objects.filter(
                document_page=self.test_document.pages.first()
            ).exists()
        )

    def test_document_content_delete_view_with_access(self):
        self.test_document.submit_for_ocr()
        self.grant_access(
            obj=self.test_document, permission=permission_ocr_document
        )

        response = self._request_document_content_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            DocumentPageOCRContent.objects.filter(
                document_page=self.test_document.pages.first()
            ).exists()
        )

    def test_document_page_content_view_no_permissions(self):
        self.test_document.submit_for_ocr()

        response = self._request_document_page_content_view()
        self.assertEqual(response.status_code, 404)

    def test_document_page_content_view_with_access(self):
        self.test_document.submit_for_ocr()
        self.grant_access(
            obj=self.test_document, permission=permission_ocr_content_view
        )

        response = self._request_document_page_content_view()
        self.assertContains(
            response=response, text=TEST_DOCUMENT_CONTENT, status_code=200
        )

    def test_document_submit_view_no_permission(self):
        response = self._request_document_submit_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            ''.join(self.test_document.latest_version.ocr_content()), ''
        )

    def test_document_submit_view_with_access(self):
        self.grant_access(
            permission=permission_ocr_document, obj=self.test_document
        )
        response = self._request_document_submit_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            TEST_DOCUMENT_CONTENT in ''.join(
                self.test_document.latest_version.ocr_content()
            )
        )

    def test_multiple_document_submit_view_no_permission(self):
        response = self._request_multiple_document_submit_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            ''.join(self.test_document.latest_version.ocr_content()), ''
        )

    def test_multiple_document_submit_view_with_access(self):
        self.grant_access(
            permission=permission_ocr_document, obj=self.test_document
        )
        response = self._request_multiple_document_submit_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            TEST_DOCUMENT_CONTENT in ''.join(
                self.test_document.latest_version.ocr_content()
            )
        )

    def test_document_ocr_download_view_no_permission(self):
        self.test_document.submit_for_ocr()

        response = self._request_document_ocr_download_view()
        self.assertEqual(response.status_code, 404)

    def test_document_ocr_download_view_with_access(self):
        self.test_document.submit_for_ocr()
        self.expected_content_types = ('text/html; charset=utf-8',)

        self.grant_access(
            obj=self.test_document, permission=permission_ocr_content_view
        )

        response = self._request_document_ocr_download_view()
        self.assertEqual(response.status_code, 200)

        self.assert_download_response(
            response=response, content=(
                ''.join(get_instance_ocr_content(instance=self.test_document))
            ),
        )


class DocumentTypeOCRViewsTestCase(
    DocumentTypeOCRViewTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_document_type_ocr_settings_view_no_permission(self):
        response = self._request_document_type_ocr_settings_view()
        self.assertEqual(response.status_code, 404)

    def test_document_type_ocr_settings_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_ocr_setup
        )

        response = self._request_document_type_ocr_settings_view()
        self.assertEqual(response.status_code, 200)
