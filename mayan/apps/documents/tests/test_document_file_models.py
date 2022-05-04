from pathlib import Path

from .base import GenericDocumentTestCase
from .literals import TEST_DOCUMENT_SMALL_CHECKSUM
from .mixins.document_file_mixins import DocumentFileTestMixin


class DocumentFileTestCase(DocumentFileTestMixin, GenericDocumentTestCase):
    def test_file_create(self):
        document_file_count = self._test_document.files.count()

        self._upload_test_document_file()

        self.assertEqual(
            self._test_document.files.count(), document_file_count + 1
        )
        self.assertEqual(
            self._test_document.file_latest.checksum,
            TEST_DOCUMENT_SMALL_CHECKSUM
        )

    def test_document_file_delete(self):
        document_file_count = self._test_document.files.count()

        self._test_document.files.last().delete()

        self.assertEqual(
            self._test_document.files.count(), document_file_count - 1
        )

    def test_document_file_filename_extraction(self):
        """
        Ensure only the filename is stored and not the entire path of the
        uploaded document file.
        """
        self.assertEqual(
            Path(self._test_document_file.filename).name,
            self._test_document_file.filename
        )

    def test_document_first_file_filename(self):
        """
        Ensure the filename of the first document is the same as the document
        label.
        """
        self.assertEqual(
            self._test_document_file.filename, self._test_document.label
        )

    def test_method_get_absolute_url(self):
        self.assertTrue(self._test_document.file_latest.get_absolute_url())
