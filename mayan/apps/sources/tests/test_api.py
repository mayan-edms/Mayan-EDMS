from django.http.response import FileResponse

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

from ..events import event_source_created, event_source_edited
from ..models import Source
from ..permissions import (
    permission_sources_create, permission_sources_delete,
    permission_sources_edit, permission_sources_view
)

from .mixins import (
    SourceAPIViewTestMixin, SourceTestMixin,
    StagingFolderActionAPIViewTestMixin, StagingFolderTestMixin
)


class SourceAPIViewTestCase(
    SourceAPIViewTestMixin, SourceTestMixin, BaseAPITestCase
):
    auto_create_test_source = False

    def test_source_create_api_view_no_permission(self):
        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_source_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Source.objects.count(), source_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_sources_create)

        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_source_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Source.objects.count(), source_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_source)
        self.assertEqual(events[0].verb, event_source_created.id)

    def test_source_delete_api_view_no_permission(self):
        self._create_test_source()

        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_source_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Source.objects.count(), source_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_delete_api_view_with_access(self):
        self._create_test_source()

        self.grant_access(
            obj=self.test_source, permission=permission_sources_delete
        )

        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_source_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Source.objects.count(), source_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_edit_api_view_via_patch_no_permission(self):
        self._create_test_source()

        source_label = self.test_source.label

        self._clear_events()

        response = self._request_test_source_edit_api_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_source.refresh_from_db()
        self.assertEqual(self.test_source.label, source_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_edit_api_view_via_patch_with_access(self):
        self._create_test_source()

        self.grant_access(
            obj=self.test_source, permission=permission_sources_edit
        )

        source_label = self.test_source.label

        self._clear_events()

        response = self._request_test_source_edit_api_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_source.refresh_from_db()
        self.assertNotEqual(self.test_source.label, source_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_source)
        self.assertEqual(events[0].verb, event_source_edited.id)

    def test_source_edit_api_view_via_put_no_permission(self):
        self._create_test_source()

        source_label = self.test_source.label

        self._clear_events()

        response = self._request_test_source_edit_api_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_source.refresh_from_db()
        self.assertEqual(self.test_source.label, source_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_edit_api_view_via_put_with_access(self):
        self._create_test_source()

        self.grant_access(
            obj=self.test_source, permission=permission_sources_edit
        )

        source_label = self.test_source.label

        self._clear_events()

        response = self._request_test_source_edit_api_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_source.refresh_from_db()
        self.assertNotEqual(self.test_source.label, source_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_source)
        self.assertEqual(events[0].verb, event_source_edited.id)

    def test_source_api_list_api_view_no_permission(self):
        self._create_test_source()

        self._clear_events()

        response = self._request_test_source_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_api_list_api_view_with_access(self):
        self._create_test_source()

        self.grant_access(
            obj=self.test_source, permission=permission_sources_view
        )
        self._clear_events()

        response = self._request_test_source_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'],
            self.test_source.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class StagingFolderActionAPIViewTestCase(
    DocumentTestMixin, StagingFolderTestMixin,
    StagingFolderActionAPIViewTestMixin, BaseAPITestCase
):
    auto_create_test_document_type = False
    auto_upload_test_document = False

    def test_staging_folder_file_delete_action_api_view_no_permission(self):
        self._copy_test_staging_folder_document()

        test_staging_folder = self.test_source.get_backend_instance()

        staging_file_count = len(list(test_staging_folder.get_files()))

        self._clear_events()

        response = self._request_test_staging_folder_file_delete_action_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            len(list(test_staging_folder.get_files())), staging_file_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_staging_folder_file_delete_action_api_view_with_access(self):
        self.grant_access(
            obj=self.test_source, permission=permission_document_create
        )

        self._copy_test_staging_folder_document()

        test_staging_folder = self.test_source.get_backend_instance()

        staging_file_count = len(list(test_staging_folder.get_files()))

        self._clear_events()

        response = self._request_test_staging_folder_file_delete_action_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            len(list(test_staging_folder.get_files())), staging_file_count - 1
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
        self.assertTrue(isinstance(response, FileResponse))

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
