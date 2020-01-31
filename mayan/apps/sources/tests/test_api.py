from __future__ import unicode_literals

from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..permissions import permission_staging_file_delete

from .mixins import StagingFolderTestMixin


class StagingFolderFileAPIViewTestCase(
    StagingFolderTestMixin, BaseAPITestCase
):
    def _request_staging_folder_file_delete_api_view(self):
        staging_file = list(self.test_staging_folder.get_files())[0]

        return self.delete(
            viewname='rest_api:stagingfolderfile-detail', kwargs={
                'staging_folder_pk': self.test_staging_folder.pk,
                'encoded_filename': staging_file.encoded_filename
            }
        )

    def _request_staging_folder_file_detail_api_view(self):
        staging_file = list(self.test_staging_folder.get_files())[0]

        return self.get(
            viewname='rest_api:stagingfolderfile-detail', kwargs={
                'staging_folder_pk': self.test_staging_folder.pk,
                'encoded_filename': staging_file.encoded_filename
            }
        )

    def test_staging_folder_file_delete_view_no_permission(self):
        self._create_test_stating_folder()
        self._copy_test_document()
        staging_file_count = len(list(self.test_staging_folder.get_files()))

        response = self._request_staging_folder_file_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(
            len(list(self.test_staging_folder.get_files())),
            staging_file_count
        )

    def test_staging_folder_file_delete_view_with_permission(self):
        self.grant_permission(permission=permission_staging_file_delete)
        self._create_test_stating_folder()
        self._copy_test_document()
        staging_file_count = len(list(self.test_staging_folder.get_files()))

        response = self._request_staging_folder_file_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(response.data is None)

        self.assertNotEqual(
            len(list(self.test_staging_folder.get_files())),
            staging_file_count
        )

    def test_staging_folder_file_detail_view(self):
        self._create_test_stating_folder()
        self._copy_test_document()
        staging_file = list(self.test_staging_folder.get_files())[0]

        response = self._request_staging_folder_file_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            response.data['image_url'].endswith(
                staging_file.get_api_image_url()
            )
        )
