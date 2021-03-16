import hashlib
import unittest

from fuse import FuseOSError

from django.db import connection
from django.test import tag

from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.document_indexing.tests.mixins import IndexTemplateTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from ..filesystems import IndexFilesystem

from .literals import (
    TEST_NODE_EXPRESSION, TEST_NODE_EXPRESSION_INVALID,
    TEST_NODE_EXPRESSION_MULTILINE, TEST_NODE_EXPRESSION_MULTILINE_EXPECTED,
    TEST_NODE_EXPRESSION_MULTILINE_2,
    TEST_NODE_EXPRESSION_MULTILINE_2_EXPECTED
)


@tag('mirroring')
@unittest.skipIf(connection.vendor == 'mysql', 'Known to fail due to unsupported feature of database manager.')
class IndexFilesystemTestCase(
    IndexTemplateTestMixin, DocumentTestMixin, BaseTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_index_template(add_test_document_type=True)

    def test_document_access(self):
        self.test_index_template.node_templates.create(
            parent=self.test_index_template.template_root,
            expression=TEST_NODE_EXPRESSION, link_documents=True
        )

        self._upload_test_document()
        index_filesystem = IndexFilesystem(index_slug=self.test_index_template.slug)

        self.assertEqual(
            index_filesystem.access(
                '/{}/{}'.format(
                    TEST_NODE_EXPRESSION, self.test_document.label
                )
            ), None
        )

    def test_trashed_document_access(self):
        self.test_index_template.node_templates.create(
            parent=self.test_index_template.template_root,
            expression=TEST_NODE_EXPRESSION, link_documents=True
        )

        self._upload_test_document()

        self.test_document.delete()

        index_filesystem = IndexFilesystem(index_slug=self.test_index_template.slug)

        with self.assertRaises(expected_exception=FuseOSError):
            self.assertEqual(
                index_filesystem.access(
                    '/{}/{}'.format(
                        TEST_NODE_EXPRESSION, self.test_document.label
                    )
                ), None
            )

    def test_document_access_failure(self):
        self.test_index_template.node_templates.create(
            parent=self.test_index_template.template_root,
            expression=TEST_NODE_EXPRESSION, link_documents=True
        )

        self._upload_test_document()
        index_filesystem = IndexFilesystem(index_slug=self.test_index_template.slug)

        with self.assertRaises(expected_exception=FuseOSError):
            index_filesystem.access(
                '/{}/{}_non_valid'.format(
                    TEST_NODE_EXPRESSION, self.test_document.label
                )
            )

    def test_document_empty(self):
        self.test_index_template.node_templates.create(
            parent=self.test_index_template.template_root,
            expression=TEST_NODE_EXPRESSION, link_documents=True
        )
        index_filesystem = IndexFilesystem(index_slug=self.test_index_template.slug)

        self._upload_test_document()

        # Delete the physical document file without deleting the document
        # database entry.
        document_file = self.test_document.file_latest.file
        document_file.storage.delete(document_file.name)

        self.assertEqual(
            index_filesystem.getattr(
                path='/{}/{}'.format(
                    TEST_NODE_EXPRESSION, self.test_document.label
                )
            )['st_size'], 0
        )

    def test_document_open(self):
        self.test_index_template.node_templates.create(
            parent=self.test_index_template.template_root,
            expression=TEST_NODE_EXPRESSION, link_documents=True
        )

        self._upload_test_document()
        index_filesystem = IndexFilesystem(index_slug=self.test_index_template.slug)

        file_handle = index_filesystem.open(
            path='/{}/{}'.format(TEST_NODE_EXPRESSION, self.test_document.label),
            flags='rb'
        )

        self.assertEqual(
            hashlib.sha256(
                index_filesystem.read(
                    fh=file_handle, offset=0, path=None,
                    size=self.test_document.file_latest.size
                )
            ).hexdigest(),
            self.test_document.file_latest.checksum
        )

    def test_multiline_indexes(self):
        self.test_index_template.node_templates.create(
            parent=self.test_index_template.template_root,
            expression=TEST_NODE_EXPRESSION_MULTILINE,
            link_documents=True
        )

        self._upload_test_document()
        index_filesystem = IndexFilesystem(index_slug=self.test_index_template.slug)

        self.assertEqual(
            list(index_filesystem.readdir('/', ''))[2:],
            [TEST_NODE_EXPRESSION_MULTILINE_EXPECTED]
        )

    def test_multiline_indexes_first_and_last(self):
        self.test_index_template.node_templates.create(
            parent=self.test_index_template.template_root,
            expression=TEST_NODE_EXPRESSION_MULTILINE_2,
            link_documents=True
        )

        self._upload_test_document()
        index_filesystem = IndexFilesystem(index_slug=self.test_index_template.slug)

        self.assertEqual(
            list(index_filesystem.readdir('/', ''))[2:],
            [TEST_NODE_EXPRESSION_MULTILINE_2_EXPECTED]
        )

    def test_duplicated_indexes(self):
        self.test_index_template.node_templates.create(
            parent=self.test_index_template.template_root,
            expression=TEST_NODE_EXPRESSION, link_documents=True
        )
        self.test_index_template.node_templates.create(
            parent=self.test_index_template.template_root,
            expression=TEST_NODE_EXPRESSION, link_documents=True
        )

        self._upload_test_document()
        index_filesystem = IndexFilesystem(index_slug=self.test_index_template.slug)

        self.assertTrue(
            'level_1({})'.format(self.test_index_template.instance_root.get_children().first().pk) in
            list(index_filesystem.readdir('/', ''))
        )

        self.assertTrue(
            'level_1({})'.format(self.test_index_template.instance_root.get_children().last().pk) in
            list(index_filesystem.readdir('/', ''))
        )

        self.assertEqual(len(list(index_filesystem.readdir('/', ''))), 4)

    def test_stub_documents(self):
        self.test_index_template.node_templates.create(
            parent=self.test_index_template.template_root,
            expression=TEST_NODE_EXPRESSION, link_documents=True
        )

        self._create_test_document_stub()
        index_filesystem = IndexFilesystem(index_slug=self.test_index_template.slug)
        self.test_index_template.rebuild()

        self.assertEqual(
            list(
                index_filesystem.readdir('/', '')
            )[2:], [TEST_NODE_EXPRESSION]
        )

    def test_duplicated_documents_readdir(self):
        self.test_index_template.node_templates.create(
            parent=self.test_index_template.template_root,
            expression=TEST_NODE_EXPRESSION, link_documents=True
        )

        self._upload_test_document()
        self._upload_test_document()

        index_filesystem = IndexFilesystem(index_slug=self.test_index_template.slug)

        self.test_index_template.rebuild()

        self.assertTrue(
            'title_page.png({})'.format(self.test_documents[0].pk) in list(
                index_filesystem.readdir('/level_1', '')
            )
        )
        self.assertTrue(
            'title_page.png({})'.format(self.test_documents[1].pk) in list(
                index_filesystem.readdir('/level_1', '')
            )
        )

    def test_duplicated_documents_open(self):
        self.test_index_template.node_templates.create(
            parent=self.test_index_template.template_root,
            expression=TEST_NODE_EXPRESSION, link_documents=True
        )

        self._upload_test_document()
        self._upload_test_document()

        index_filesystem = IndexFilesystem(index_slug=self.test_index_template.slug)

        self.test_index_template.rebuild()

        test_document_1_path = '/level_1/title_page.png({})'.format(
            self.test_documents[0].pk
        )
        test_document_2_path = '/level_1/title_page.png({})'.format(
            self.test_documents[1].pk
        )

        file_handle = index_filesystem.open(
            path=test_document_1_path, flags=None
        )

        self.assertEqual(
            index_filesystem.read(
                path=None, size=-1, offset=0, fh=file_handle
            ), self.test_documents[0].file_latest.open().read()
        )

        index_filesystem.release(path=None, fh=file_handle)

        file_handle = index_filesystem.open(
            path=test_document_2_path, flags=None
        )

        self.assertEqual(
            index_filesystem.read(
                path=None, size=-1, offset=0, fh=file_handle
            ), self.test_documents[1].file_latest.open().read()
        )

        index_filesystem.release(path=None, fh=file_handle)

    def test_invalid_document_label_character_open(self):
        self.test_index_template.node_templates.create(
            parent=self.test_index_template.template_root,
            expression=TEST_NODE_EXPRESSION, link_documents=True
        )

        self._upload_test_document()

        index_filesystem = IndexFilesystem(index_slug=self.test_index_template.slug)

        self.test_document.label = 'Document of 2019/12'
        self.test_document.save()

        self.test_index_template.rebuild()

        test_document_path = '/level_1/Document of 2019_12'

        file_handle = index_filesystem.open(
            path=test_document_path, flags=None
        )

        self.assertEqual(
            index_filesystem.read(
                path=None, size=-1, offset=0, fh=file_handle
            ), self.test_document.file_latest.open().read()
        )

        index_filesystem.release(path=None, fh=file_handle)

    def test_invalid_document_label_character_readdir(self):
        self.test_index_template.node_templates.create(
            parent=self.test_index_template.template_root,
            expression=TEST_NODE_EXPRESSION, link_documents=True
        )

        self._upload_test_document()

        index_filesystem = IndexFilesystem(index_slug=self.test_index_template.slug)

        self.test_document.label = 'Document of 2019/12'
        self.test_document.save()

        self.test_index_template.rebuild()

        self.assertEqual(
            list(
                index_filesystem.readdir('/level_1', '')
            )[2], 'Document of 2019_12'
        )

    def test_invalid_directory_name_character_open(self):
        self.test_index_template.node_templates.create(
            parent=self.test_index_template.template_root,
            expression=TEST_NODE_EXPRESSION_INVALID, link_documents=True
        )

        self._upload_test_document()

        index_filesystem = IndexFilesystem(index_slug=self.test_index_template.slug)

        self.test_index_template.rebuild()

        test_document_path = '/level_1/{}'.format(self.test_document.label)

        file_handle = index_filesystem.open(
            path=test_document_path, flags=None
        )

        self.assertEqual(
            index_filesystem.read(
                path=None, size=-1, offset=0, fh=file_handle
            ), self.test_document.file_latest.open().read()
        )

        index_filesystem.release(path=None, fh=file_handle)

    def test_invalid_directory_name_character_readdir(self):
        self.test_index_template.node_templates.create(
            parent=self.test_index_template.template_root,
            expression=TEST_NODE_EXPRESSION_INVALID, link_documents=True
        )

        self._upload_test_document()

        index_filesystem = IndexFilesystem(index_slug=self.test_index_template.slug)

        self.test_index_template.rebuild()

        self.assertEqual(
            list(
                index_filesystem.readdir('/', '')
            )[2], 'level_1'
        )

        self.assertEqual(
            list(
                index_filesystem.readdir('/level_1', '')
            )[2], self.test_document.label
        )
