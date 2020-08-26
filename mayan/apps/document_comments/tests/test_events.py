from actstream.models import Action

from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..events import (
    event_document_comment_created, event_document_comment_deleted,
    event_document_comment_edited
)
from ..models import Comment
from ..permissions import (
    permission_document_comment_create, permission_document_comment_delete,
    permission_document_comment_edit
)

from .mixins import DocumentCommentTestMixin, DocumentCommentViewTestMixin


class CommentEventsTestCase(
    DocumentCommentTestMixin, DocumentCommentViewTestMixin,
    GenericDocumentViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_user()

    def test_comment_create_event_no_permission(self):
        action_count = Action.objects.count()

        response = self._request_test_comment_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Action.objects.count(), action_count)

    def test_comment_create_event_with_permissions(self):
        self.grant_permission(permission=permission_document_comment_create)

        action_count = Action.objects.count()

        response = self._request_test_comment_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Action.objects.count(), action_count + 1)

        event = Action.objects.first()

        comment = Comment.objects.first()

        self.assertEqual(event.action_object, self.test_document)
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.target, comment)
        self.assertEqual(event.verb, event_document_comment_created.id)

    def test_comment_delete_event_no_permission(self):
        self._create_test_comment()

        action_count = Action.objects.count()

        response = self._request_test_comment_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Action.objects.count(), action_count)

    def test_comment_delete_event_with_access(self):
        self._create_test_comment()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_comment_delete
        )

        action_count = Action.objects.count()

        response = self._request_test_comment_delete_view()
        self.assertEqual(response.status_code, 302)
        # Total count remains the same. Document comment created is removed due
        # to cascade delete, document comment deleted event is added.
        self.assertEqual(Action.objects.count(), action_count)

        event = Action.objects.first()

        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.target, self.test_document)
        self.assertEqual(event.verb, event_document_comment_deleted.id)

    def test_comment_edit_event_no_permission(self):
        self._create_test_comment()

        action_count = Action.objects.count()

        response = self._request_test_comment_edit_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Action.objects.count(), action_count)

    def test_comment_edit_event_with_access(self):
        self._create_test_comment()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_comment_edit
        )

        action_count = Action.objects.count()

        response = self._request_test_comment_edit_view()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Action.objects.count(), action_count + 1)

        event = Action.objects.first()

        self.assertEqual(event.action_object, self.test_document)
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.target, self.test_document_comment)
        self.assertEqual(event.verb, event_document_comment_edited.id)
