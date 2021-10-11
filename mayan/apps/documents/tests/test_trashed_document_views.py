from ..events import (
    event_document_trashed, event_trashed_document_deleted,
    event_trashed_document_restored
)
from ..models.document_models import Document
from ..models.trashed_document_models import TrashedDocument
from ..permissions import (
    permission_trashed_document_delete, permission_trashed_document_restore,
    permission_document_trash, permission_document_view,
    permission_trash_empty
)

from .base import GenericDocumentViewTestCase
from .mixins.trashed_document_mixins import TrashedDocumentViewTestMixin


class DocumentTrashViewTestCase(
    TrashedDocumentViewTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_document_trash_get_view_no_permission(self):
        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        self._clear_events()

        response = self._request_test_document_trash_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Document.valid.count(), document_count)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_trash_get_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_trash
        )

        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        self._clear_events()

        response = self._request_test_document_trash_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Document.valid.count(), document_count)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_trash_get_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_trash
        )

        self.test_document.delete()

        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        self._clear_events()

        response = self._request_test_document_trash_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Document.valid.count(), document_count)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_trash_post_view_no_permission(self):
        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        self._clear_events()

        response = self._request_test_document_trash_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Document.valid.count(), document_count)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_trash_post_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_trash
        )

        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        self._clear_events()

        response = self._request_test_document_trash_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Document.valid.count(), document_count - 1)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_trashed.id)

    def test_trashed_document_trash_post_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_trash
        )

        self.test_document.delete()

        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        self._clear_events()

        response = self._request_test_document_trash_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Document.valid.count(), document_count)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class TrashedDocumentViewTestCase(
    TrashedDocumentViewTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_trashed_document_delete_get_view_no_permission(self):
        self.test_document.delete()

        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        self._clear_events()

        response = self._request_test_trashed_document_delete_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            Document.valid.count(), document_count
        )
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_delete_get_view_with_access(self):
        self.test_document.delete()
        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_trashed_document_delete
        )

        self._clear_events()

        response = self._request_test_trashed_document_delete_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            Document.valid.count(), document_count
        )
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_delete_post_view_no_permission(self):
        self.test_document.delete()
        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        self._clear_events()

        response = self._request_test_trashed_document_delete_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Document.valid.count(), document_count)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_delete_post_view_with_access(self):
        self.test_document.delete()
        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_trashed_document_delete
        )

        self._clear_events()

        response = self._request_test_trashed_document_delete_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Document.valid.count(), document_count)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_type)
        self.assertEqual(events[0].verb, event_trashed_document_deleted.id)

    def test_trashed_document_list_view_no_permission(self):
        self.test_document.delete()

        self._clear_events()

        response = self._request_test_trashed_document_list_view()
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_list_view_with_access(self):
        self.test_document.delete()

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_trashed_document_list_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_restore_get_view_no_permission(self):
        self.test_document.delete()
        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        self._clear_events()

        response = self._request_test_trashed_document_restore_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Document.valid.count(), document_count)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_restore_get_view_with_access(self):
        self.test_document.delete()
        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_trashed_document_restore
        )

        document_count = Document.valid.count()

        self._clear_events()

        response = self._request_test_trashed_document_restore_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Document.valid.count(), document_count)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_restore_post_view_no_permission(self):
        self.test_document.delete()
        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        self._clear_events()

        response = self._request_test_trashed_document_restore_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Document.valid.count(), document_count)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_restore_post_view_with_access(self):
        self.test_document.delete()
        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_trashed_document_restore
        )

        self._clear_events()

        response = self._request_test_trashed_document_restore_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Document.valid.count(), document_count + 1)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_trashed_document_restored.id)


class TrashCanViewTestCase(
    TrashedDocumentViewTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_trash_can_empty_view_no_permission(self):
        self.test_document.delete()

        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        self._clear_events()

        response = self._request_empty_trash_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Document.valid.count(), document_count)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trash_can_empty_view_with_permission(self):
        self.test_document.delete()

        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        self.grant_permission(permission=permission_trash_empty)

        self._clear_events()

        response = self._request_empty_trash_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Document.valid.count(), document_count)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_type)
        self.assertEqual(events[0].verb, event_trashed_document_deleted.id)
