from pathlib import Path

from django.core.files.base import ContentFile
from django.utils.encoding import force_bytes

from mayan.apps.common.tests.base import BaseTestCase
from mayan.apps.storage.utils import fs_cleanup, mkdtemp
from mayan.apps.mimetype.api import get_mimetype

from ..backends.compressedstorage import ZipCompressedPassthroughStorage
from ..backends.encryptedstorage import EncryptedPassthroughStorage

from .literals import TEST_CONTENT, TEST_FILE_NAME


class EncryptedPassthroughStorageTestCase(BaseTestCase):
    def setUp(self):
        super(EncryptedPassthroughStorageTestCase, self).setUp()
        self.temporary_directory = mkdtemp()

    def tearDown(self):
        fs_cleanup(filename=self.temporary_directory)
        super(EncryptedPassthroughStorageTestCase, self).tearDown()

    def test_file_save_and_load(self):
        storage = EncryptedPassthroughStorage(
            password='testpassword',
            next_storage_backend_arguments={
                'location': self.temporary_directory,
            }
        )

        test_file_name = storage.save(
            name=TEST_FILE_NAME, content=ContentFile(
                content=force_bytes(TEST_CONTENT)
            )
        )

        path_file = Path(self.temporary_directory) / test_file_name

        with path_file.open(mode='rb') as file_object:
            self.assertEqual(
                get_mimetype(file_object=file_object),
                ('application/octet-stream', 'binary')
            )

        with storage.open(name=TEST_FILE_NAME, mode='r') as file_object:
            self.assertEqual(file_object.read(), TEST_CONTENT)

        with storage.open(name=TEST_FILE_NAME, mode='r') as file_object:
            self.assertEqual(file_object.read(1), TEST_CONTENT[0:1])

        with storage.open(name=TEST_FILE_NAME, mode='r') as file_object:
            self.assertEqual(file_object.read(999), TEST_CONTENT)


class ZipCompressedPassthroughStorageTestCase(BaseTestCase):
    def setUp(self):
        super(ZipCompressedPassthroughStorageTestCase, self).setUp()
        self.temporary_directory = mkdtemp()

    def tearDown(self):
        fs_cleanup(filename=self.temporary_directory)
        super(ZipCompressedPassthroughStorageTestCase, self).tearDown()

    def test_file_save_and_load(self):
        storage = ZipCompressedPassthroughStorage(
            next_storage_backend_arguments={
                'location': self.temporary_directory
            }
        )

        test_file_name = storage.save(
            name=TEST_FILE_NAME, content=ContentFile(content=TEST_CONTENT)
        )

        path_file = Path(self.temporary_directory) / test_file_name

        with path_file.open(mode='rb') as file_object:
            self.assertEqual(
                get_mimetype(file_object=file_object),
                ('application/zip', 'binary')
            )

        with path_file.open(mode='rb') as file_object:
            self.assertNotEqual(
                file_object.read(), force_bytes(TEST_CONTENT)
            )

        with storage.open(name=TEST_FILE_NAME, mode='r') as file_object:
            self.assertEqual(file_object.read(), TEST_CONTENT)
