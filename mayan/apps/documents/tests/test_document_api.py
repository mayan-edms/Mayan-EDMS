from django.utils.encoding import force_text

from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..models import Document, DocumentType
from ..permissions import (
    permission_document_create, permission_trashed_document_delete,
    permission_document_properties_edit, permission_trashed_document_restore,
    permission_document_trash, permission_document_view
)

from .literals import (
    TEST_DOCUMENT_DESCRIPTION_EDITED, TEST_PDF_DOCUMENT_FILENAME,
    TEST_DOCUMENT_TYPE_2_LABEL
)
from .mixins.document_mixins import (
    DocumentAPIViewTestMixin, DocumentTestMixin
)
from .mixins.trashed_document_mixins import TrashedDocumentAPIViewTestMixin


class DocumentAPIViewTestCase(
    DocumentAPIViewTestMixin, DocumentTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def test_document_api_upload_view_no_permission(self):
        response = self._request_test_document_upload_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_api_upload_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type, permission=permission_document_create
        )

        response = self._request_test_document_upload_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Document.objects.count(), 1)

        document = Document.objects.first()

        # Correct document PK
        self.assertEqual(document.pk, response.data['id'])

        # Document initial file uploaded correctly
        self.assertEqual(document.files.count(), 1)

        # Document's file exists in the document storage
        self.assertEqual(document.file_latest.exists(), True)

        # And is of the expected size
        self.assertEqual(document.file_latest.size, 272213)

        # Correct mimetype
        self.assertEqual(document.file_latest.mimetype, 'application/pdf')

        # Check document file encoding
        self.assertEqual(document.file_latest.encoding, 'binary')
        self.assertEqual(document.label, TEST_PDF_DOCUMENT_FILENAME)
        self.assertEqual(
            document.file_latest.checksum,
            'c637ffab6b8bb026ed3784afdb07663fddc60099853fae2be93890852a69ecf3'
        )
        self.assertEqual(document.page_count, 47)

    def test_document_document_type_change_api_via_no_permission(self):
        self._upload_test_document()
        self.test_document_type_2 = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2_LABEL
        )

        response = self._request_test_document_type_change_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document.refresh_from_db()
        self.assertEqual(
            self.test_document.document_type,
            self.test_document_type
        )

    def test_document_document_type_change_api_via_with_access(self):
        self._upload_test_document()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_properties_edit
        )
        self.test_document_type_2 = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2_LABEL
        )

        response = self._request_test_document_type_change_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document.refresh_from_db()
        self.assertEqual(
            self.test_document.document_type,
            self.test_document_type_2
        )

    def test_document_description_api_edit_via_patch_view_no_permission(self):
        self._upload_test_document()

        response = self._request_test_document_description_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_description_api_edit_via_patch_view_with_access(self):
        self._upload_test_document()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_properties_edit
        )

        response = self._request_test_document_description_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document.refresh_from_db()
        self.assertEqual(
            self.test_document.description,
            TEST_DOCUMENT_DESCRIPTION_EDITED
        )

    def test_document_description_api_edit_via_put_view_no_permission(self):
        self._upload_test_document()

        response = self._request_test_document_description_edit_via_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_description_api_edit_via_put_view_with_access(self):
        self._upload_test_document()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_properties_edit
        )

        response = self._request_test_document_description_edit_via_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document.refresh_from_db()
        self.assertEqual(
            self.test_document.description,
            TEST_DOCUMENT_DESCRIPTION_EDITED
        )


class TrashedDocumentAPIViewTestCase(
    TrashedDocumentAPIViewTestMixin, DocumentTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def test_document_trash_api_view_no_permission(self):
        self._upload_test_document()

        response = self._request_test_document_trash_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_trash_api_view_with_access(self):
        self._upload_test_document()
        self.grant_access(
            obj=self.test_document, permission=permission_document_trash
        )

        response = self._request_test_document_trash_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Document.valid.count(), 0)
        self.assertEqual(Document.trash.count(), 1)

    def test_trashed_document_delete_api_view_no_permission(self):
        self._upload_test_document()
        self.test_document.delete()

        response = self._request_test_trashed_document_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Document.valid.count(), 0)
        self.assertEqual(Document.trash.count(), 1)

    def test_trashed_document_delete_api_view_with_access(self):
        self._upload_test_document()
        self.test_document.delete()
        self.grant_access(
            obj=self.test_document,
            permission=permission_trashed_document_delete
        )

        response = self._request_test_trashed_document_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Document.valid.count(), 0)
        self.assertEqual(Document.trash.count(), 0)

    def test_trashed_document_detail_api_view_no_permission(self):
        self._upload_test_document()
        self.test_document.delete()

        response = self._request_test_trashed_document_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse('uuid' in response.data)

    def test_trashed_document_detail_api_view_with_access(self):
        self._upload_test_document()
        self.test_document.delete()
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_trashed_document_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['uuid'], force_text(s=self.test_document.uuid)
        )

    def test_trashed_document_image_api_view_no_permission(self):
        self._upload_test_document()
        self.test_document.delete()

        response = self._request_test_trashed_document_image_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_trashed_document_image_api_view_with_access(self):
        self._upload_test_document()
        self.test_document.delete()
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_trashed_document_image_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_trashed_document_list_api_view_no_permission(self):
        self._upload_test_document()
        self.test_document.delete()

        response = self._request_test_trashed_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_trashed_document_list_api_view_with_access(self):
        self._upload_test_document()
        self.test_document.delete()
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_trashed_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['uuid'],
            force_text(s=self.test_document.uuid)
        )

    def test_trashed_document_restore_api_view_no_permission(self):
        self._upload_test_document()
        self.test_document.delete()

        response = self._request_test_trashed_document_restore_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Document.trash.count(), 1)
        self.assertEqual(Document.valid.count(), 0)

    def test_trashed_document_restore_api_view_with_access(self):
        self._upload_test_document()
        self.test_document.delete()

        self.grant_access(
            obj=self.test_document,
            permission=permission_trashed_document_restore
        )
        response = self._request_test_trashed_document_restore_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Document.trash.count(), 0)
        self.assertEqual(Document.valid.count(), 1)
