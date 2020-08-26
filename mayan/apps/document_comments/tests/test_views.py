from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..models import Comment
from ..permissions import (
    permission_document_comment_create, permission_document_comment_delete,
    permission_document_comment_edit, permission_document_comment_view
)

from .mixins import DocumentCommentTestMixin, DocumentCommentViewTestMixin


class DocumentCommentViewTestCase(
    DocumentCommentViewTestMixin, DocumentCommentTestMixin,
    GenericDocumentViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_user()

    def test_comment_create_view_no_permission(self):
        comment_count = Comment.objects.count()

        response = self._request_test_comment_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(comment_count, Comment.objects.count())

    def test_comment_create_view_with_permissions(self):
        comment_count = Comment.objects.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_comment_create
        )
        response = self._request_test_comment_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(comment_count + 1, Comment.objects.count())

    def test_comment_delete_view_no_permission(self):
        self._create_test_comment()

        comment_count = Comment.objects.count()

        response = self._request_test_comment_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Comment.objects.count(), comment_count)

    def test_comment_delete_view_with_access(self):
        self._create_test_comment()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_comment_delete
        )

        comment_count = Comment.objects.count()

        response = self._request_test_comment_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Comment.objects.count(), comment_count - 1)

    def test_comment_edit_view_no_permission(self):
        self._create_test_comment()

        comment_text = self.test_document_comment.comment

        response = self._request_test_comment_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_document_comment.refresh_from_db()
        self.assertEqual(self.test_document_comment.comment, comment_text)

    def test_comment_edit_view_with_access(self):
        self._create_test_comment()

        self.grant_access(
            obj=self.test_document, permission=permission_document_comment_edit
        )

        comment_text = self.test_document_comment.comment

        response = self._request_test_comment_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_document_comment.refresh_from_db()
        self.assertNotEqual(self.test_document_comment.comment, comment_text)

    def test_comment_list_view_with_no_permission(self):
        self._create_test_comment()

        response = self._request_test_comment_list_view()
        self.assertNotContains(
            response=response, text=self.test_document_comment.comment,
            status_code=404
        )

    def test_comment_list_view_with_access(self):
        self._create_test_comment()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_comment_view
        )

        response = self._request_test_comment_list_view()
        self.assertContains(
            response=response, text=self.test_document_comment.comment,
            status_code=200
        )
