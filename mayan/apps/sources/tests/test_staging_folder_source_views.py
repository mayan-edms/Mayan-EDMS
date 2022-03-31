from mayan.apps.documents.permissions import permission_document_create
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from .mixins.base_mixins import SourceDocumentUploadViewTestMixin
from .mixins.staging_folder_source_mixins import (
    StagingFolderTestMixin, StagingFolderViewTestMixin
)


class StagingFolderActionViewTestCase(
    StagingFolderTestMixin, StagingFolderViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_staging_folder_file_delete_get_view_no_permission(self):
        self._copy_test_staging_folder_document()

        staging_folder_file_count = len(
            list(
                self._test_source.get_backend_instance().get_files()
            )
        )

        self._clear_events()

        response = self._request_staging_folder_action_file_delete_view_via_get()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            len(
                list(
                    self._test_source.get_backend_instance().get_files()
                )
            ), staging_folder_file_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_staging_folder_file_delete_get_view_with_access(self):
        self.grant_access(
            obj=self._test_source, permission=permission_document_create
        )
        self._copy_test_staging_folder_document()

        staging_folder_file_count = len(
            list(
                self._test_source.get_backend_instance().get_files()
            )
        )

        self._clear_events()

        response = self._request_staging_folder_action_file_delete_view_via_get()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            len(
                list(
                    self._test_source.get_backend_instance().get_files()
                )
            ), staging_folder_file_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_staging_folder_file_delete_post_view_no_permission(self):
        self._copy_test_staging_folder_document()

        staging_folder_file_count = len(
            list(
                self._test_source.get_backend_instance().get_files()
            )
        )

        self._clear_events()

        response = self._request_staging_folder_action_file_delete_view_via_post()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            len(
                list(
                    self._test_source.get_backend_instance().get_files()
                )
            ), staging_folder_file_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_staging_folder_file_delete_post_view_with_access(self):
        self.grant_access(
            obj=self._test_source, permission=permission_document_create
        )
        self._copy_test_staging_folder_document()

        staging_folder_file_count = len(
            list(
                self._test_source.get_backend_instance().get_files()
            )
        )

        self._clear_events()

        response = self._request_staging_folder_action_file_delete_view_via_post()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            len(
                list(
                    self._test_source.get_backend_instance().get_files()
                )
            ), staging_folder_file_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class StagingFolderViewTestCase(
    StagingFolderTestMixin, SourceDocumentUploadViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_create_test_source = False
    auto_upload_test_document = False

    def test_staging_folder_document_upload_view_with_full_access(self):
        self._create_test_staging_folder()

        self.grant_access(
            obj=self._test_document_type,
            permission=permission_document_create
        )
        self.grant_access(
            obj=self._test_source, permission=permission_document_create
        )

        self._clear_events()

        response = self._request_source_document_upload_view_via_get()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_staging_folder_document_upload_not_include_subdirectories_view_with_full_access(self):
        self._create_test_staging_folder(
            add_subdirectory=True, extra_data={
                'include_subdirectories': False
            }
        )

        self._copy_test_staging_folder_document(filename='test_document_1')
        self._copy_test_staging_folder_document(
            filename='test_document_2', to_subfolder=True
        )

        self.grant_access(
            obj=self._test_document_type,
            permission=permission_document_create
        )
        self.grant_access(
            obj=self._test_source, permission=permission_document_create
        )

        self._clear_events()

        response = self._request_source_document_upload_view_via_get()
        self.assertContains(
            response=response, status_code=200, text='test_document_1'
        )
        self.assertNotContains(
            response=response, status_code=200, text='test_document_2'
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_staging_folder_document_upload_include_subdirectories_view_with_full_access(self):
        self._create_test_staging_folder(
            add_subdirectory=True, extra_data={
                'include_subdirectories': True
            }
        )

        self._copy_test_staging_folder_document(filename='test_document_1')
        self._copy_test_staging_folder_document(
            filename='test_document_2', to_subfolder=True
        )

        self.grant_access(
            obj=self._test_document_type,
            permission=permission_document_create
        )
        self.grant_access(
            obj=self._test_source, permission=permission_document_create
        )

        self._clear_events()

        response = self._request_source_document_upload_view_via_get()
        self.assertContains(
            response=response, status_code=200, text='test_document_1'
        )
        self.assertContains(
            response=response, status_code=200, text='test_document_2'
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_staging_folder_document_include_regular_expression_view_with_full_access(self):
        self._create_test_staging_folder(
            extra_data={'include_regex': 'test_document_1'}
        )

        self._copy_test_staging_folder_document(filename='test_document_1')
        self._copy_test_staging_folder_document(filename='test_document_2')

        self.grant_access(
            obj=self._test_document_type,
            permission=permission_document_create
        )
        self.grant_access(
            obj=self._test_source, permission=permission_document_create
        )

        self._clear_events()

        response = self._request_source_document_upload_view_via_get()
        self.assertContains(
            response=response, status_code=200, text='test_document_1'
        )
        self.assertNotContains(
            response=response, status_code=200, text='test_document_2'
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_staging_folder_document_exclude_regular_expression_view_with_full_access(self):
        self._create_test_staging_folder(
            extra_data={'exclude_regex': 'test_document_1'}
        )

        self._copy_test_staging_folder_document(filename='test_document_1')
        self._copy_test_staging_folder_document(filename='test_document_2')

        self.grant_access(
            obj=self._test_document_type,
            permission=permission_document_create
        )
        self.grant_access(
            obj=self._test_source, permission=permission_document_create
        )

        self._clear_events()

        response = self._request_source_document_upload_view_via_get()
        self.assertNotContains(
            response=response, status_code=200, text='test_document_1'
        )
        self.assertContains(
            response=response, status_code=200, text='test_document_2'
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
