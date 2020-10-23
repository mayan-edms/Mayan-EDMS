from django.utils.encoding import force_text

from ..permissions import (
    permission_document_download, permission_document_version_revert,
    permission_document_version_view,
)

from .base import GenericDocumentViewTestCase
from .literals import TEST_VERSION_COMMENT
from .mixins import DocumentVersionTestMixin, DocumentVersionViewTestMixin


class DocumentVersionViewTestCase(
    DocumentVersionTestMixin, DocumentVersionViewTestMixin,
    GenericDocumentViewTestCase
):
    def test_document_version_download_view_no_permission(self):
        response = self._request_document_version_download()
        self.assertEqual(response.status_code, 404)

    def test_document_version_download_view_with_permission(self):
        # Set the expected_content_types for
        # common.tests.mixins.ContentTypeCheckMixin
        self.expected_content_types = (
            self.test_document.latest_version.mimetype,
        )

        self.grant_access(
            obj=self.test_document, permission=permission_document_download
        )

        response = self._request_document_version_download()
        self.assertEqual(response.status_code, 200)

        with self.test_document.open() as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
                filename=force_text(s=self.test_document.latest_version),
                mime_type=self.test_document.latest_version.mimetype
            )

    def test_document_version_download_preserve_extension_view_with_permission(self):
        # Set the expected_content_types for
        # common.tests.mixins.ContentTypeCheckMixin
        self.expected_content_types = (
            self.test_document.latest_version.mimetype,
        )

        self.grant_access(
            obj=self.test_document, permission=permission_document_download
        )

        response = self._request_document_version_download(
            data={'preserve_extension': True}
        )
        self.assertEqual(response.status_code, 200)

        with self.test_document.open() as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
                filename=self.test_document.latest_version.get_rendered_string(
                    preserve_extension=True
                ), mime_type=self.test_document.latest_version.mimetype
            )

    def test_document_version_list_no_permission(self):
        self._upload_new_version()

        response = self._request_document_version_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_version_list_with_access(self):
        self._upload_new_version()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_view
        )

        response = self._request_document_version_list_view()
        self.assertContains(
            response=response, status_code=200, text=TEST_VERSION_COMMENT
        )

    def test_document_version_revert_no_permission(self):
        first_version = self.test_document.latest_version
        self._upload_new_version()

        response = self._request_document_version_revert_view(
            document_version=first_version
        )
        self.assertEqual(response.status_code, 404)

        self.assertEqual(self.test_document.versions.count(), 2)

    def test_document_version_revert_with_access(self):
        first_version = self.test_document.latest_version
        self._upload_new_version()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_revert
        )

        response = self._request_document_version_revert_view(
            document_version=first_version
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.test_document.versions.count(), 1)
