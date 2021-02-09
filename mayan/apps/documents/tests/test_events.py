from actstream.models import Action

from ..events import event_document_trashed, event_document_viewed
from ..permissions import permission_document_trash, permission_document_view

from .base import GenericDocumentViewTestCase
from .mixins.document_mixins import DocumentViewTestMixin
from .mixins.trashed_document_mixins import TrashedDocumentViewTestMixin


class DocumentEventsTestCase(
    DocumentViewTestMixin, TrashedDocumentViewTestMixin,
    GenericDocumentViewTestCase
):
    def setUp(self):
        super().setUp()
        Action.objects.all().delete()

    def test_document_view_event_no_permission(self):
        response = self._request_test_document_preview_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(list(Action.objects.any(obj=self.test_document)), [])

    def test_document_view_event_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_document_preview_view()
        self.assertEqual(response.status_code, 200)

        event = Action.objects.any(obj=self.test_document).first()
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.target, self.test_document)
        self.assertEqual(event.verb, event_document_viewed.id)

    def test_document_trashed_view_event_no_permission(self):
        response = self._request_test_document_trash_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(list(Action.objects.any(obj=self.test_document)), [])

    def test_document_trashed_view_event_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_trash
        )

        response = self._request_test_document_trash_post_view()
        self.assertEqual(response.status_code, 302)

        event = Action.objects.any(obj=self.test_document).first()
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.target, self.test_document)
        self.assertEqual(event.verb, event_document_trashed.id)
