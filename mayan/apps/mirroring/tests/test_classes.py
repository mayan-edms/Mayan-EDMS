from __future__ import absolute_import, unicode_literals

import hashlib

from fuse import FuseOSError

from django.test import override_settings

from common.tests import BaseTestCase
from documents.tests import DocumentTestMixin

from document_indexing.tests import DocumentIndexingTestMixin

from ..classes import IndexFilesystem

from .literals import (
    TEST_NODE_EXPRESSION, TEST_NODE_EXPRESSION_MULTILINE
)


@override_settings(OCR_AUTO_OCR=False)
class IndexFSTestCase(DocumentIndexingTestMixin, DocumentTestMixin, BaseTestCase):
    auto_upload_document = False

    def test_document_access(self):
        self._create_index()

        self.index.node_templates.create(
            parent=self.index.template_root, expression=TEST_NODE_EXPRESSION,
            link_documents=True
        )

        document = self.upload_document()
        index_filesystem = IndexFilesystem(index_slug=self.index.slug)

        self.assertEqual(
            index_filesystem.access(
                '/{}/{}'.format(TEST_NODE_EXPRESSION, document.label)
            ), None
        )

    def test_document_access_failure(self):
        self._create_index()

        self.index.node_templates.create(
            parent=self.index.template_root, expression=TEST_NODE_EXPRESSION,
            link_documents=True
        )

        document = self.upload_document()
        index_filesystem = IndexFilesystem(index_slug=self.index.slug)

        with self.assertRaises(FuseOSError):
            index_filesystem.access(
                '/{}/{}_non_valid'.format(TEST_NODE_EXPRESSION, document.label)
            )

    def test_document_open(self):
        self._create_index()

        self.index.node_templates.create(
            parent=self.index.template_root, expression=TEST_NODE_EXPRESSION,
            link_documents=True
        )

        document = self.upload_document()
        index_filesystem = IndexFilesystem(index_slug=self.index.slug)

        file_handle = index_filesystem.open(
            '/{}/{}'.format(TEST_NODE_EXPRESSION, document.label), 'rb'
        )

        self.assertEqual(
            hashlib.sha256(
                index_filesystem.read(
                    path=None, size=document.size, offset=0, fh=file_handle
                )
            ).hexdigest(),
            document.checksum
        )

    def test_multiline_indexes(self):
        self._create_index()

        self.index.node_templates.create(
            parent=self.index.template_root,
            expression=TEST_NODE_EXPRESSION_MULTILINE,
            link_documents=True
        )

        self.upload_document()
        index_filesystem = IndexFilesystem(index_slug=self.index.slug)

        self.assertEqual(
            list(index_filesystem.readdir('/', ''))[2:],
            [TEST_NODE_EXPRESSION_MULTILINE.replace('\r\n', ' ')]
        )

    def test_duplicated_indexes(self):
        self._create_index()

        self.index.node_templates.create(
            parent=self.index.template_root, expression=TEST_NODE_EXPRESSION,
            link_documents=True
        )
        self.index.node_templates.create(
            parent=self.index.template_root, expression=TEST_NODE_EXPRESSION,
            link_documents=True
        )

        self.upload_document()
        index_filesystem = IndexFilesystem(index_slug=self.index.slug)

        self.assertEqual(
            list(index_filesystem.readdir('/', ''))[2:], []
        )
