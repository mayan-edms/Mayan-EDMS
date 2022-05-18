from rest_framework import status

from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import (
    event_signature_capture_created, event_signature_capture_deleted,
    event_signature_capture_edited
)
from ..permissions import (
    permission_signature_capture_create, permission_signature_capture_delete,
    permission_signature_capture_edit, permission_signature_capture_view
)

from .mixins import (
    SignatureCaptureAPIViewTestMixin, SignatureCaptureTestMixin
)


class SignatureCaptureAPIViewTestCase(
    DocumentTestMixin, SignatureCaptureAPIViewTestMixin,
    SignatureCaptureTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_signature_capture_create_api_view_no_permission(self):
        signature_capture_count = self._test_document.signature_captures.count()

        self._clear_events()

        response = self._request_test_signature_capture_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self._test_document.signature_captures.count(),
            signature_capture_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_signature_capture_create_api_view_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_signature_capture_create
        )

        signature_capture_count = self._test_document.signature_captures.count()

        self._clear_events()

        response = self._request_test_signature_capture_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            self._test_document.signature_captures.count(),
            signature_capture_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_signature_capture)
        self.assertEqual(events[0].verb, event_signature_capture_created.id)

    def test_trashed_document_signature_capture_create_api_view_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_signature_capture_create
        )

        signature_capture_count = self._test_document.signature_captures.count()

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_signature_capture_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self._test_document.signature_captures.count(),
            signature_capture_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_signature_capture_delete_api_view_no_permission(self):
        self._create_test_signature_capture()

        signature_capture_count = self._test_document.signature_captures.count()

        self._clear_events()

        response = self._request_test_signature_capture_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self._test_document.signature_captures.count(),
            signature_capture_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_signature_capture_delete_api_view_with_document_access(self):
        self._create_test_signature_capture()

        self.grant_access(
            obj=self._test_document,
            permission=permission_signature_capture_delete
        )

        signature_capture_count = self._test_document.signature_captures.count()

        self._clear_events()

        response = self._request_test_signature_capture_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(
            self._test_document.signature_captures.count(),
            signature_capture_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_document)
        self.assertEqual(events[0].verb, event_signature_capture_deleted.id)

    def test_signature_capture_delete_api_view_with_signature_capture_access(self):
        self._create_test_signature_capture()

        self.grant_access(
            obj=self._test_signature_capture,
            permission=permission_signature_capture_delete
        )

        signature_capture_count = self._test_document.signature_captures.count()

        self._clear_events()

        response = self._request_test_signature_capture_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(
            self._test_document.signature_captures.count(),
            signature_capture_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_document)
        self.assertEqual(events[0].verb, event_signature_capture_deleted.id)

    def test_trashed_document_signature_capture_delete_api_view_with_document_access(self):
        self._create_test_signature_capture()

        self.grant_access(
            obj=self._test_document,
            permission=permission_signature_capture_delete
        )

        signature_capture_count = self._test_document.signature_captures.count()

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_signature_capture_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self._test_document.signature_captures.count(),
            signature_capture_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_signature_capture_delete_api_view_with_signature_capture_access(self):
        self._create_test_signature_capture()

        self.grant_access(
            obj=self._test_signature_capture,
            permission=permission_signature_capture_delete
        )

        signature_capture_count = self._test_document.signature_captures.count()

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_signature_capture_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self._test_document.signature_captures.count(),
            signature_capture_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_signature_capture_detail_api_view_no_permission(self):
        self._create_test_signature_capture()

        self._clear_events()

        response = self._request_test_signature_capture_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_signature_capture_detail_api_view_with_document_access(self):
        self._create_test_signature_capture()
        self.grant_access(
            obj=self._test_document,
            permission=permission_signature_capture_view
        )

        self._clear_events()

        response = self._request_test_signature_capture_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['text'], self._test_signature_capture.text
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_signature_capture_detail_api_view_with_signature_capture_access(self):
        self._create_test_signature_capture()
        self.grant_access(
            obj=self._test_signature_capture,
            permission=permission_signature_capture_view
        )

        self._clear_events()

        response = self._request_test_signature_capture_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['text'], self._test_signature_capture.text
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_signature_capture_detail_api_view_with_document_access(self):
        self._create_test_signature_capture()
        self.grant_access(
            obj=self._test_document,
            permission=permission_signature_capture_view
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_signature_capture_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_signature_capture_detail_api_view_with_signature_capture_access(self):
        self._create_test_signature_capture()
        self.grant_access(
            obj=self._test_signature_capture,
            permission=permission_signature_capture_view
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_signature_capture_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_signature_capture_edit_api_view_via_patch_no_permission(self):
        self._create_test_signature_capture()

        signature_capture_text = self._test_signature_capture.text

        self._clear_events()

        response = self._request_test_signature_capture_edit_api_view(verb='patch')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self._test_signature_capture.refresh_from_db()
        self.assertEqual(self._test_signature_capture.text, signature_capture_text)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_signature_capture_edit_api_view_via_patch_with_document_access(self):
        self._create_test_signature_capture()

        self.grant_access(
            obj=self._test_document,
            permission=permission_signature_capture_edit
        )

        signature_capture_text = self._test_signature_capture.text

        self._clear_events()

        response = self._request_test_signature_capture_edit_api_view(verb='patch')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self._test_signature_capture.refresh_from_db()
        self.assertNotEqual(
            self._test_signature_capture.text, signature_capture_text
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_signature_capture)
        self.assertEqual(events[0].verb, event_signature_capture_edited.id)

    def test_signature_capture_edit_api_view_via_patch_with_signature_capture_access(self):
        self._create_test_signature_capture()

        self.grant_access(
            obj=self._test_signature_capture,
            permission=permission_signature_capture_edit
        )

        signature_capture_text = self._test_signature_capture.text

        self._clear_events()

        response = self._request_test_signature_capture_edit_api_view(verb='patch')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self._test_signature_capture.refresh_from_db()
        self.assertNotEqual(
            self._test_signature_capture.text, signature_capture_text
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_signature_capture)
        self.assertEqual(events[0].verb, event_signature_capture_edited.id)

    def test_trashed_document_signature_capture_edit_api_view_via_patch_with_document_access(self):
        self._create_test_signature_capture()

        self.grant_access(
            obj=self._test_document,
            permission=permission_signature_capture_edit
        )

        signature_capture_text = self._test_signature_capture.text

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_signature_capture_edit_api_view(verb='patch')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self._test_signature_capture.refresh_from_db()
        self.assertEqual(
            self._test_signature_capture.text, signature_capture_text
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_signature_capture_edit_api_view_via_patch_with_signature_capture_access(self):
        self._create_test_signature_capture()

        self.grant_access(
            obj=self._test_signature_capture,
            permission=permission_signature_capture_edit
        )

        signature_capture_text = self._test_signature_capture.text

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_signature_capture_edit_api_view(verb='patch')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self._test_signature_capture.refresh_from_db()
        self.assertEqual(
            self._test_signature_capture.text, signature_capture_text
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_signature_capture_edit_api_view_via_put_no_permission(self):
        self._create_test_signature_capture()

        signature_capture_text = self._test_signature_capture.text

        self._clear_events()

        response = self._request_test_signature_capture_edit_api_view(verb='put')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self._test_signature_capture.refresh_from_db()
        self.assertEqual(
            self._test_signature_capture.text, signature_capture_text
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_signature_capture_edit_api_view_via_put_with_document_access(self):
        self._create_test_signature_capture()

        self.grant_access(
            obj=self._test_document,
            permission=permission_signature_capture_edit
        )

        signature_capture_text = self._test_signature_capture.text

        self._clear_events()

        response = self._request_test_signature_capture_edit_api_view(verb='put')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self._test_signature_capture.refresh_from_db()
        self.assertNotEqual(
            self._test_signature_capture.text, signature_capture_text
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_signature_capture)
        self.assertEqual(events[0].verb, event_signature_capture_edited.id)

    def test_signature_capture_edit_api_view_via_put_with_signature_capture_access(self):
        self._create_test_signature_capture()

        self.grant_access(
            obj=self._test_signature_capture,
            permission=permission_signature_capture_edit
        )

        signature_capture_text = self._test_signature_capture.text

        self._clear_events()

        response = self._request_test_signature_capture_edit_api_view(verb='put')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self._test_signature_capture.refresh_from_db()
        self.assertNotEqual(
            self._test_signature_capture.text, signature_capture_text
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_signature_capture)
        self.assertEqual(events[0].verb, event_signature_capture_edited.id)

    def test_trashed_document_signature_capture_edit_api_view_via_put_with_document_access(self):
        self._create_test_signature_capture()

        self.grant_access(
            obj=self._test_document,
            permission=permission_signature_capture_edit
        )

        signature_capture_text = self._test_signature_capture.text

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_signature_capture_edit_api_view(verb='put')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self._test_signature_capture.refresh_from_db()
        self.assertEqual(
            self._test_signature_capture.text, signature_capture_text
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_signature_capture_edit_api_view_via_put_with_signature_capture_access(self):
        self._create_test_signature_capture()

        self.grant_access(
            obj=self._test_signature_capture,
            permission=permission_signature_capture_edit
        )

        signature_capture_text = self._test_signature_capture.text

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_signature_capture_edit_api_view(verb='put')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self._test_signature_capture.refresh_from_db()
        self.assertEqual(
            self._test_signature_capture.text, signature_capture_text
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_signature_capture_list_api_view_no_permission(self):
        self._create_test_signature_capture()

        self._clear_events()

        response = self._request_test_signature_capture_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_signature_capture_list_api_view_with_document_access(self):
        self._create_test_signature_capture()
        self.grant_access(
            obj=self._test_document,
            permission=permission_signature_capture_view
        )

        self._clear_events()

        response = self._request_test_signature_capture_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['text'],
            self._test_signature_capture.text
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_signature_capture_list_api_view_with_signature_capture_access(self):
        self._create_test_signature_capture()
        self.grant_access(
            obj=self._test_signature_capture,
            permission=permission_signature_capture_view
        )

        self._clear_events()

        response = self._request_test_signature_capture_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['text'],
            self._test_signature_capture.text
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_signature_capture_list_api_view_with_document_access(self):
        self._create_test_signature_capture()
        self.grant_access(
            obj=self._test_document,
            permission=permission_signature_capture_view
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_signature_capture_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_signature_capture_list_api_view_with_signature_capture_access(self):
        self._create_test_signature_capture()
        self.grant_access(
            obj=self._test_signature_capture,
            permission=permission_signature_capture_view
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_signature_capture_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
