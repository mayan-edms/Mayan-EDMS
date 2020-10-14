import time

from django.urls import reverse

from ..links.document_file_links import (
    link_document_file_download, link_document_file_delete
)
from ..links.trashed_document_links import link_document_restore
from ..models import DeletedDocument
from ..permissions import (
    permission_document_file_download, permission_document_edit,
    permission_trashed_document_restore, permission_document_file_delete
)

from .base import GenericDocumentViewTestCase
from .literals import TEST_SMALL_DOCUMENT_PATH


class DocumentsLinksTestCase(GenericDocumentViewTestCase):
    def test_document_file_delete_link_no_permission(self):
        with open(file=TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.test_document.new_file(file_object=file_object)

        self.assertTrue(self.test_document.files.count(), 2)

        self.add_test_view(test_object=self.test_document.files.first())
        context = self.get_test_view()
        resolved_link = link_document_file_delete.resolve(context=context)

        self.assertEqual(resolved_link, None)

    def test_document_file_delete_link_with_permission(self):
        # Needed by MySQL as milliseconds value is not store in timestamp
        # field
        time.sleep(1.01)

        with open(file=TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.test_document.new_file(file_object=file_object)

        self.assertTrue(self.test_document.files.count(), 2)

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_delete
        )

        self.add_test_view(test_object=self.test_document.files.first())
        context = self.get_test_view()
        resolved_link = link_document_file_delete.resolve(context=context)

        self.assertNotEqual(resolved_link, None)
        self.assertEqual(
            resolved_link.url,
            reverse(
                viewname=link_document_file_delete.view,
                args=(self.test_document.files.first().pk,)
            )
        )

    def test_document_file_download_link_no_permission(self):
        self.add_test_view(test_object=self.test_document.latest_file)
        context = self.get_test_view()
        resolved_link = link_document_file_download.resolve(context=context)

        self.assertEqual(resolved_link, None)

    def test_document_file_download_link_with_permission(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_download
        )

        self.add_test_view(test_object=self.test_document.latest_file)
        context = self.get_test_view()
        resolved_link = link_document_file_download.resolve(context=context)

        self.assertNotEqual(resolved_link, None)
        self.assertEqual(
            resolved_link.url,
            reverse(
                viewname=link_document_file_download.view,
                args=(self.test_document.latest_file.pk,)
            )
        )


class DeletedDocumentsLinksTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(DeletedDocumentsLinksTestCase, self).setUp()
        self.test_document.delete()
        self.test_deleted_document = DeletedDocument.objects.get(
            pk=self.test_document.pk
        )
        self.add_test_view(test_object=self.test_deleted_document)
        self.context = self.get_test_view()

    def test_deleted_document_restore_link_no_permission(self):
        resolved_link = link_document_restore.resolve(context=self.context)
        self.assertEqual(resolved_link, None)

    def test_deleted_document_restore_link_with_permission(self):
        self.grant_access(
            obj=self.test_document, permission=permission_trashed_document_restore
        )
        resolved_link = link_document_restore.resolve(context=self.context)
        self.assertNotEqual(resolved_link, None)
        self.assertEqual(
            resolved_link.url,
            reverse(
                viewname=link_document_restore.view,
                args=(self.test_deleted_document.pk,)
            )
        )
