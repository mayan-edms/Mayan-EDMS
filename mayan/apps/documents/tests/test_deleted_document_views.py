# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ..models import DeletedDocument, Document
from ..permissions import (
    permission_document_delete, permission_document_restore,
    permission_document_trash, permission_document_view
)

from .base import GenericDocumentViewTestCase


class DeletedDocumentTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(DeletedDocumentTestCase, self).setUp()
        self.login_user()

    def test_document_restore_view_no_permission(self):
        self.document.delete()
        self.assertEqual(Document.objects.count(), 0)

        response = self.post(
            'documents:document_restore', args=(self.document.pk,)
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(DeletedDocument.objects.count(), 1)
        self.assertEqual(Document.objects.count(), 0)

    def test_document_restore_view_with_access(self):
        self.document.delete()
        self.assertEqual(Document.objects.count(), 0)

        self.grant_access(
            obj=self.document, permission=permission_document_restore
        )
        response = self.post(
            'documents:document_restore', args=(self.document.pk,),
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DeletedDocument.objects.count(), 0)
        self.assertEqual(Document.objects.count(), 1)

    def test_document_trash_no_permissions(self):
        response = self.post(
            'documents:document_trash', args=(self.document.pk,)
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(DeletedDocument.objects.count(), 0)
        self.assertEqual(Document.objects.count(), 1)

    def test_document_trash_with_access(self):
        self.grant_access(
            obj=self.document, permission=permission_document_trash
        )

        response = self.post(
            'documents:document_trash', args=(self.document.pk,),
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(DeletedDocument.objects.count(), 1)
        self.assertEqual(Document.objects.count(), 0)

    def test_document_delete_no_permissions(self):
        self.document.delete()
        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(DeletedDocument.objects.count(), 1)

        response = self.post(
            'documents:document_delete', args=(self.document.pk,),
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(DeletedDocument.objects.count(), 1)

    def test_document_delete_with_access(self):
        self.document.delete()
        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(DeletedDocument.objects.count(), 1)

        self.grant_access(
            obj=self.document, permission=permission_document_delete
        )

        response = self.post(
            'documents:document_delete', args=(self.document.pk,),
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DeletedDocument.objects.count(), 0)
        self.assertEqual(Document.objects.count(), 0)

    def test_deleted_document_list_view_no_permissions(self):
        self.document.delete()

        response = self.get('documents:document_list_deleted')

        self.assertNotContains(response, self.document.label, status_code=200)

    def test_deleted_document_list_view_with_access(self):
        self.document.delete()

        self.grant_access(
            obj=self.document, permission=permission_document_view
        )
        response = self.get('documents:document_list_deleted')

        self.assertContains(response, self.document.label, status_code=200)
