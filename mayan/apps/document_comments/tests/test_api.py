from rest_framework import status

from mayan.apps.documents.tests.mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..models import Comment
from ..permissions import (
    permission_document_comment_create, permission_document_comment_delete,
    permission_document_comment_edit, permission_document_comment_view
)

from .literals import TEST_COMMENT_TEXT, TEST_COMMENT_TEXT_EDITED
from .mixins import DocumentCommentTestMixin


class CommentAPIViewTestMixin(object):
    def _request_test_comment_create_api_view(self):
        return self.post(
            viewname='rest_api:comment-list', kwargs={
                'document_pk': self.test_document.pk
            }, data={
                'comment': TEST_COMMENT_TEXT
            }
        )

    def _request_test_comment_delete_api_view(self):
        return self.delete(
            viewname='rest_api:comment-detail', kwargs={
                'document_pk': self.test_document.pk,
                'comment_pk': self.test_document_comment.pk,
            }
        )

    def _request_test_comment_detail_api_view(self):
        return self.get(
            viewname='rest_api:comment-detail', kwargs={
                'document_pk': self.test_document.pk,
                'comment_pk': self.test_document_comment.pk
            }
        )

    def _request_test_comment_edit_patch_api_view(self):
        return self.patch(
            viewname='rest_api:comment-detail', kwargs={
                'document_pk': self.test_document.pk,
                'comment_pk': self.test_document_comment.pk,
            }, data={'comment': TEST_COMMENT_TEXT_EDITED}
        )

    def _request_test_comment_list_api_view(self):
        return self.get(
            viewname='rest_api:comment-list', kwargs={
                'document_pk': self.test_document.pk
            }
        )


class CommentAPIViewTestCase(
    CommentAPIViewTestMixin, DocumentCommentTestMixin, DocumentTestMixin,
    BaseAPITestCase
):
    def test_comment_create_view_no_access(self):
        response = self._request_test_comment_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Comment.objects.count(), 0)

    def test_comment_create_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_comment_create
        )

        response = self._request_test_comment_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        comment = Comment.objects.first()
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(response.data['id'], comment.pk)

    def test_comment_delete_view_no_access(self):
        self._create_test_comment()

        response = self._request_test_comment_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertTrue(self.test_document_comment in Comment.objects.all())

    def test_comment_delete_view_with_access(self):
        self._create_test_comment()
        self.grant_access(
            obj=self.test_document, permission=permission_document_comment_delete
        )

        response = self._request_test_comment_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(self.test_document_comment in Comment.objects.all())

    def test_comment_edit_view_no_access(self):
        self._create_test_comment()
        comment_text = self.test_document_comment.comment

        response = self._request_test_comment_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.test_document_comment.refresh_from_db()
        self.assertEqual(self.test_document_comment.comment, comment_text)

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

    def test_comment_detail_view_no_access(self):
        self._create_test_comment()

        response = self._request_test_comment_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_detail_view_with_access(self):
        self._create_test_comment()
        self.grant_access(
            obj=self.test_document, permission=permission_document_comment_view
        )

        response = self._request_test_comment_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['comment'], self.test_document_comment.comment)

    def test_comment_list_view_no_access(self):
        self._create_test_comment()

        response = self._request_test_comment_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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
