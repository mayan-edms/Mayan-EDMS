from rest_framework import status

from mayan.apps.rest_api.tests.base import (
    BaseAPITestCase, BaseAPITransactionTestCase
)
from mayan.apps.storage.events import event_download_file_created
from mayan.apps.storage.models import DownloadFile

from ..events import (
    event_document_version_created, event_document_version_deleted,
    event_document_version_edited, event_document_version_exported
)
from ..permissions import (
    permission_document_version_create, permission_document_version_delete,
    permission_document_version_edit, permission_document_version_view,
    permission_document_version_export
)

from .mixins.document_mixins import DocumentTestMixin
from .mixins.document_version_mixins import (
    DocumentVersionAPIViewTestMixin, DocumentVersionTestMixin
)


class DocumentVersionAPIViewTestCase(
    DocumentVersionAPIViewTestMixin, DocumentTestMixin,
    DocumentVersionTestMixin, BaseAPITestCase
):
    def test_document_version_create_api_view_no_permission(self):
        document_version_count = self.test_document.versions.count()

        self._clear_events()

        response = self._request_test_document_version_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.versions.count(), document_version_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_create_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_create
        )

        document_version_count = self.test_document.versions.count()

        self._clear_events()

        response = self._request_test_document_version_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            self.test_document.versions.count(), document_version_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].action_object, self.test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_version)
        self.assertEqual(events[0].verb, event_document_version_created.id)

    def test_document_version_delete_api_view_no_permission(self):
        document_version_count = self.test_document.versions.count()

        self._clear_events()

        response = self._request_test_document_version_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.versions.count(), document_version_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_delete_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_delete
        )

        document_version_count = self.test_document.versions.count()

        self._clear_events()

        response = self._request_test_document_version_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(
            self.test_document.versions.count(), document_version_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_version_deleted.id)

    def test_document_version_detail_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_version_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_detail_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_view
        )

        self._clear_events()

        response = self._request_test_document_version_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['id'], self.test_document.version_active.id
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_edit_via_patch_api_view_no_permission(self):
        document_version_comment = self.test_document.version_active.comment

        self._clear_events()

        response = self._request_test_document_version_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document.version_active.refresh_from_db()
        self.assertEqual(
            self.test_document.version_active.comment,
            document_version_comment
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_edit_via_patch_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_edit
        )

        document_version_comment = self.test_document.version_active.comment

        self._clear_events()

        response = self._request_test_document_version_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document.version_active.refresh_from_db()
        self.assertNotEqual(
            self.test_document.version_active.comment,
            document_version_comment
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].action_object, self.test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_version)
        self.assertEqual(events[0].verb, event_document_version_edited.id)

    def test_document_version_edit_via_put_api_view_no_permission(self):
        document_version_comment = self.test_document.version_active.comment

        self._clear_events()

        response = self._request_test_document_version_edit_via_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document.version_active.refresh_from_db()
        self.assertEqual(
            self.test_document.version_active.comment,
            document_version_comment
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_edit_via_put_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_edit
        )

        document_version_comment = self.test_document.version_active.comment

        self._clear_events()

        response = self._request_test_document_version_edit_via_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document.version_active.refresh_from_db()
        self.assertNotEqual(
            self.test_document.version_active.comment,
            document_version_comment
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].action_object, self.test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_version)
        self.assertEqual(events[0].verb, event_document_version_edited.id)

    def test_document_version_list_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_version_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_list_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_view
        )

        self._clear_events()

        response = self._request_test_document_version_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['results'][0]['id'],
            self.test_document.version_active.id
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentVersionExportAPIViewTestCase(
    DocumentVersionAPIViewTestMixin, DocumentTestMixin,
    DocumentVersionTestMixin, BaseAPITransactionTestCase
):
    def test_document_version_export_api_view_no_permission(self):
        download_file_count = DownloadFile.objects.count()

        self._clear_events()

        response = self._request_test_document_version_export_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            DownloadFile.objects.count(), download_file_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_export_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_export
        )
        download_file_count = DownloadFile.objects.count()

        self._clear_events()

        response = self._request_test_document_version_export_api_view()
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.assertEqual(
            DownloadFile.objects.count(), download_file_count + 1
        )

        test_download_file = DownloadFile.objects.first()

        events = self._get_test_events()
        self.assertEqual(events.count(), 2)

        self.assertEqual(events[0].action_object, self.test_document_version)
        self.assertEqual(events[0].actor, test_download_file)
        self.assertEqual(events[0].target, test_download_file)
        self.assertEqual(events[0].verb, event_download_file_created.id)

        self.assertEqual(events[1].action_object, test_download_file)
        self.assertEqual(events[1].actor, self.test_document_version)
        self.assertEqual(events[1].target, self.test_document_version)
        self.assertEqual(events[1].verb, event_document_version_exported.id)
