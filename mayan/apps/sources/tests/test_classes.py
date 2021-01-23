import os
import shutil

from mayan.apps.documents.tests.literals import TEST_NON_ASCII_DOCUMENT_PATH
from mayan.apps.storage.utils import mkdtemp
from mayan.apps.testing.tests.base import BaseTestCase

from ..classes import StagingFile

from .mocks import MockStagingFolder


class StagingFileTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.temporary_directory = mkdtemp()
        shutil.copy(
            src=TEST_NON_ASCII_DOCUMENT_PATH, dst=self.temporary_directory
        )
        self.test_filename = os.path.basename(TEST_NON_ASCII_DOCUMENT_PATH)
        self.test_staging_folder = MockStagingFolder()
        self.test_staging_folder.folder_path = self.temporary_directory
        self.test_staging_files = []

    def tearDown(self):
        for test_staging_file in self.test_staging_files:
            try:
                test_staging_file.delete()
            except FileNotFoundError:
                """Ignore file not found errors"""

        shutil.rmtree(path=self.temporary_directory)
        super().tearDown()

    def test_unicode_staging_file(self):
        self.test_staging_files.append(
            StagingFile(
                staging_folder=self.test_staging_folder,
                filename=self.test_filename
            )
        )

        self.test_staging_files.append(
            StagingFile(
                staging_folder=self.test_staging_folder,
                encoded_filename=self.test_staging_files[0].encoded_filename
            )
        )

        self.assertEqual(
            self.test_staging_files[1].filename, self.test_filename
        )

    def test_staging_file_generate_image_method(self):
        self.test_staging_files.append(
            StagingFile(
                staging_folder=self.test_staging_folder,
                filename=self.test_filename
            )
        )

        self.assertNotEqual(self.test_staging_files[0].generate_image(), '')
