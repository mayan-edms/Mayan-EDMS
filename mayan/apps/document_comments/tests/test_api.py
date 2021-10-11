from rest_framework import status

from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import (
    event_document_comment_created, event_document_comment_deleted,
    event_document_comment_edited
)
from ..permissions import (
    permission_document_comment_create, permission_document_comment_delete,
    permission_document_comment_edit, permission_document_comment_view
)

from .mixins import CommentAPIViewTestMixin, DocumentCommentTestMixin


class CommentAPIViewTestCase(
    CommentAPIViewTestMixin, DocumentCommentTestMixin, DocumentTestMixin,
    BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_user()
        self._create_test_document_stub()

    def test_comment_create_api_view_no_permission(self):
        comment_count = self.test_document.comments.count()

        self._clear_events()

        response = self._request_test_comment_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(self.test_document.comments.count(), comment_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_comment_create_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_comment_create
        )

        comment_count = self.test_document.comments.count()

        self._clear_events()

        response = self._request_test_comment_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            self.test_document.comments.count(), comment_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_comment)
        self.assertEqual(events[0].verb, event_document_comment_created.id)

    def test_trashed_document_comment_create_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_comment_create
        )

        comment_count = self.test_document.comments.count()

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_comment_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(self.test_document.comments.count(), comment_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_comment_delete_api_view_no_permission(self):
        self._create_test_comment()

        comment_count = self.test_document.comments.count()

        self._clear_events()

        response = self._request_test_comment_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(self.test_document.comments.count(), comment_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_comment_delete_api_view_with_access(self):
        self._create_test_comment()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_comment_delete
        )

        comment_count = self.test_document.comments.count()

        self._clear_events()

        response = self._request_test_comment_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(
            self.test_document.comments.count(), comment_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_comment_deleted.id)

    def test_trashed_document_comment_delete_api_view_with_access(self):
        self._create_test_comment()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_comment_delete
        )

        comment_count = self.test_document.comments.count()

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_comment_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(self.test_document.comments.count(), comment_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_comment_detail_api_view_no_permission(self):
        self._create_test_comment()

        self._clear_events()

        response = self._request_test_comment_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_comment_detail_api_view_with_access(self):
        self._create_test_comment()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_comment_view
        )

        self._clear_events()

        response = self._request_test_comment_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['text'], self.test_document_comment.text
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_comment_detail_api_view_with_access(self):
        self._create_test_comment()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_comment_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_comment_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_comment_edit_via_patch_api_view_no_permission(self):
        self._create_test_comment()

        comment_text = self.test_document_comment.text

        self._clear_events()

        response = self._request_test_comment_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_comment.refresh_from_db()
        self.assertEqual(self.test_document_comment.text, comment_text)
        self.assertEqual(self.test_document_comment.user, self.test_user)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_comment_edit_via_patch_api_view_with_access(self):
        self._create_test_comment()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_comment_edit
        )

        comment_text = self.test_document_comment.text

        self._clear_events()

        response = self._request_test_comment_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document_comment.refresh_from_db()
        self.assertNotEqual(self.test_document_comment.text, comment_text)
        self.assertEqual(self.test_document_comment.user, self.test_user)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_comment)
        self.assertEqual(events[0].verb, event_document_comment_edited.id)

    def test_trashed_document_comment_edit_via_patch_api_view_with_access(self):
        self._create_test_comment()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_comment_edit
        )

        comment_text = self.test_document_comment.text

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_comment_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_comment.refresh_from_db()
        self.assertEqual(self.test_document_comment.text, comment_text)
        self.assertEqual(self.test_document_comment.user, self.test_user)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_comment_edit_via_put_api_view_no_permission(self):
        self._create_test_comment()

        comment_text = self.test_document_comment.text

        self._clear_events()

        response = self._request_test_comment_edit_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_comment.refresh_from_db()
        self.assertEqual(self.test_document_comment.text, comment_text)
        self.assertEqual(self.test_document_comment.user, self.test_user)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_comment_edit_via_put_api_view_with_access(self):
        self._create_test_comment()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_comment_edit
        )

        comment_text = self.test_document_comment.text

        self._clear_events()

        response = self._request_test_comment_edit_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document_comment.refresh_from_db()
        self.assertNotEqual(self.test_document_comment.text, comment_text)
        self.assertEqual(self.test_document_comment.user, self.test_user)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_comment)
        self.assertEqual(events[0].verb, event_document_comment_edited.id)

    def test_trashed_document_comment_edit_via_put_api_view_with_access(self):
        self._create_test_comment()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_comment_edit
        )

        comment_text = self.test_document_comment.text

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_comment_edit_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_comment.refresh_from_db()
        self.assertEqual(self.test_document_comment.text, comment_text)
        self.assertEqual(self.test_document_comment.user, self.test_user)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_comment_list_api_view_no_permission(self):
        self._create_test_comment()

        self._clear_events()

        response = self._request_test_comment_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_comment_list_api_view_with_access(self):
        self._create_test_comment()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_comment_view
        )

        self._clear_events()

        response = self._request_test_comment_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['text'],
            self.test_document_comment.text
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_comment_list_api_view_with_access(self):
        self._create_test_comment()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_comment_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_comment_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
