from django.test import override_settings

from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.documents.tests.literals import TEST_HYBRID_DOCUMENT

from ..models import DocumentPageContent
from ..permissions import (
    permission_content_view, permission_document_type_parsing_setup,
    permission_parse_document
)
from ..utils import get_instance_content

from .literals import TEST_DOCUMENT_CONTENT
from .mixins import (
    DocumentContentToolsViewsTestMixin, DocumentContentViewTestMixin,
    DocumentTypeContentViewsTestMixin
)


@override_settings(DOCUMENT_PARSING_AUTO_PARSING=True)
class DocumentContentViewsTestCase(
    DocumentContentViewTestMixin, GenericDocumentViewTestCase
):
    _skip_file_descriptor_test = True

    # Ensure we use a PDF file
    test_document_filename = TEST_HYBRID_DOCUMENT

    def test_document_content_view_no_permissions(self):
        response = self._request_test_document_content_view()
        self.assertEqual(response.status_code, 404)

    def test_document_content_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_content_view
        )

        response = self._request_test_document_content_view()
        self.assertContains(
            response=response, text=TEST_DOCUMENT_CONTENT, status_code=200
        )

    def test_document_content_delete_view_no_permissions(self):
        response = self._request_test_document_content_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            DocumentPageContent.objects.filter(
                document_page=self.test_document.pages.first()
            ).exists()
        )

    def test_document_content_delete_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_parse_document
        )

        response = self._request_test_document_content_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            DocumentPageContent.objects.filter(
                document_page=self.test_document.pages.first()
            ).exists()
        )

    def test_document_page_content_view_no_permissions(self):
        response = self._request_test_document_page_content_view()
        self.assertEqual(response.status_code, 404)

    def test_document_page_content_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_content_view
        )

        response = self._request_test_document_page_content_view()
        self.assertContains(
            response=response, text=TEST_DOCUMENT_CONTENT, status_code=200
        )

    def test_document_parsing_download_view_no_permission(self):
        response = self._request_test_document_content_download_view()
        self.assertEqual(response.status_code, 404)

    def test_document_parsing_download_view_with_access(self):
        self.expected_content_types = ('text/html; charset=utf-8',)
        self.grant_access(
            obj=self.test_document, permission=permission_content_view
        )

        response = self._request_test_document_content_download_view()
        self.assertEqual(response.status_code, 200)

        self.assert_download_response(
            response=response, content=(
                ''.join(get_instance_content(document=self.test_document))
            ),
        )

    def test_document_parsing_error_list_view_no_permission(self):
        response = self._request_test_document_parsing_error_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_parsing_error_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_parse_document
        )

        response = self._request_test_document_parsing_error_list_view()
        self.assertEqual(response.status_code, 200)


class DocumentTypeContentViewsTestCase(
    DocumentTypeContentViewsTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_document_type_parsing_settings_view_no_permission(self):
        response = self._request_test_document_type_parsing_settings()
        self.assertEqual(response.status_code, 404)

    def test_document_type_parsing_settings_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_parsing_setup
        )

        response = self._request_test_document_type_parsing_settings()
        self.assertEqual(response.status_code, 200)


class DocumentContentToolsViewsTestCase(
    DocumentContentToolsViewsTestMixin, GenericDocumentViewTestCase
):
    _skip_file_descriptor_test = True
    auto_upload_test_document = False

    # Ensure we use a PDF file
    test_document_filename = TEST_HYBRID_DOCUMENT

    def _get_instance_content(self):
        return ''.join(
            list(get_instance_content(document=self.test_document))
        )

    def test_document_parsing_error_list_view_no_permission(self):
        response = self._request_document_parsing_error_list_view()
        self.assertEqual(response.status_code, 403)

    def test_document_parsing_error_list_view_with_permission(self):
        self.grant_permission(permission=permission_parse_document)

        response = self._request_document_parsing_error_list_view()
        self.assertEqual(response.status_code, 200)

    def test_document_parsing_tool_view_no_permission(self):
        self._upload_test_document()

        response = self._request_document_parsing_tool_view()
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_document_type.label
        )

        self.assertNotEqual(
            self._get_instance_content(), TEST_DOCUMENT_CONTENT
        )

    def test_document_parsing_tool_view_with_permission(self):
        self.grant_permission(permission=permission_parse_document)

        self._upload_test_document()

        response = self._request_document_parsing_tool_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self._get_instance_content(), TEST_DOCUMENT_CONTENT
        )
