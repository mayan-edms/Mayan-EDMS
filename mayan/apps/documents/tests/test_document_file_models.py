import time

from .base import GenericDocumentTestCase
from .literals import TEST_SMALL_DOCUMENT_CHECKSUM, TEST_SMALL_DOCUMENT_PATH


class DocumentFileTestCase(GenericDocumentTestCase):
    def test_file_create(self):
        self.assertEqual(self.test_document.files.count(), 1)

        self._upload_test_document_file()
        #with open(file=TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
        #    self.test_document.new_file(
        #        file_object=file_object
        #    )

        self.assertEqual(self.test_document.files.count(), 2)

        self.assertEqual(
            self.test_document.checksum,
            TEST_SMALL_DOCUMENT_CHECKSUM
        )

    def test_file_delete(self):
        self.assertEqual(self.test_document.files.count(), 1)

        ## Needed by MySQL as milliseconds value is not store in timestamp
        ## field
        ##time.sleep(1.01)

        self._upload_test_document_file()
        #with open(file=TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
        #    self.test_document.new_file(
        #        file_object=file_object
        #    )

        self.assertEqual(self.test_document.files.count(), 2)

        self.test_document.files.last().delete()

        self.assertEqual(self.test_document.files.count(), 1)

    def test_method_get_absolute_url(self):
        self.assertTrue(self.test_document.latest_file.get_absolute_url())
