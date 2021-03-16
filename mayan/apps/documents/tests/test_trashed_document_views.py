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
    def test_document_trash_get_view_no_permission(self):
        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        response = self._request_test_document_trash_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Document.valid.count(), document_count)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count
        )

    def test_document_trash_get_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_trash
        )

        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        response = self._request_test_document_trash_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Document.valid.count(), document_count)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count
        )

    def test_trashed_document_trash_get_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_trash
        )

        self.test_document.delete()

        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        response = self._request_test_document_trash_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Document.valid.count(), document_count)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count
        )

    def test_document_trash_post_view_no_permission(self):
        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        response = self._request_test_document_trash_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Document.valid.count(), document_count)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count
        )

    def test_document_trash_post_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_trash
        )

        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        response = self._request_test_document_trash_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Document.valid.count(), document_count - 1)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count + 1
        )

    def test_trashed_document_trash_post_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_trash
        )

        self.test_document.delete()

        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        response = self._request_test_document_trash_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Document.valid.count(), document_count)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count
        )


class TrashedDocumentViewTestCase(
    TrashedDocumentViewTestMixin, GenericDocumentViewTestCase
):
    def test_trashed_document_delete_get_view_no_permission(self):
        self.test_document.delete()

        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        response = self._request_test_trashed_document_delete_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            Document.valid.count(), document_count
        )
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count
        )

    def test_trashed_document_delete_get_view_with_access(self):
        self.test_document.delete()
        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_trashed_document_delete
        )

        response = self._request_test_trashed_document_delete_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            Document.valid.count(), document_count
        )
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count
        )

    def test_trashed_document_delete_post_view_no_permission(self):
        self.test_document.delete()
        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        response = self._request_test_trashed_document_delete_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Document.valid.count(), document_count)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count
        )

    def test_trashed_document_delete_post_view_with_access(self):
        self.test_document.delete()
        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        self.grant_access(
            obj=self.test_document, permission=permission_trashed_document_delete
        )

        response = self._request_test_trashed_document_delete_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Document.valid.count(), document_count)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count - 1
        )

    def test_trashed_document_list_view_no_permission(self):
        self.test_document.delete()

        response = self._request_test_trashed_document_list_view()
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )

    def test_trashed_document_list_view_with_access(self):
        self.test_document.delete()

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_trashed_document_list_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )

    def test_trashed_document_restore_get_view_no_permission(self):
        self.test_document.delete()
        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        response = self._request_test_trashed_document_restore_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Document.valid.count(), document_count)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count
        )

    def test_trashed_document_restore_get_view_with_access(self):
        self.test_document.delete()
        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_trashed_document_restore
        )

        document_count = Document.valid.count()

        response = self._request_test_trashed_document_restore_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Document.valid.count(), document_count)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count
        )

    def test_trashed_document_restore_post_view_no_permission(self):
        self.test_document.delete()
        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        response = self._request_test_trashed_document_restore_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Document.valid.count(), document_count)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count
        )

    def test_trashed_document_restore_post_view_with_access(self):
        self.test_document.delete()
        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_trashed_document_restore
        )

        response = self._request_test_trashed_document_restore_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Document.valid.count(), document_count + 1)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count - 1
        )


class TrashCanViewTestCase(
    TrashedDocumentViewTestMixin, GenericDocumentViewTestCase
):
    def test_trash_can_empty_view_no_permission(self):
        self.test_document.delete()

        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        response = self._request_empty_trash_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Document.valid.count(), document_count)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count
        )

    def test_trash_can_empty_view_with_permission(self):
        self.test_document.delete()

        document_count = Document.valid.count()
        trashed_document_count = TrashedDocument.objects.count()

        self.grant_permission(permission=permission_trash_empty)

        response = self._request_empty_trash_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Document.valid.count(), document_count)
        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count - 1
        )
