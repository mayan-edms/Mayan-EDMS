from rest_framework import status

from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import (
    event_document_comment_created, event_document_comment_deleted,
    event_document_comment_edited
)
from ..models import Comment
from ..permissions import (
    permission_document_comment_create, permission_document_comment_delete,
    permission_document_comment_edit, permission_document_comment_view
)

from .mixins import CommentAPIViewTestMixin, DocumentCommentTestMixin


class CommentAPIViewTestCase(
    CommentAPIViewTestMixin, DocumentCommentTestMixin, DocumentTestMixin,
    BaseAPITestCase
):
    _test_event_object_name = 'test_document_comment'
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_user()
        self._create_test_document_stub()

    def test_comment_create_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_comment_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Comment.objects.count(), 0)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_comment_create_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_comment_create
        )

        self._clear_events()

        response = self._request_test_comment_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        comment = Comment.objects.first()
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(response.data['id'], comment.pk)

        event = self._get_test_object_event()
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.action_object, self.test_document)
        self.assertEqual(event.target, self.test_document_comment)
        self.assertEqual(event.verb, event_document_comment_created.id)

    def test_comment_delete_api_view_no_permission(self):
        self._create_test_comment()

        self._clear_events()

        response = self._request_test_comment_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertTrue(self.test_document_comment in Comment.objects.all())

        event = self._get_test_object_event(object_name='test_document')
        self.assertEqual(event, None)

    def test_comment_delete_api_view_with_access(self):
        self._create_test_comment()
        self.grant_access(
            obj=self.test_document, permission=permission_document_comment_delete
        )

        self._clear_events()

        response = self._request_test_comment_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(self.test_document_comment in Comment.objects.all())

        event = self._get_test_object_event(object_name='test_document')
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.target, self.test_document)
        self.assertEqual(event.verb, event_document_comment_deleted.id)

    def test_comment_detail_api_view_no_permission(self):
        self._create_test_comment()

        self._clear_events()

        response = self._request_test_comment_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_comment_detail_api_view_with_access(self):
        self._create_test_comment()
        self.grant_access(
            obj=self.test_document, permission=permission_document_comment_view
        )

        self._clear_events()

        response = self._request_test_comment_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['comment'], self.test_document_comment.comment)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_comment_edit_via_patch_api_view_no_permission(self):
        self._create_test_comment()
        comment_text = self.test_document_comment.comment

        self._clear_events()

        response = self._request_test_comment_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.test_document_comment.refresh_from_db()
        self.assertEqual(self.test_document_comment.comment, comment_text)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_comment_edit_via_patch_api_view_with_access(self):
        self._create_test_comment()
        self.grant_access(
            obj=self.test_document, permission=permission_document_comment_edit
        )
        comment_text = self.test_document_comment.comment

        self._clear_events()

        response = self._request_test_comment_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document_comment.refresh_from_db()
        self.assertNotEqual(self.test_document_comment.comment, comment_text)

        event = self._get_test_object_event()
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.target, self.test_document_comment)
        self.assertEqual(event.verb, event_document_comment_edited.id)

    def test_comment_list_api_view_no_permission(self):
        self._create_test_comment()

        self._clear_events()

        response = self._request_test_comment_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_comment_list_api_view_with_access(self):
        self._create_test_comment()
        self.grant_access(
            obj=self.test_document, permission=permission_document_comment_view
        )

        self._clear_events()

        response = self._request_test_comment_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['comment'], self.test_document_comment.comment
        )

        event = self._get_test_object_event()
        self.assertEqual(event, None)
