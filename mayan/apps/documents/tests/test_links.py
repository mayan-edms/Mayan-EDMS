from django.urls import reverse

from ..links.document_file_links import (
    link_document_file_delete, link_document_file_download_quick
)
from ..links.trashed_document_links import link_document_restore
from ..models import TrashedDocument
from ..permissions import (
    permission_document_file_delete, permission_document_file_download,
    permission_trashed_document_restore
)

from .base import GenericDocumentViewTestCase
from .mixins.document_file_mixins import DocumentFileTestMixin


class DocumentsLinksTestCase(
    DocumentFileTestMixin, GenericDocumentViewTestCase
):
    def test_document_file_delete_link_no_permission(self):
        self._upload_test_document_file()

        self.assertTrue(self._test_document.files.count(), 2)

        self.add_test_view(test_object=self._test_document.files.first())
        context = self.get_test_view()
        resolved_link = link_document_file_delete.resolve(context=context)

        self.assertEqual(resolved_link, None)

    def test_document_file_delete_link_with_permission(self):
        self._upload_test_document_file()

        self.assertTrue(self._test_document.files.count(), 2)

        self.grant_access(
            obj=self._test_document,
            permission=permission_document_file_delete
        )

        self.add_test_view(test_object=self._test_document.files.first())
        context = self.get_test_view()
        resolved_link = link_document_file_delete.resolve(context=context)

        self.assertNotEqual(resolved_link, None)
        self.assertEqual(
            resolved_link.url,
            reverse(
                viewname=link_document_file_delete.view,
                args=(self._test_document.files.first().pk,)
            )
        )

    def test_document_file_download_link_no_permission(self):
        self.add_test_view(test_object=self._test_document.file_latest)
        context = self.get_test_view()
        resolved_link = link_document_file_download_quick.resolve(context=context)

        self.assertEqual(resolved_link, None)

    def test_document_file_download_link_with_permission(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_file_download
        )

        self.add_test_view(test_object=self._test_document.file_latest)
        context = self.get_test_view()
        resolved_link = link_document_file_download_quick.resolve(context=context)

        self.assertNotEqual(resolved_link, None)
        self.assertEqual(
            resolved_link.url,
            reverse(
                viewname=link_document_file_download_quick.view,
                args=(self._test_document.file_latest.pk,)
            )
        )


class TrashedDocumentsLinksTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super().setUp()
        self._test_document.delete()
        self.test_trashed_document = TrashedDocument.objects.get(
            pk=self._test_document.pk
        )
        self.add_test_view(test_object=self.test_trashed_document)
        self.context = self.get_test_view()

    def test_trashed_document_restore_link_no_permission(self):
        resolved_link = link_document_restore.resolve(context=self.context)
        self.assertEqual(resolved_link, None)

    def test_trashed_document_restore_link_with_permission(self):
        self.grant_access(
            obj=self._test_document, permission=permission_trashed_document_restore
        )
        resolved_link = link_document_restore.resolve(context=self.context)
        self.assertNotEqual(resolved_link, None)
        self.assertEqual(
            resolved_link.url,
            reverse(
                viewname=link_document_restore.view,
                args=(self.test_trashed_document.pk,)
            )
        )
