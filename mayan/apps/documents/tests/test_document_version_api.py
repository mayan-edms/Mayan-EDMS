from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase
from mayan.apps.storage.models import DownloadFile

from ..events import (
    event_document_version_created, event_document_version_deleted,
    event_document_version_edited
)
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
    _test_event_object_name = 'test_document_version'

    def test_document_version_create_api_view_no_permission(self):
        self._clear_events()

        document_version_count = self.test_document.versions.count()

        response = self._request_test_document_version_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.versions.count(), document_version_count
        )

        event = self._get_test_object_event()
        self.assertEqual(event, None)

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

        event = self._get_test_object_event()
        self.assertEqual(event.action_object, self.test_document)
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.target, self.test_document_version)
        self.assertEqual(event.verb, event_document_version_created.id)

    def test_document_version_delete_api_view_no_permission(self):
        self._clear_events()

        document_version_count = self.test_document.versions.count()

        response = self._request_test_document_version_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.versions.count(), document_version_count
        )

        event = self._get_test_object_event(object_name='test_document')
        self.assertEqual(event, None)

    def test_document_version_delete_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_delete
        )

        self._clear_events()

        document_version_count = self.test_document.versions.count()

        response = self._request_test_document_version_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(
            self.test_document.versions.count(), document_version_count - 1
        )

        event = self._get_test_object_event(object_name='test_document')
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.target, self.test_document)
        self.assertEqual(event.verb, event_document_version_deleted.id)

    def test_document_version_detail_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_version_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

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

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_document_version_edit_via_patch_api_view_no_permission(self):
        self._clear_events()

        document_version_comment = self.test_document.version_active.comment

        response = self._request_test_document_version_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document.version_active.refresh_from_db()
        self.assertEqual(
            self.test_document.version_active.comment,
            document_version_comment
        )

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_document_version_edit_via_patch_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_edit
        )

        self._clear_events()

        document_version_comment = self.test_document.version_active.comment

        response = self._request_test_document_version_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document.version_active.refresh_from_db()
        self.assertNotEqual(
            self.test_document.version_active.comment,
            document_version_comment
        )

        event = self._get_test_object_event()
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.target, self.test_document_version)
        self.assertEqual(event.verb, event_document_version_edited.id)

    def test_document_version_edit_via_put_api_view_no_permission(self):
        self._clear_events()

        document_version_comment = self.test_document.version_active.comment

        response = self._request_test_document_version_edit_via_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document.version_active.refresh_from_db()
        self.assertEqual(
            self.test_document.version_active.comment,
            document_version_comment
        )

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_document_version_edit_via_put_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_edit
        )

        self._clear_events()

        document_version_comment = self.test_document.version_active.comment

        response = self._request_test_document_version_edit_via_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document.version_active.refresh_from_db()
        self.assertNotEqual(
            self.test_document.version_active.comment,
            document_version_comment
        )

        event = self._get_test_object_event()
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.target, self.test_document_version)
        self.assertEqual(event.verb, event_document_version_edited.id)

    def test_document_version_export_api_view_no_permission(self):
        download_file_count = DownloadFile.objects.count()

        self._clear_events()

        response = self._request_test_document_version_export_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            DownloadFile.objects.count(), download_file_count
        )

        event = self._get_test_object_event()
        self.assertEqual(event, None)

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

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_document_version_list_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_version_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

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

        event = self._get_test_object_event()
        self.assertEqual(event, None)
