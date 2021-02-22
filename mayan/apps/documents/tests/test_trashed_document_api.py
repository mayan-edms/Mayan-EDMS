from django.utils.encoding import force_text

from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import (
    event_document_trashed, event_trashed_document_deleted,
    event_trashed_document_restored
)

from ..models.document_models import Document
from ..permissions import (
    permission_trashed_document_delete, permission_trashed_document_restore,
    permission_document_trash, permission_document_version_view,
    permission_document_view
)

from .mixins.document_mixins import DocumentTestMixin
from .mixins.trashed_document_mixins import TrashedDocumentAPIViewTestMixin


class TrashedDocumentAPIViewTestCase(
    TrashedDocumentAPIViewTestMixin, DocumentTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def test_document_trash_api_view_no_permission(self):
        self._upload_test_document()

        trashed_document_count = Document.trash.count()
        document_count = Document.valid.count()

        self._clear_events()

        response = self._request_test_document_trash_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Document.trash.count(), trashed_document_count)
        self.assertEqual(Document.valid.count(), document_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_trash_api_view_with_access(self):
        self._upload_test_document()
        self.grant_access(
            obj=self.test_document, permission=permission_document_trash
        )

        trashed_document_count = Document.trash.count()
        document_count = Document.valid.count()

        self._clear_events()

        response = self._request_test_document_trash_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Document.trash.count(), trashed_document_count + 1)
        self.assertEqual(Document.valid.count(), document_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_trashed.id)

    def test_trashed_document_delete_api_view_no_permission(self):
        self._upload_test_document()
        self.test_document.delete()

        trashed_document_count = Document.trash.count()
        document_count = Document.valid.count()

        self._clear_events()

        response = self._request_test_trashed_document_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Document.trash.count(), trashed_document_count)
        self.assertEqual(Document.valid.count(), document_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_delete_api_view_with_access(self):
        self._upload_test_document()
        self.test_document.delete()
        self.grant_access(
            obj=self.test_document,
            permission=permission_trashed_document_delete
        )

        trashed_document_count = Document.trash.count()
        document_count = Document.valid.count()

        self._clear_events()

        response = self._request_test_trashed_document_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Document.trash.count(), trashed_document_count - 1)
        self.assertEqual(Document.valid.count(), document_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_type)
        self.assertEqual(events[0].verb, event_trashed_document_deleted.id)

    def test_trashed_document_detail_api_view_no_permission(self):
        self._upload_test_document()
        self.test_document.delete()

        trashed_document_count = Document.trash.count()
        document_count = Document.valid.count()

        self._clear_events()

        response = self._request_test_trashed_document_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse('uuid' in response.data)

        self.assertEqual(Document.trash.count(), trashed_document_count)
        self.assertEqual(Document.valid.count(), document_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_detail_api_view_with_access(self):
        self._upload_test_document()
        self.test_document.delete()
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        trashed_document_count = Document.trash.count()
        document_count = Document.valid.count()

        self._clear_events()

        response = self._request_test_trashed_document_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['uuid'], force_text(s=self.test_document.uuid)
        )

        self.assertEqual(Document.trash.count(), trashed_document_count)
        self.assertEqual(Document.valid.count(), document_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_image_api_view_no_permission(self):
        self._upload_test_document()
        self.test_document.delete()

        self._clear_events()

        response = self._request_test_trashed_document_image_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_image_api_view_with_access(self):
        self._upload_test_document()
        self.test_document.delete()
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_view
        )

        self._clear_events()

        response = self._request_test_trashed_document_image_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_list_api_view_no_permission(self):
        self._upload_test_document()
        self.test_document.delete()

        self._clear_events()

        response = self._request_test_trashed_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_list_api_view_with_access(self):
        self._upload_test_document()
        self.test_document.delete()
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_trashed_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['uuid'],
            force_text(s=self.test_document.uuid)
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_restore_via_get_api_view_no_permission(self):
        self._upload_test_document()
        self.test_document.delete()

        trashed_document_count = Document.trash.count()
        document_count = Document.valid.count()

        self._clear_events()

        response = self._request_test_trashed_document_restore_via_get_api_view()
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        self.assertEqual(Document.trash.count(), trashed_document_count)
        self.assertEqual(Document.valid.count(), document_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_restore_via_get_api_view_with_access(self):
        self._upload_test_document()
        self.test_document.delete()

        self.grant_access(
            obj=self.test_document,
            permission=permission_trashed_document_restore
        )

        trashed_document_count = Document.trash.count()
        document_count = Document.valid.count()

        self._clear_events()

        response = self._request_test_trashed_document_restore_via_get_api_view()
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        self.assertEqual(Document.trash.count(), trashed_document_count)
        self.assertEqual(Document.valid.count(), document_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_restore_via_post_api_view_no_permission(self):
        self._upload_test_document()
        self.test_document.delete()

        trashed_document_count = Document.trash.count()
        document_count = Document.valid.count()

        self._clear_events()

        response = self._request_test_trashed_document_restore_via_post_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Document.trash.count(), trashed_document_count)
        self.assertEqual(Document.valid.count(), document_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_restore_via_post_api_view_with_access(self):
        self._upload_test_document()
        self.test_document.delete()

        self.grant_access(
            obj=self.test_document,
            permission=permission_trashed_document_restore
        )

        trashed_document_count = Document.trash.count()
        document_count = Document.valid.count()

        self._clear_events()

        response = self._request_test_trashed_document_restore_via_post_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Document.trash.count(), trashed_document_count - 1)
        self.assertEqual(Document.valid.count(), document_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_trashed_document_restored.id)
