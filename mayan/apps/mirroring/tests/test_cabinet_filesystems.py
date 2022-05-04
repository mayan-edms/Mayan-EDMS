import hashlib
import unittest

from fuse import FuseOSError

from django.db import connection
from django.test import tag

from mayan.apps.cabinets.tests.mixins import CabinetTestMixin
from mayan.apps.documents.tests.base import GenericDocumentTestCase

from ..filesystems import MirrorFilesystem
from ..runtime import cache

from .literals import (
    TEST_CABINET_LABEL, TEST_CABINET_LABEL_INVALID,
    TEST_CABINET_LABEL_MULTILINE, TEST_CABINET_LABEL_MULTILINE_EXPECTED,
    TEST_CABINET_LABEL_MULTILINE_2, TEST_CABINET_LABEL_MULTILINE_2_EXPECTED
)


@tag('mirroring')
@unittest.skipIf(connection.vendor == 'mysql', 'Known to fail due to unsupported feature of database manager.')
class CabinetMirroringTestCase(
    CabinetTestMixin, GenericDocumentTestCase
):
    auto_create_test_cabinet = False
    auto_upload_test_document = False

    def tearDown(self):
        cache.clear_all()
        super().tearDown()

    def _get_test_filesystem(self):
        def func_document_container_node():
            return self._test_cabinets[0]

        return MirrorFilesystem(
            func_document_container_node=func_document_container_node,
            node_text_attribute='label'
        )

    def test_document_access(self):
        self._create_test_document_stub()
        self._create_test_cabinet(
            add_test_document=True, label=TEST_CABINET_LABEL
        )

        test_filesystem = self._get_test_filesystem()
        self.assertEqual(
            test_filesystem.access(
                '/{}/{}'.format(
                    TEST_CABINET_LABEL, self._test_document.label
                )
            ), None
        )

    def test_trashed_document_access(self):
        self._create_test_document_stub()
        self._create_test_cabinet(
            add_test_document=True, label=TEST_CABINET_LABEL
        )

        self._test_document.delete()

        test_filesystem = self._get_test_filesystem()
        with self.assertRaises(expected_exception=FuseOSError):
            self.assertEqual(
                test_filesystem.access(
                    '/{}/{}'.format(
                        TEST_CABINET_LABEL, self._test_document.label
                    )
                ), None
            )

    def test_document_access_failure(self):
        self._create_test_document_stub()
        self._create_test_cabinet(
            add_test_document=True, label=TEST_CABINET_LABEL
        )

        test_filesystem = self._get_test_filesystem()
        with self.assertRaises(expected_exception=FuseOSError):
            test_filesystem.access(
                '/{}/{}_non_valid'.format(
                    TEST_CABINET_LABEL, self._test_document.label
                )
            )

    def test_document_empty(self):
        self._create_test_cabinet(label=TEST_CABINET_LABEL)
        test_filesystem = self._get_test_filesystem()

        self._upload_test_document()
        self._test_cabinet.documents.add(self._test_document)

        # Delete the physical document file without deleting the document
        # database entry.
        document_file = self._test_document.file_latest
        document_file.file.storage.delete(document_file.file.name)

        # Document file disk size is immutable since
        # 8733e07974c9ecce4880fb1fa19a14f6416c5fe6
        # 2022-04-30.
        self.assertEqual(
            test_filesystem.getattr(
                path='/{}/{}'.format(
                    TEST_CABINET_LABEL, self._test_document.label
                )
            )['st_size'], document_file.size
        )

    def test_document_open(self):
        self._upload_test_document()
        self._create_test_cabinet(
            add_test_document=True, label=TEST_CABINET_LABEL
        )

        test_filesystem = self._get_test_filesystem()

        file_handle = test_filesystem.open(
            path='/{}/{}'.format(
                TEST_CABINET_LABEL, self._test_document.label
            ), flags='rb'
        )

        self.assertEqual(
            hashlib.sha256(
                test_filesystem.read(
                    fh=file_handle, offset=0, path=None,
                    size=self._test_document.file_latest.size
                )
            ).hexdigest(),
            self._test_document.file_latest.checksum
        )

    def test_multiline_indexes(self):
        self._create_test_cabinet()
        self._create_test_cabinet_child(
            label=TEST_CABINET_LABEL_MULTILINE
        )

        test_filesystem = self._get_test_filesystem()
        self.assertEqual(
            list(test_filesystem.readdir('/', ''))[2:],
            [TEST_CABINET_LABEL_MULTILINE_EXPECTED]
        )

    def test_multiline_indexes_first_and_last(self):
        self._create_test_cabinet()
        self._create_test_cabinet_child(
            label=TEST_CABINET_LABEL_MULTILINE_2
        )

        test_filesystem = self._get_test_filesystem()
        self.assertEqual(
            list(test_filesystem.readdir('/', ''))[2:],
            [TEST_CABINET_LABEL_MULTILINE_2_EXPECTED]
        )

    def test_stub_documents(self):
        self._create_test_cabinet()
        self._create_test_cabinet_child(label=TEST_CABINET_LABEL)

        test_filesystem = self._get_test_filesystem()
        self.assertEqual(
            list(
                test_filesystem.readdir('/', '')
            )[2:], [TEST_CABINET_LABEL]
        )

    def test_duplicated_documents_readdir(self):
        self._create_test_cabinet(label=TEST_CABINET_LABEL)
        self._create_test_document_stub()
        self._create_test_document_stub(label=self._test_document.label)
        self._test_cabinet.documents.add(self._test_documents[0])
        self._test_cabinet.documents.add(self._test_documents[1])

        test_filesystem = self._get_test_filesystem()
        self.assertTrue(
            '{}({})'.format(
                self._test_documents[0].label, self._test_documents[0].pk
            ) in list(
                test_filesystem.readdir('/level_1', '')
            )
        )
        self.assertTrue(
            '{}({})'.format(
                self._test_documents[0].label, self._test_documents[1].pk
            ) in list(
                test_filesystem.readdir('/level_1', '')
            )
        )

    def test_duplicated_documents_open(self):
        self._create_test_cabinet(label=TEST_CABINET_LABEL)
        self._upload_test_document()
        self._upload_test_document()
        self._test_cabinet.documents.add(self._test_documents[0])
        self._test_cabinet.documents.add(self._test_documents[1])

        test_filesystem = self._get_test_filesystem()

        test_document_1_path = '/level_1/{}({})'.format(
            self._test_documents[0].label, self._test_documents[0].pk
        )
        test_document_2_path = '/level_1/{}({})'.format(
            self._test_documents[1].label, self._test_documents[1].pk
        )

        file_handle = test_filesystem.open(
            path=test_document_1_path, flags=None
        )

        self.assertEqual(
            test_filesystem.read(
                path=None, size=-1, offset=0, fh=file_handle
            ), self._test_documents[0].file_latest.open().read()
        )

        test_filesystem.release(path=None, fh=file_handle)

        file_handle = test_filesystem.open(
            path=test_document_2_path, flags=None
        )

        self.assertEqual(
            test_filesystem.read(
                path=None, size=-1, offset=0, fh=file_handle
            ), self._test_documents[1].file_latest.open().read()
        )

        test_filesystem.release(path=None, fh=file_handle)

    def test_invalid_document_label_character_open(self):
        self._upload_test_document()
        self._create_test_cabinet(
            add_test_document=True, label=TEST_CABINET_LABEL
        )

        test_filesystem = self._get_test_filesystem()

        self._test_document.label = 'Document of 2019/12'
        self._test_document.save()

        test_document_path = '/level_1/Document of 2019_12'

        file_handle = test_filesystem.open(
            path=test_document_path, flags=None
        )
        self.assertEqual(
            test_filesystem.read(
                path=None, size=-1, offset=0, fh=file_handle
            ), self._test_document.file_latest.open().read()
        )

        test_filesystem.release(path=None, fh=file_handle)

    def test_invalid_document_label_character_readdir(self):
        self._create_test_cabinet(label=TEST_CABINET_LABEL)
        self._create_test_document_stub()
        self._test_cabinet.documents.add(self._test_document)

        test_filesystem = self._get_test_filesystem()

        self._test_document.label = 'Document of 2019/12'
        self._test_document.save()

        self.assertEqual(
            list(
                test_filesystem.readdir('/level_1', '')
            )[2], 'Document of 2019_12'
        )

    def test_invalid_directory_name_character_open(self):
        self._create_test_cabinet(
            label=TEST_CABINET_LABEL_INVALID
        )
        self._upload_test_document()
        self._test_cabinet.documents.add(self._test_document)

        test_filesystem = self._get_test_filesystem()

        test_document_path = '/level_1/{}'.format(self._test_document.label)

        file_handle = test_filesystem.open(
            path=test_document_path, flags=None
        )

        self.assertEqual(
            test_filesystem.read(
                path=None, size=-1, offset=0, fh=file_handle
            ), self._test_document.file_latest.open().read()
        )

        test_filesystem.release(path=None, fh=file_handle)

    def test_invalid_directory_name_character_readdir(self):
        self._create_test_cabinet()
        self._create_test_cabinet_child(
            label=TEST_CABINET_LABEL_INVALID
        )
        self._create_test_document_stub()
        self._test_cabinet_child.documents.add(self._test_document)

        test_filesystem = self._get_test_filesystem()
        self.assertEqual(
            list(
                test_filesystem.readdir('/', '')
            )[2], 'level_1'
        )

        self.assertEqual(
            list(
                test_filesystem.readdir('/level_1', '')
            )[2], self._test_document.label
        )
