from django.utils.encoding import force_text

from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..models.document_models import Document
from ..permissions import (
    permission_trashed_document_delete, permission_trashed_document_restore,
    permission_document_trash, permission_document_view
)

from .mixins.document_mixins import DocumentTestMixin
from .mixins.trashed_document_mixins import TrashedDocumentAPIViewTestMixin


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
