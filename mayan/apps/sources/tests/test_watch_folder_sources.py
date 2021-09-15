from pathlib import Path
import shutil

from mayan.apps.documents.models import Document
from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.documents.tests.literals import (
    TEST_NON_ASCII_DOCUMENT_FILENAME,
    TEST_NON_ASCII_COMPRESSED_DOCUMENT_PATH, TEST_SMALL_DOCUMENT_CHECKSUM,
    TEST_SMALL_DOCUMENT_PATH
)

from ..source_backends.literals import SOURCE_UNCOMPRESS_CHOICE_ALWAYS

from .literals import TEST_WATCHFOLDER_SUBFOLDER
from .mixins.watch_folder_source_mixins import WatchFolderSourceTestMixin


class WatchFolderSourceBackendTestCase(
    WatchFolderSourceTestMixin, GenericDocumentTestCase
):
    auto_create_test_source = False
    auto_upload_test_document = False

    def test_upload_simple_file(self):
        self._create_test_watch_folder()

        document_count = Document.objects.count()

        temporary_directory = self.test_source.get_backend_data()['folder_path']

        shutil.copy(src=TEST_SMALL_DOCUMENT_PATH, dst=temporary_directory)

        self.test_source.get_backend_instance().process_documents()

        self.assertEqual(Document.objects.count(), document_count + 1)
        self.assertEqual(
            Document.objects.first().file_latest.checksum,
            TEST_SMALL_DOCUMENT_CHECKSUM
        )

    def test_subfolder_disabled(self):
        self._create_test_watch_folder()

        temporary_directory = self.test_source.get_backend_data()['folder_path']

        test_path = Path(temporary_directory)
        test_subfolder = test_path.joinpath(TEST_WATCHFOLDER_SUBFOLDER)
        test_subfolder.mkdir()

        shutil.copy(
            src=TEST_SMALL_DOCUMENT_PATH, dst=test_subfolder
        )

        document_count = Document.objects.count()

        self.test_source.get_backend_instance().process_documents()
        self.assertEqual(Document.objects.count(), document_count)

    def test_subfolder_enabled(self):
        self._create_test_watch_folder(
            extra_data={'include_subdirectories': True}
        )

        temporary_directory = self.test_source.get_backend_data()['folder_path']

        test_path = Path(temporary_directory)
        test_subfolder = test_path.joinpath(TEST_WATCHFOLDER_SUBFOLDER)
        test_subfolder.mkdir()

        shutil.copy(src=TEST_SMALL_DOCUMENT_PATH, dst=test_subfolder)

        document_count = Document.objects.count()

        self.test_source.get_backend_instance().process_documents()

        self.assertEqual(Document.objects.count(), document_count + 1)

        document = Document.objects.first()

        self.assertEqual(
            document.file_latest.checksum, TEST_SMALL_DOCUMENT_CHECKSUM
        )

    def test_non_ascii_file_in_non_ascii_compressed_file(self):
        """
        Test Non-ASCII named documents inside Non-ASCII named compressed
        file. GitHub issue #163.
        """
        self._create_test_watch_folder(
            extra_data={'uncompress': SOURCE_UNCOMPRESS_CHOICE_ALWAYS}
        )

        temporary_directory = self.test_source.get_backend_data()['folder_path']

        shutil.copy(
            src=TEST_NON_ASCII_COMPRESSED_DOCUMENT_PATH,
            dst=temporary_directory
        )

        document_count = Document.objects.count()

        self.test_source.get_backend_instance().process_documents()

        self.assertEqual(Document.objects.count(), document_count + 1)

        document = Document.objects.first()

        self.assertEqual(document.label, TEST_NON_ASCII_DOCUMENT_FILENAME)
        self.assertEqual(document.file_latest.exists(), True)
        self.assertEqual(document.file_latest.size, 17436)
        self.assertEqual(document.file_latest.mimetype, 'image/png')
        self.assertEqual(document.file_latest.encoding, 'binary')
