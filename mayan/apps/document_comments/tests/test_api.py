from __future__ import unicode_literals

from django.test import override_settings

from rest_framework import status

from documents.tests import DocumentTestMixin
from rest_api.tests import BaseAPITestCase

from ..models import Comment
from ..permissions import (
    permission_comment_create, permission_comment_delete,
    permission_comment_view
)

from .literals import TEST_COMMENT_TEXT


@override_settings(OCR_AUTO_OCR=False)
class CommentAPITestCase(DocumentTestMixin, BaseAPITestCase):
    def setUp(self):
        super(CommentAPITestCase, self).setUp()
        self.login_user()

    def _create_comment(self):
        return self.document.comments.create(
            comment=TEST_COMMENT_TEXT, user=self.admin_user
        )

    def _request_comment_create_view(self):
        return self.post(
            viewname='rest_api:comment-list', args=(self.document.pk,),
            data={
                'comment': TEST_COMMENT_TEXT
            }
        )

    def test_comment_create_view_no_access(self):
        response = self._request_comment_create_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Comment.objects.count(), 0)

    def test_comment_create_view_with_access(self):
        self.grant_access(permission=permission_comment_create, obj=self.document)
        response = self._request_comment_create_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        comment = Comment.objects.first()
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(response.data['id'], comment.pk)

    def _request_comment_delete_view(self):
        return self.delete(
            viewname='rest_api:comment-detail', args=(
                self.document.pk, self.comment.pk,
            )
        )

    def test_comment_delete_view_no_access(self):
        self.comment = self._create_comment()
        response = self._request_comment_delete_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(self.comment in Comment.objects.all())

    def test_comment_delete_view_with_access(self):
        self.comment = self._create_comment()
        self.grant_access(
            permission=permission_comment_delete, obj=self.document
        )
        response = self._request_comment_delete_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.comment in Comment.objects.all())

    def _request_comment_view(self):
        return self.get(
            viewname='rest_api:comment-detail', args=(
                self.document.pk, self.comment.pk,
            )
        )

    def test_comment_detail_view_no_access(self):
        self.comment = self._create_comment()
        response = self._request_comment_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_detail_view_with_access(self):
        self.comment = self._create_comment()
        self.grant_access(
            permission=permission_comment_view, obj=self.document
        )
        response = self._request_comment_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['comment'], self.comment.comment)

    def _request_comment_list_view(self):
        return self.get(
            viewname='rest_api:comment-list', args=(self.document.pk,)
        )

    def test_comment_list_view_no_access(self):
        self.comment = self._create_comment()
        response = self._request_comment_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_list_view_with_access(self):
        self.comment = self._create_comment()
        self.grant_access(
            permission=permission_comment_view, obj=self.document
        )
        response = self._request_comment_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['comment'], self.comment.comment
        )
