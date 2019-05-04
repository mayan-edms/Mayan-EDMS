from __future__ import unicode_literals

from ..models import DeletedDocument, Document
from ..permissions import (
    permission_document_delete, permission_document_restore,
    permission_document_trash, permission_document_view
)

from .base import GenericDocumentViewTestCase


class TrashedDocumentTestCase(GenericDocumentViewTestCase):
    def _request_document_restore_view(self):
        return self.post(
            viewname='documents:document_restore', kwargs={
                'pk': self.test_document.pk
            }
        )

    def test_document_restore_view_no_permission(self):
        self.test_document.delete()
        self.assertEqual(Document.objects.count(), 0)

        response = self._request_document_restore_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(DeletedDocument.objects.count(), 1)
        self.assertEqual(Document.objects.count(), 0)

    def test_document_restore_view_with_access(self):
        self.test_document.delete()
        self.assertEqual(Document.objects.count(), 0)

        self.grant_access(
            obj=self.test_document, permission=permission_document_restore
        )

        response = self._request_document_restore_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(DeletedDocument.objects.count(), 0)
        self.assertEqual(Document.objects.count(), 1)

    def _request_document_trash_view(self):
        return self.post(
            viewname='documents:document_trash', kwargs={
                'pk': self.test_document.pk
            }
        )

    def test_document_trash_no_permissions(self):
        response = self._request_document_trash_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(DeletedDocument.objects.count(), 0)
        self.assertEqual(Document.objects.count(), 1)

    def test_document_trash_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_trash
        )

        response = self._request_document_trash_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(DeletedDocument.objects.count(), 1)
        self.assertEqual(Document.objects.count(), 0)

    def _request_document_delete_view(self):
        return self.post(
            viewname='documents:document_delete', kwargs={
                'pk': self.test_document.pk
            }
        )

    def test_document_delete_no_permissions(self):
        self.test_document.delete()
        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(DeletedDocument.objects.count(), 1)

        response = self._request_document_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(DeletedDocument.objects.count(), 1)

    def test_document_delete_with_access(self):
        self.test_document.delete()
        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(DeletedDocument.objects.count(), 1)

        self.grant_access(
            obj=self.test_document, permission=permission_document_delete
        )

        response = self._request_document_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(DeletedDocument.objects.count(), 0)
        self.assertEqual(Document.objects.count(), 0)

    def _request_document_list_deleted_view(self):
        return self.get(viewname='documents:document_list_deleted')

    def test_deleted_document_list_view_no_permissions(self):
        self.test_document.delete()

        response = self._request_document_list_deleted_view()
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )

    def test_deleted_document_list_view_with_access(self):
        self.test_document.delete()

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_document_list_deleted_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )
