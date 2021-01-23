from django.test import override_settings

from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.documents.tests.literals import TEST_HYBRID_DOCUMENT

from ..models import DocumentFilePageContent
from ..permissions import (
    permission_document_file_content_view, permission_document_file_parse,
    permission_document_type_parsing_setup
)
from ..utils import get_document_file_content

from .literals import TEST_DOCUMENT_CONTENT
from .mixins import (
    DocumentFileContentToolsViewsTestMixin, DocumentFileContentViewTestMixin,
    DocumentTypeContentViewsTestMixin
)


@override_settings(DOCUMENT_PARSING_AUTO_PARSING=True)
class DocumentFileContentViewsTestCase(
    DocumentFileContentViewTestMixin, GenericDocumentViewTestCase
):
    _skip_file_descriptor_test = True
    # Ensure we use a PDF file
    test_document_filename = TEST_HYBRID_DOCUMENT

    def test_document_file_content_view_no_permission(self):
        response = self._request_test_document_file_content_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_content_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_content_view
        )

        response = self._request_test_document_file_content_view()
        self.assertContains(
            response=response, text=TEST_DOCUMENT_CONTENT, status_code=200
        )

    def test_document_file_content_delete_view_no_permission(self):
        response = self._request_test_document_file_content_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            DocumentFilePageContent.objects.filter(
                document_file_page=self.test_document_file.pages.first()
            ).exists()
        )

    def test_document_file_content_delete_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_parse
        )

        response = self._request_test_document_file_content_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            DocumentFilePageContent.objects.filter(
                document_file_page=self.test_document_file.pages.first()
            ).exists()
        )

    def test_document_file_page_content_view_no_permission(self):
        response = self._request_test_document_file_page_content_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_page_content_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_content_view
        )
        response = self._request_test_document_file_page_content_view()
        self.assertContains(
            response=response, text=TEST_DOCUMENT_CONTENT, status_code=200
        )

    def test_trashed_document_file_page_content_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_content_view
        )

        self.test_document.delete()

        response = self._request_test_document_file_page_content_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_parsing_download_view_no_permission(self):
        response = self._request_test_document_file_content_download_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_parsing_download_view_with_access(self):
        self.expected_content_types = ('text/html; charset=utf-8',)
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_content_view
        )

        response = self._request_test_document_file_content_download_view()
        self.assertEqual(response.status_code, 200)

        self.assert_download_response(
            response=response, content=(
                ''.join(
                    get_document_file_content(
                        document_file=self.test_document_file
                    )
                )
            ),
        )

    def test_trashed_document_file_parsing_download_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_content_view
        )

        self.test_document.delete()

        response = self._request_test_document_file_content_download_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_parsing_error_list_view_no_permission(self):
        response = self._request_test_document_file_parsing_error_list_view()

        self.assertEqual(response.status_code, 404)

    def test_document_file_parsing_error_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_parse
        )

        response = self._request_test_document_file_parsing_error_list_view()
        self.assertEqual(response.status_code, 200)

    def test_trashed_document_file_parsing_error_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_parse
        )

        self.test_document.delete()

        response = self._request_test_document_file_parsing_error_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_parsing_submit_view_no_permission(self):
        response = self._request_test_document_file_parsing_submit_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_parsing_submit_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_parse
        )

        response = self._request_test_document_file_parsing_submit_view()
        self.assertEqual(response.status_code, 302)

    def test_trashed_document_file_parsing_submit_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_parse
        )

        self.test_document.delete()

        response = self._request_test_document_file_parsing_submit_view()
        self.assertEqual(response.status_code, 404)


class DocumentTypeParsingViewsTestCase(
    DocumentFileContentToolsViewsTestMixin, GenericDocumentViewTestCase
):
    _skip_file_descriptor_test = True
    auto_upload_test_document = False

    # Ensure we use a PDF file
    test_document_filename = TEST_HYBRID_DOCUMENT

    def _get_document_file_content(self):
        return ''.join(
            list(
                get_document_file_content(
                    document_file=self.test_document_file
                )
            )
        )

    def test_document_parsing_error_list_view_no_permission(self):
        response = self._request_document_parsing_error_list_view()
        self.assertEqual(response.status_code, 403)

    def test_document_parsing_error_list_view_with_permission(self):
        self.grant_permission(permission=permission_document_file_parse)

        response = self._request_document_parsing_error_list_view()
        self.assertEqual(response.status_code, 200)

    def test_document_type_parsing_view_no_permission(self):
        self._upload_test_document()

        response = self._request_document_type_parsing_view()
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_document_type.label
        )

        self.assertNotEqual(
            self._get_document_file_content(), TEST_DOCUMENT_CONTENT
        )

    def test_document_type_parsing_view_with_permission(self):
        self.grant_permission(permission=permission_document_file_parse)

        self._upload_test_document()

        response = self._request_document_type_parsing_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self._get_document_file_content(), TEST_DOCUMENT_CONTENT
        )


class DocumentTypeContentViewsTestCase(
    DocumentTypeContentViewsTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_document_type_parsing_settings_view_no_permission(self):
        response = self._request_test_document_type_parsing_settings_view()
        self.assertEqual(response.status_code, 404)

    def test_document_type_parsing_settings_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_parsing_setup
        )

        response = self._request_test_document_type_parsing_settings_view()
        self.assertEqual(response.status_code, 200)
