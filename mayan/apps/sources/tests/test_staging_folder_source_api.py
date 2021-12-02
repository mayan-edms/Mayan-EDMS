from django.http.response import StreamingHttpResponse

from rest_framework import status

from mayan.apps.documents.events import (
    event_document_created, event_document_file_created,
    event_document_file_edited, event_document_version_created,
    event_document_version_page_created
)
from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.permissions import permission_document_create
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from .mixins.staging_folder_source_mixins import (
    StagingFolderActionAPIViewTestMixin, StagingFolderTestMixin
)


class StagingFolderActionAPIViewTestCase(
    DocumentTestMixin, StagingFolderTestMixin,
    StagingFolderActionAPIViewTestMixin, BaseAPITestCase
):
    auto_create_test_document_type = False
    auto_upload_test_document = False

    def test_staging_folder_file_delete_action_api_view_no_permission(self):
        self._copy_test_staging_folder_document()

        test_staging_folder = self.test_source.get_backend_instance()

        staging_folder_file_count = len(
            list(test_staging_folder.get_files())
        )

        self._clear_events()

        response = self._request_test_staging_folder_file_delete_action_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            len(
                list(test_staging_folder.get_files())
            ), staging_folder_file_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_staging_folder_file_delete_action_api_view_with_access(self):
        self.grant_access(
            obj=self.test_source, permission=permission_document_create
        )

        self._copy_test_staging_folder_document()

        test_staging_folder = self.test_source.get_backend_instance()

        staging_folder_file_count = len(
            list(test_staging_folder.get_files())
        )

        self._clear_events()

        response = self._request_test_staging_folder_file_delete_action_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            len(
                list(test_staging_folder.get_files())
            ), staging_folder_file_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_staging_folder_file_image_action_api_view_no_permission(self):
        self._copy_test_staging_folder_document()

        self._clear_events()

        response = self._request_test_staging_folder_file_image_action_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_staging_folder_file_image_action_api_view_with_access(self):
        self.grant_access(
            obj=self.test_source, permission=permission_document_create
        )

        self._copy_test_staging_folder_document()

        self._clear_events()

        response = self._request_test_staging_folder_file_image_action_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response, StreamingHttpResponse))

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_staging_folder_file_list_action_api_view_no_permission(self):
        self._copy_test_staging_folder_document()

        self._clear_events()

        response = self._request_test_staging_folder_file_list_action_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_staging_folder_file_list_action_api_view_with_access(self):
        self.grant_access(
            obj=self.test_source, permission=permission_document_create
        )

        self._copy_test_staging_folder_document()

        self._clear_events()

        response = self._request_test_staging_folder_file_list_action_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data[0]['encoded_filename'],
            self.test_staging_folder_file.encoded_filename
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_staging_folder_file_upload_api_view_no_permission(self):
        self._create_test_document_type()

        self._copy_test_staging_folder_document()

        document_count = Document.objects.count()

        self._clear_events()

        response = self._request_test_staging_folder_file_upload_action_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Document.objects.count(), document_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_staging_folder_file_upload_api_view_with_document_type_access(self):
        self._create_test_document_type()

        self.grant_access(
            obj=self.test_document_type, permission=permission_document_create
        )

        self._copy_test_staging_folder_document()

        document_count = Document.objects.count()

        self._clear_events()

        response = self._request_test_staging_folder_file_upload_action_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Document.objects.count(), document_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_staging_folder_file_upload_api_view_with_source_access(self):
        self._create_test_document_type()

        self.grant_access(
            obj=self.test_source, permission=permission_document_create
        )

        self._copy_test_staging_folder_document()

        document_count = Document.objects.count()

        self._clear_events()

        response = self._request_test_staging_folder_file_upload_action_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Document.objects.count(), document_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_staging_folder_file_upload_api_view_with_full_access(self):
        self._create_test_document_type()

        self.grant_access(
            obj=self.test_document_type, permission=permission_document_create
        )
        self.grant_access(
            obj=self.test_source, permission=permission_document_create
        )

        self._copy_test_staging_folder_document()

        document_count = Document.objects.count()

        self._clear_events()

        response = self._request_test_staging_folder_file_upload_action_api_view()
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.assertEqual(Document.objects.count(), document_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 5)

        test_document = Document.objects.first()
        test_document_file = test_document.file_latest
        test_document_version = test_document.version_active
        test_document_version_page = test_document_version.pages.first()

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, test_document)
        self.assertEqual(events[0].verb, event_document_created.id)

        self.assertEqual(events[1].action_object, test_document)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, test_document_file)
        self.assertEqual(events[1].verb, event_document_file_created.id)

        self.assertEqual(events[2].action_object, test_document)
        self.assertEqual(events[2].actor, self._test_case_user)
        self.assertEqual(events[2].target, test_document_file)
        self.assertEqual(events[2].verb, event_document_file_edited.id)

        self.assertEqual(events[3].action_object, test_document)
        self.assertEqual(events[3].actor, self._test_case_user)
        self.assertEqual(events[3].target, test_document_version)
        self.assertEqual(events[3].verb, event_document_version_created.id)

        self.assertEqual(events[4].action_object, test_document_version)
        self.assertEqual(events[4].actor, self._test_case_user)
        self.assertEqual(events[4].target, test_document_version_page)
        self.assertEqual(
            events[4].verb, event_document_version_page_created.id
        )
