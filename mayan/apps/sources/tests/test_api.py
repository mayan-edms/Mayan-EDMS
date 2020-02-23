from __future__ import unicode_literals

from rest_framework import status

from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.permissions import permission_document_create
from mayan.apps.documents.tests.mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..models.staging_folder_sources import StagingFolderSource
from ..permissions import (
    permission_sources_setup_create, permission_sources_setup_delete,
    permission_sources_setup_edit, permission_sources_setup_view,
    permission_staging_file_delete
)

from .mixins import (
    StagingFolderAPIViewTestMixin, StagingFolderFileAPIViewTestMixin,
    StagingFolderTestMixin
)


class StagingFolderAPIViewTestCase(
    StagingFolderAPIViewTestMixin, StagingFolderTestMixin, BaseAPITestCase
):
    def test_staging_folder_create_api_view_no_permission(self):
        staging_folder_count = StagingFolderSource.objects.count()

        response = self._request_test_staging_folder_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(
            StagingFolderSource.objects.count(), staging_folder_count
        )

    def test_staging_folder_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_sources_setup_create)

        staging_folder_count = StagingFolderSource.objects.count()

        response = self._request_test_staging_folder_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            StagingFolderSource.objects.count(), staging_folder_count + 1
        )

    def test_staging_folder_delete_api_view_no_access(self):
        self._create_test_staging_folder()

        staging_folder_count = StagingFolderSource.objects.count()

        response = self._request_test_staging_folder_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            StagingFolderSource.objects.count(), staging_folder_count
        )

    def test_staging_folder_delete_api_view_with_permission(self):
        self._create_test_staging_folder()

        self.grant_permission(permission=permission_sources_setup_delete)

        staging_folder_count = StagingFolderSource.objects.count()

        response = self._request_test_staging_folder_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(
            StagingFolderSource.objects.count(), staging_folder_count - 1
        )

    def test_staging_folder_edit_api_view_via_patch_no_access(self):
        self._create_test_staging_folder()

        staging_folder_label = self.test_staging_folder.label

        response = self._request_staging_folder_edit_view(verb='patch')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_staging_folder.refresh_from_db()
        self.assertEqual(self.test_staging_folder.label, staging_folder_label)

    def test_staging_folder_edit_api_view_via_patch_with_permission(self):
        self._create_test_staging_folder()

        self.grant_permission(permission=permission_sources_setup_edit)

        staging_folder_label = self.test_staging_folder.label

        response = self._request_staging_folder_edit_view(verb='patch')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_staging_folder.refresh_from_db()
        self.assertNotEqual(
            self.test_staging_folder.label, staging_folder_label
        )

    def test_staging_folder_edit_api_view_via_put_no_access(self):
        self._create_test_staging_folder()

        staging_folder_label = self.test_staging_folder.label

        response = self._request_staging_folder_edit_view(
            extra_data={
                'folder_path': self.test_staging_folder.folder_path,
                'preview_width': self.test_staging_folder.preview_width,
                'uncompress': self.test_staging_folder.uncompress
            }, verb='put'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_staging_folder.refresh_from_db()
        self.assertEqual(self.test_staging_folder.label, staging_folder_label)

    def test_staging_folder_edit_api_view_via_put_with_permission(self):
        self._create_test_staging_folder()

        self.grant_permission(permission=permission_sources_setup_edit)

        staging_folder_label = self.test_staging_folder.label

        response = self._request_staging_folder_edit_view(
            extra_data={
                'folder_path': self.test_staging_folder.folder_path,
                'preview_width': self.test_staging_folder.preview_width,
                'uncompress': self.test_staging_folder.uncompress
            }, verb='put'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_staging_folder.refresh_from_db()
        self.assertNotEqual(
            self.test_staging_folder.label, staging_folder_label
        )

    def test_staging_folder_api_list_api_view_no_permission(self):
        self._create_test_staging_folder()

        response = self._request_staging_folder_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staging_folder_api_list_api_view_with_permission(self):
        self._create_test_staging_folder()

        self.grant_permission(permission=permission_sources_setup_view)

        response = self._request_staging_folder_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'],
            self.test_staging_folder.label
        )


class StagingFolderFileAPIViewTestCase(
    DocumentTestMixin, StagingFolderFileAPIViewTestMixin,
    StagingFolderTestMixin, BaseAPITestCase
):
    auto_create_test_document_type = False
    auto_upload_document = False

    def test_staging_folder_file_delete_api_view_no_permission(self):
        self._create_test_staging_folder()
        self._copy_test_document()
        staging_file_count = len(list(self.test_staging_folder.get_files()))

        response = self._request_staging_folder_file_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(
            len(list(self.test_staging_folder.get_files())),
            staging_file_count
        )

    def test_staging_folder_file_delete_api_view_with_permission(self):
        self.grant_permission(permission=permission_staging_file_delete)
        self._create_test_staging_folder()
        self._copy_test_document()
        staging_file_count = len(list(self.test_staging_folder.get_files()))

        response = self._request_staging_folder_file_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(response.data is None)

        self.assertNotEqual(
            len(list(self.test_staging_folder.get_files())),
            staging_file_count
        )

    def test_staging_folder_file_detail_api_view(self):
        self._create_test_staging_folder()
        self._copy_test_document()

        response = self._request_staging_folder_file_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            response.data['image_url'].endswith(
                self.test_staging_folder_file.get_api_image_url()
            )
        )

    def test_staging_folder_file_upload_api_view_no_permission(self):
        self._create_test_document_type()
        self._create_test_staging_folder()
        self._copy_test_document()
        document_count = Document.objects.count()

        response = self._request_staging_folder_file_upload_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Document.objects.count(), document_count)

    def test_staging_folder_file_upload_api_view_document_access(self):
        self._create_test_document_type()
        self._create_test_staging_folder()
        self._copy_test_document()
        document_count = Document.objects.count()

        self.grant_access(
            obj=self.test_document_type, permission=permission_document_create
        )

        response = self._request_staging_folder_file_upload_api_view()
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Document.objects.count(), document_count + 1)
