from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..events import (
    event_document_comment_created, event_document_comment_deleted,
    event_document_comment_edited
)
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
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_user()
        self._create_test_document_stub()

    def test_comment_create_view_no_permission(self):
        comment_count = Comment.objects.count()

        self._clear_events()

        response = self._request_test_comment_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Comment.objects.count(), comment_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_comment_create_view_with_permissions(self):
        comment_count = Comment.objects.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_comment_create
        )

        self._clear_events()

        response = self._request_test_comment_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Comment.objects.count(), comment_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_comment)
        self.assertEqual(events[0].verb, event_document_comment_created.id)

    def test_trashed_document_comment_create_view_with_permissions(self):
        comment_count = Comment.objects.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_comment_create
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_comment_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Comment.objects.count(), comment_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_comment_delete_view_no_permission(self):
        self._create_test_comment()

        comment_count = Comment.objects.count()

        self._clear_events()

        response = self._request_test_comment_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Comment.objects.count(), comment_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_comment_delete_view_with_access(self):
        self._create_test_comment()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_comment_delete
        )

        comment_count = Comment.objects.count()

        self._clear_events()

        response = self._request_test_comment_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Comment.objects.count(), comment_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_comment_deleted.id)

    def test_trashed_document_comment_delete_view_with_access(self):
        self._create_test_comment()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_comment_delete
        )

        self.test_document.delete()

        comment_count = Comment.objects.count()

        self._clear_events()

        response = self._request_test_comment_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Comment.objects.count(), comment_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_comment_detail_view_no_permission(self):
        self._create_test_comment()

        self._clear_events()

        response = self._request_test_comment_detail_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_comment_detail_view_with_access(self):
        self._create_test_comment()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_comment_view
        )

        self._clear_events()

        response = self._request_test_comment_detail_view()
        self.assertContains(
            response=response, text=self.test_document_comment.text,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_documen_comment_detail_view_with_access(self):
        self._create_test_comment()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_comment_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_comment_detail_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_comment_edit_view_no_permission(self):
        self._create_test_comment()

        comment_text = self.test_document_comment.text

        self._clear_events()

        response = self._request_test_comment_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_document_comment.refresh_from_db()
        self.assertEqual(self.test_document_comment.text, comment_text)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_comment_edit_view_with_access(self):
        self._create_test_comment()

        self.grant_access(
            obj=self.test_document, permission=permission_document_comment_edit
        )

        comment_text = self.test_document_comment.text

        self._clear_events()

        response = self._request_test_comment_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_document_comment.refresh_from_db()
        self.assertNotEqual(self.test_document_comment.text, comment_text)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_comment)
        self.assertEqual(events[0].verb, event_document_comment_edited.id)

    def test_trashed_document_comment_edit_view_with_access(self):
        self._create_test_comment()

        self.grant_access(
            obj=self.test_document, permission=permission_document_comment_edit
        )

        comment_text = self.test_document_comment.text

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_comment_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_document_comment.refresh_from_db()
        self.assertEqual(self.test_document_comment.text, comment_text)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_comment_list_view_with_no_permission(self):
        self._create_test_comment()

        self._clear_events()

        response = self._request_test_comment_list_view()
        self.assertNotContains(
            response=response, text=self.test_document_comment.text,
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_comment_list_view_with_access(self):
        self._create_test_comment()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_comment_view
        )

        self._clear_events()

        response = self._request_test_comment_list_view()
        self.assertContains(
            response=response, text=self.test_document_comment.text,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_comment_list_view_with_access(self):
        self._create_test_comment()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_comment_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_comment_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
