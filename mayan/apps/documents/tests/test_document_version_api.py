from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase
from mayan.apps.storage.models import DownloadFile

from ..permissions import (
    permission_document_version_create, permission_document_version_delete,
    permission_document_version_edit, permission_document_version_view,
    permission_document_version_export
)

from .literals import TEST_DOCUMENT_VERSION_COMMENT_EDITED
from .mixins.document_mixins import DocumentTestMixin
from .mixins.document_version_mixins import (
    DocumentVersionAPIViewTestMixin, DocumentVersionTestMixin
)


class DocumentVersionAPIViewTestCase(
    DocumentVersionAPIViewTestMixin, DocumentTestMixin,
    DocumentVersionTestMixin, BaseAPITestCase
):
    def test_document_version_create_api_view_no_permission(self):
        response = self._request_test_document_version_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(self.test_document.versions.count(), 1)
        self.assertEqual(self.test_document.page_count, 1)

    def test_document_version_create_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_create
        )

        response = self._request_test_document_version_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(self.test_document.versions.count(), 2)
        self.assertEqual(self.test_document.page_count, 0)

    def test_document_version_delete_api_view_no_permission(self):
        response = self._request_test_document_version_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(self.test_document.versions.count(), 1)

    def test_document_version_delete_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_delete
        )

        response = self._request_test_document_version_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(self.test_document.versions.count(), 0)

    def test_document_version_edit_via_patch_api_view_no_permission(self):
        response = self._request_test_document_version_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_version_edit_via_patch_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_edit
        )
        response = self._request_test_document_version_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_document.version_active.refresh_from_db()
        self.assertEqual(self.test_document.versions.count(), 1)
        self.assertEqual(
            self.test_document.version_active.comment,
            TEST_DOCUMENT_VERSION_COMMENT_EDITED
        )

    def test_document_version_edit_via_put_api_view_no_permission(self):
        response = self._request_test_document_version_edit_via_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_version_edit_via_put_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_edit
        )

        response = self._request_test_document_version_edit_via_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document.version_active.refresh_from_db()
        self.assertEqual(self.test_document.versions.count(), 1)
        self.assertEqual(
            self.test_document.version_active.comment,
            TEST_DOCUMENT_VERSION_COMMENT_EDITED
        )

    def test_document_version_export_api_view_no_permission(self):
        download_file_count = DownloadFile.objects.count()

        response = self._request_test_document_version_export_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            DownloadFile.objects.count(), download_file_count
        )

    def test_document_version_export_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_export
        )
        download_file_count = DownloadFile.objects.count()

        response = self._request_test_document_version_export_api_view()
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.assertEqual(
            DownloadFile.objects.count(), download_file_count + 1
        )

    def test_document_version_list_api_view_no_permission(self):
        response = self._request_test_document_version_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_version_list_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_view
        )
        response = self._request_test_document_version_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['results'][0]['id'],
            self.test_document.version_active.id
        )
