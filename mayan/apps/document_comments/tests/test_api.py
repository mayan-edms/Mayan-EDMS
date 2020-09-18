from rest_framework import status

from mayan.apps.documents.tests.mixins import DocumentTestMixin
from mayan.apps.events.tests.mixins import EventTestCaseMixin
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
    EventTestCaseMixin, BaseAPITestCase
):
    _test_event_object_name = 'test_document_comment'

    def setUp(self):
        super().setUp()
        self._create_test_user()

    def test_comment_create_view_no_permission(self):
        response = self._request_test_comment_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Comment.objects.count(), 0)

        event = self._get_test_object_event()
        self.assertNotEqual(event.verb, event_document_comment_created.id)

    def test_comment_create_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_comment_create
        )

        response = self._request_test_comment_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        comment = Comment.objects.first()
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(response.data['id'], comment.pk)

        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_document_comment_created.id)
        self.assertEqual(event.actor, self._test_case_user)

    def test_comment_delete_view_no_permission(self):
        self._create_test_comment()

        response = self._request_test_comment_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertTrue(self.test_document_comment in Comment.objects.all())

        event = self._get_test_object_event(object_name='test_document')
        self.assertEqual(event.verb, event_document_comment_created.id)
        self.assertEqual(event.actor, self.test_user)

    def test_comment_delete_view_with_access(self):
        self._create_test_comment()
        self.grant_access(
            obj=self.test_document, permission=permission_document_comment_delete
        )

        response = self._request_test_comment_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(self.test_document_comment in Comment.objects.all())

        event = self._get_test_object_event(object_name='test_document')
        self.assertEqual(event.verb, event_document_comment_deleted.id)
        self.assertEqual(event.actor, self._test_case_user)

    def test_comment_edit_view_no_permission(self):
        self._create_test_comment()
        comment_text = self.test_document_comment.comment

        response = self._request_test_comment_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.test_document_comment.refresh_from_db()
        self.assertEqual(self.test_document_comment.comment, comment_text)

        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_document_comment_created.id)
        self.assertEqual(event.actor, self.test_user)

    def test_comment_edit_view_with_access(self):
        self._create_test_comment()
        self.grant_access(
            obj=self.test_document, permission=permission_document_comment_edit
        )
        comment_text = self.test_document_comment.comment

        response = self._request_test_comment_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document_comment.refresh_from_db()
        self.assertNotEqual(self.test_document_comment.comment, comment_text)

        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_document_comment_edited.id)
        self.assertEqual(event.actor, self._test_case_user)

    def test_comment_detail_view_no_permission(self):
        self._create_test_comment()

        response = self._request_test_comment_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_document_comment_created.id)
        self.assertEqual(event.actor, self.test_user)

    def test_comment_detail_view_with_access(self):
        self._create_test_comment()
        self.grant_access(
            obj=self.test_document, permission=permission_document_comment_view
        )

        response = self._request_test_comment_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['comment'], self.test_document_comment.comment)

        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_document_comment_created.id)
        self.assertEqual(event.actor, self.test_user)

    def test_comment_list_view_no_permission(self):
        self._create_test_comment()

        response = self._request_test_comment_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_document_comment_created.id)
        self.assertEqual(event.actor, self.test_user)

    def test_comment_list_view_with_access(self):
        self._create_test_comment()
        self.grant_access(
            obj=self.test_document, permission=permission_document_comment_view
        )

        response = self._request_test_comment_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['comment'], self.test_document_comment.comment
        )

        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_document_comment_created.id)
        self.assertEqual(event.actor, self.test_user)
