from __future__ import unicode_literals

import time

from django.urls import reverse

from ..links import (
    link_document_restore, link_document_version_download,
    link_document_version_revert
)
from ..models import DeletedDocument
from ..permissions import (
    permission_document_download, permission_document_restore,
    permission_document_version_revert
)

from .base import GenericDocumentViewTestCase
from .literals import TEST_SMALL_DOCUMENT_PATH


class DocumentsLinksTestCase(GenericDocumentViewTestCase):
    def test_document_version_revert_link_no_permission(self):
        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.test_document.new_version(file_object=file_object)

        self.assertTrue(self.test_document.versions.count(), 2)

        self.add_test_view(test_object=self.test_document.versions.first())
        context = self.get_test_view()
        resolved_link = link_document_version_revert.resolve(context=context)

        self.assertEqual(resolved_link, None)

    def test_document_version_revert_link_with_permission(self):
        # Needed by MySQL as milliseconds value is not store in timestamp
        # field
        time.sleep(1.01)

        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.test_document.new_version(file_object=file_object)

        self.assertTrue(self.test_document.versions.count(), 2)

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_revert
        )

        self.add_test_view(test_object=self.test_document.versions.first())
        context = self.get_test_view()
        resolved_link = link_document_version_revert.resolve(context=context)

        self.assertNotEqual(resolved_link, None)
        self.assertEqual(
            resolved_link.url,
            reverse(
                viewname=link_document_version_revert.view,
                args=(self.test_document.versions.first().pk,)
            )
        )

    def test_document_version_download_link_no_permission(self):
        self.add_test_view(test_object=self.test_document.latest_version)
        context = self.get_test_view()
        resolved_link = link_document_version_download.resolve(context=context)

        self.assertEqual(resolved_link, None)

    def test_document_version_download_link_with_permission(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_download
        )

        self.add_test_view(test_object=self.test_document.latest_version)
        context = self.get_test_view()
        resolved_link = link_document_version_download.resolve(context=context)

        self.assertNotEqual(resolved_link, None)
        self.assertEqual(
            resolved_link.url,
            reverse(
                viewname=link_document_version_download.view,
                args=(self.test_document.latest_version.pk,)
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
            obj=self.test_document, permission=permission_document_restore
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
