from ..models import DeletedDocument, Document
from ..permissions import (
    permission_document_delete, permission_document_restore,
    permission_document_trash, permission_document_view
)

from .base import GenericDocumentViewTestCase
from .mixins import TrashedDocumentViewTestMixin


class TrashedDocumentViewTestCase(
    TrashedDocumentViewTestMixin, GenericDocumentViewTestCase
):
    def test_document_trash_get_view_no_permissions(self):
        document_count = Document.objects.count()

        response = self._request_document_trash_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Document.objects.count(), document_count)

    def test_document_trash_get_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_trash
        )

        document_count = Document.objects.count()

        response = self._request_document_trash_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Document.objects.count(), document_count)

    def test_document_trash_post_view_no_permissions(self):
        response = self._request_document_trash_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(DeletedDocument.objects.count(), 0)
        self.assertEqual(Document.objects.count(), 1)

    def test_document_trash_post_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_trash
        )

        response = self._request_document_trash_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(DeletedDocument.objects.count(), 1)
        self.assertEqual(Document.objects.count(), 0)

    def test_trashed_document_restore_get_view_no_permission(self):
        self.test_document.delete()
        self.assertEqual(Document.objects.count(), 0)

        document_count = Document.objects.count()

        response = self._request_trashed_document_restore_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Document.objects.count(), document_count)

    def test_trashed_document_restore_get_view_with_access(self):
        self.test_document.delete()
        self.assertEqual(Document.objects.count(), 0)

        self.grant_access(
            obj=self.test_document, permission=permission_document_restore
        )

        document_count = Document.objects.count()

        response = self._request_trashed_document_restore_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Document.objects.count(), document_count)

    def test_trashed_document_restore_post_view_no_permission(self):
        self.test_document.delete()
        self.assertEqual(Document.objects.count(), 0)

        response = self._request_trashed_document_restore_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(DeletedDocument.objects.count(), 1)
        self.assertEqual(Document.objects.count(), 0)

    def test_trashed_document_restore_post_view_with_access(self):
        self.test_document.delete()
        self.assertEqual(Document.objects.count(), 0)

        self.grant_access(
            obj=self.test_document, permission=permission_document_restore
        )

        response = self._request_trashed_document_restore_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(DeletedDocument.objects.count(), 0)
        self.assertEqual(Document.objects.count(), 1)

    def test_trashed_document_delete_get_view_no_permissions(self):
        self.test_document.delete()
        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(DeletedDocument.objects.count(), 1)

        trashed_document_count = DeletedDocument.objects.count()

        response = self._request_trashed_document_delete_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            DeletedDocument.objects.count(), trashed_document_count
        )

    def test_trashed_document_delete_get_view_with_access(self):
        self.test_document.delete()
        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(DeletedDocument.objects.count(), 1)

        self.grant_access(
            obj=self.test_document, permission=permission_document_delete
        )

        trashed_document_count = DeletedDocument.objects.count()

        response = self._request_trashed_document_delete_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            DeletedDocument.objects.count(), trashed_document_count
        )

    def test_trashed_document_delete_post_view_no_permissions(self):
        self.test_document.delete()
        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(DeletedDocument.objects.count(), 1)

        response = self._request_trashed_document_delete_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(DeletedDocument.objects.count(), 1)

    def test_trashed_document_delete_post_view_with_access(self):
        self.test_document.delete()
        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(DeletedDocument.objects.count(), 1)

        self.grant_access(
            obj=self.test_document, permission=permission_document_delete
        )

        response = self._request_trashed_document_delete_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(DeletedDocument.objects.count(), 0)
        self.assertEqual(Document.objects.count(), 0)

    def test_trashed_document_list_view_no_permissions(self):
        self.test_document.delete()

        response = self._request_trashed_document_list_view()
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )

    def test_trashed_document_list_view_with_access(self):
        self.test_document.delete()

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_trashed_document_list_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )
