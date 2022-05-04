from django.test import override_settings

from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.documents.tests.literals import (
    TEST_FILE_HYBRID_PDF_CONTENT, TEST_FILE_HYBRID_PDF_FILENAME
)


class DocumentAutoParsingTestCase(GenericDocumentTestCase):
    _test_document_filename = TEST_FILE_HYBRID_PDF_FILENAME
    auto_create_test_document_type = False

    def test_disable_auto_parsing(self):
        self._create_test_document_type()
        self._upload_test_document()
        with self.assertRaises(expected_exception=StopIteration):
            next(self._test_document_file.content())

    @override_settings(DOCUMENT_PARSING_AUTO_PARSING=True)
    def test_enabled_auto_parsing(self):
        self._create_test_document_type()
        self._upload_test_document()
        self.assertTrue(
            TEST_FILE_HYBRID_PDF_CONTENT in next(
                self._test_document_file.content()
            )
        )
