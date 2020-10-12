from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.documents.tests.literals import TEST_PDF_DOCUMENT_FILENAME

from .literals import (
    TEST_PDF_FILE_METADATA_DOTTED_NAME, TEST_PDF_FILE_METADATA_VALUE
)


class EXIFToolDriverTestCase(GenericDocumentTestCase):
    test_document_filename = TEST_PDF_DOCUMENT_FILENAME

    def test_driver_entries(self):
        self.test_document.submit_for_file_metadata_processing()
        value = self.test_document.get_file_metadata(
            dotted_name=TEST_PDF_FILE_METADATA_DOTTED_NAME
        )
        self.assertEqual(value, TEST_PDF_FILE_METADATA_VALUE)
