from django.utils.encoding import force_text

from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..permissions import (
    permission_document_file_delete, permission_document_file_download,
    permission_document_file_new, permission_document_file_view
)

from .mixins.document_mixins import DocumentTestMixin
from .mixins.document_file_mixins import (
    DocumentFileAPIViewTestMixin, DocumentFileTestMixin,
    DocumentFilePageAPIViewTestMixin
)


class DocumentFileAPIViewTestCase(
    DocumentFileAPIViewTestMixin, DocumentTestMixin,
    DocumentFileTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def test_document_file_download_api_view_no_permission(self):
        self._upload_test_document()

        response = self._request_test_document_file_download_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_file_download_api_view_with_access(self):
        self._upload_test_document()
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_download
        )

        response = self._request_test_document_file_download_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with self.test_document.file_latest.open() as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
                filename=force_text(s=self.test_document.file_latest),
                mime_type=self.test_document.file_latest.mimetype
            )

    def test_document_file_download_preserve_extension_api_view(self):
        self._upload_test_document()
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_download
        )

        response = self.get(
            viewname='rest_api:documentfile-download', kwargs={
                'document_id': self.test_document.pk,
                'document_file_id': self.test_document.file_latest.pk,
            }, data={'preserve_extension': True}
        )

        with self.test_document.file_latest.open() as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
                filename=self.test_document.file_latest.get_rendered_string(
                    preserve_extension=True
                ), mime_type=self.test_document.file_latest.mimetype
            )

    def test_document_file_list_api_view_no_permission(self):
        self._upload_test_document()
        self._upload_new_file()

        response = self._request_test_document_file_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_file_list_api_view_with_access(self):
        self._upload_test_document()
        self._upload_new_file()

        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )
        response = self._request_test_document_file_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['results'][1]['checksum'],
            self.test_document.file_latest.checksum
        )

    def test_document_file_delete_api_view_no_permission(self):
        self._upload_test_document()
        self._upload_new_file()

        response = self._request_test_document_file_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_file_delete_api_view_with_access(self):
        self._upload_test_document()
        self._upload_new_file()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_delete
        )

        response = self._request_test_document_file_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(self.test_document.files.count(), 1)
        self.assertEqual(
            self.test_document.files.first(), self.test_document.file_latest
        )

    def test_document_file_upload_api_view_no_permission(self):
        self._upload_test_document()

        response = self._request_test_document_file_upload_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_file_upload_api_view_with_access(self):
        self._upload_test_document()
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_new
        )

        response = self._request_test_document_file_upload_api_view()
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.assertEqual(self.test_document.files.count(), 2)
        self.assertEqual(self.test_document.file_latest.exists(), True)
        self.assertEqual(self.test_document.file_latest.size, 272213)
        self.assertEqual(self.test_document.file_latest.mimetype, 'application/pdf')
        self.assertEqual(self.test_document.file_latest.encoding, 'binary')
        self.assertEqual(
            self.test_document.file_latest.checksum,
            'c637ffab6b8bb026ed3784afdb07663fddc60099853fae2be93890852a69ecf3'
        )
        self.assertEqual(self.test_document.page_count, 47)


class DocumentFilePageAPIViewTestCase(
    DocumentFilePageAPIViewTestMixin, DocumentTestMixin, BaseAPITestCase
):
    def test_document_file_page_image_api_view_no_permission(self):
        response = self._request_test_document_file_page_image_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_file_page_image_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        response = self._request_test_document_file_page_image_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
