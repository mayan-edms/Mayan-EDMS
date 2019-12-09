from __future__ import absolute_import, unicode_literals

import hashlib

from fuse import FuseOSError

from mayan.apps.common.tests.base import BaseTestCase
from mayan.apps.documents.models import Document
from mayan.apps.documents.tests.mixins import DocumentTestMixin
from mayan.apps.document_indexing.tests.mixins import IndexTestMixin

from ..filesystems import IndexFilesystem

from .literals import (
    TEST_NODE_EXPRESSION, TEST_NODE_EXPRESSION_MULTILINE,
    TEST_NODE_EXPRESSION_MULTILINE_EXPECTED, TEST_NODE_EXPRESSION_MULTILINE_2,
    TEST_NODE_EXPRESSION_MULTILINE_2_EXPECTED
)


class IndexFilesystemTestCase(IndexTestMixin, DocumentTestMixin, BaseTestCase):
    auto_upload_document = False

    def test_document_access(self):
        self._create_test_index()

        self.test_index.node_templates.create(
            parent=self.test_index.template_root, expression=TEST_NODE_EXPRESSION,
            link_documents=True
        )

        self.upload_document()
        index_filesystem = IndexFilesystem(index_slug=self.test_index.slug)

        self.assertEqual(
            index_filesystem.access(
                '/{}/{}'.format(TEST_NODE_EXPRESSION, self.test_document.label)
            ), None
        )

    def test_document_access_failure(self):
        self._create_test_index()

        self.test_index.node_templates.create(
            parent=self.test_index.template_root, expression=TEST_NODE_EXPRESSION,
            link_documents=True
        )

        self.upload_document()
        index_filesystem = IndexFilesystem(index_slug=self.test_index.slug)

        with self.assertRaises(FuseOSError):
            index_filesystem.access(
                '/{}/{}_non_valid'.format(TEST_NODE_EXPRESSION, self.test_document.label)
            )

    def test_document_open(self):
        self._create_test_index()

        self.test_index.node_templates.create(
            parent=self.test_index.template_root, expression=TEST_NODE_EXPRESSION,
            link_documents=True
        )

        self.upload_document()
        index_filesystem = IndexFilesystem(index_slug=self.test_index.slug)

        file_handle = index_filesystem.open(
            '/{}/{}'.format(TEST_NODE_EXPRESSION, self.test_document.label),
            'rb'
        )

        self.assertEqual(
            hashlib.sha256(
                index_filesystem.read(
                    fh=file_handle, offset=0, path=None,
                    size=self.test_document.size
                )
            ).hexdigest(),
            self.test_document.checksum
        )

    def test_multiline_indexes(self):
        self._create_test_index()

        self.test_index.node_templates.create(
            parent=self.test_index.template_root,
            expression=TEST_NODE_EXPRESSION_MULTILINE,
            link_documents=True
        )

        self.upload_document()
        index_filesystem = IndexFilesystem(index_slug=self.test_index.slug)

        self.assertEqual(
            list(index_filesystem.readdir('/', ''))[2:],
            [TEST_NODE_EXPRESSION_MULTILINE_EXPECTED]
        )

    def test_multiline_indexes_first_and_last(self):
        self._create_test_index()

        self.test_index.node_templates.create(
            parent=self.test_index.template_root,
            expression=TEST_NODE_EXPRESSION_MULTILINE_2,
            link_documents=True
        )

        self.upload_document()
        index_filesystem = IndexFilesystem(index_slug=self.test_index.slug)

        self.assertEqual(
            list(index_filesystem.readdir('/', ''))[2:],
            [TEST_NODE_EXPRESSION_MULTILINE_2_EXPECTED]
        )

    def test_duplicated_indexes(self):
        self._create_test_index()

        self.test_index.node_templates.create(
            parent=self.test_index.template_root, expression=TEST_NODE_EXPRESSION,
            link_documents=True
        )
        self.test_index.node_templates.create(
            parent=self.test_index.template_root, expression=TEST_NODE_EXPRESSION,
            link_documents=True
        )

        self.upload_document()
        index_filesystem = IndexFilesystem(index_slug=self.test_index.slug)

        self.assertEqual(
            list(index_filesystem.readdir('/', ''))[2:], []
        )

    def test_ignore_stub_documents(self):
        self._create_test_index()

        self.test_index.node_templates.create(
            parent=self.test_index.template_root, expression=TEST_NODE_EXPRESSION,
            link_documents=True
        )

        self.test_document = Document.objects.create(
            document_type=self.test_document_type, label='document_stub'
        )
        index_filesystem = IndexFilesystem(index_slug=self.test_index.slug)
        self.test_index.rebuild()

        self.assertEqual(
            list(
                index_filesystem.readdir('/', ''))[2:], []
        )
