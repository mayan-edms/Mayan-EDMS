from django.utils.encoding import force_text

from ..permissions import (
    permission_document_download, permission_document_file_revert,
    permission_document_file_view,
)

from .base import GenericDocumentViewTestCase
from .literals import TEST_VERSION_COMMENT
from .mixins import DocumentFileTestMixin, DocumentFileViewTestMixin


class DocumentFileViewTestCase(
    DocumentFileTestMixin, DocumentFileViewTestMixin,
    GenericDocumentViewTestCase
):
    def test_document_file_download_view_no_permission(self):
        response = self._request_document_file_download()
        self.assertEqual(response.status_code, 404)

    def test_document_file_download_view_with_permission(self):
        # Set the expected_content_types for
        # common.tests.mixins.ContentTypeCheckMixin
        self.expected_content_types = (
            self.test_document.latest_file.mimetype,
        )

        self.grant_access(
            obj=self.test_document, permission=permission_document_download
        )

        response = self._request_document_file_download()
        self.assertEqual(response.status_code, 200)

        with self.test_document.open() as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
                filename=force_text(self.test_document.latest_file),
                mime_type=self.test_document.latest_file.mimetype
            )

    def test_document_file_download_preserve_extension_view_with_permission(self):
        # Set the expected_content_types for
        # common.tests.mixins.ContentTypeCheckMixin
        self.expected_content_types = (
            self.test_document.latest_file.mimetype,
        )

        self.grant_access(
            obj=self.test_document, permission=permission_document_download
        )

        response = self._request_document_file_download(
            data={'preserve_extension': True}
        )
        self.assertEqual(response.status_code, 200)

        with self.test_document.open() as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
                filename=self.test_document.latest_file.get_rendered_string(
                    preserve_extension=True
                ), mime_type=self.test_document.latest_file.mimetype
            )

    def test_document_file_list_no_permission(self):
        self._upload_new_file()

        response = self._request_document_file_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_list_with_access(self):
        self._upload_new_file()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_view
        )

        response = self._request_document_file_list_view()
        self.assertContains(
            response=response, status_code=200, text=TEST_VERSION_COMMENT
        )

    def test_document_file_revert_no_permission(self):
        first_file = self.test_document.latest_file
        self._upload_new_file()

        response = self._request_document_file_revert_view(
            document_file=first_file
        )
        self.assertEqual(response.status_code, 404)

        self.assertEqual(self.test_document.files.count(), 2)

    def test_document_file_revert_with_access(self):
        first_file = self.test_document.latest_file
        self._upload_new_file()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_revert
        )

        response = self._request_document_file_revert_view(
            document_file=first_file
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.test_document.files.count(), 1)
