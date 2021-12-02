from mayan.apps.documents.permissions import permission_document_create
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from .mixins.staging_folder_source_mixins import (
    StagingFolderTestMixin, StagingFolderViewTestMixin
)


class StagingFolderViewTestCase(
    StagingFolderTestMixin, StagingFolderViewTestMixin,
    GenericDocumentViewTestCase
):
    def test_staging_folder_file_delete_get_view_no_permission(self):
        self._copy_test_staging_folder_document()

        staging_folder_file_count = len(
            list(
                self.test_source.get_backend_instance().get_files()
            )
        )

        self._clear_events()

        response = self._request_staging_folder_action_file_delete_view_via_get()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            len(
                list(
                    self.test_source.get_backend_instance().get_files()
                )
            ), staging_folder_file_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_staging_folder_file_delete_get_view_with_access(self):
        self.grant_access(
            obj=self.test_source, permission=permission_document_create
        )
        self._copy_test_staging_folder_document()

        staging_folder_file_count = len(
            list(
                self.test_source.get_backend_instance().get_files()
            )
        )

        self._clear_events()

        response = self._request_staging_folder_action_file_delete_view_via_get()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            len(
                list(
                    self.test_source.get_backend_instance().get_files()
                )
            ), staging_folder_file_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_staging_folder_file_delete_post_view_no_permission(self):
        self._copy_test_staging_folder_document()

        staging_folder_file_count = len(
            list(
                self.test_source.get_backend_instance().get_files()
            )
        )

        self._clear_events()

        response = self._request_staging_folder_action_file_delete_view_via_post()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            len(
                list(
                    self.test_source.get_backend_instance().get_files()
                )
            ), staging_folder_file_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_staging_folder_file_delete_post_view_with_access(self):
        self.grant_access(
            obj=self.test_source, permission=permission_document_create
        )
        self._copy_test_staging_folder_document()

        staging_folder_file_count = len(
            list(
                self.test_source.get_backend_instance().get_files()
            )
        )

        self._clear_events()

        response = self._request_staging_folder_action_file_delete_view_via_post()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            len(
                list(
                    self.test_source.get_backend_instance().get_files()
                )
            ), staging_folder_file_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
