from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.documents.tests.literals import (
    TEST_FILE_HYBRID_PDF_CONTENT, TEST_FILE_HYBRID_PDF_PATH,
    TEST_FILE_OFFICE_CONTENT, TEST_FILE_OFFICE_PATH,
    TEST_FILE_TEXT_CONTENT, TEST_FILE_TEXT_PATH
)

from ..parsers import OfficePopplerParser, PopplerParser


class ParserTestCase(GenericDocumentTestCase):
    auto_upload_test_document = False

    def test_office_file_parser_with_office_doc_file(self):
        self._test_document_path = TEST_FILE_OFFICE_PATH
        self._upload_test_document()

        parser = OfficePopplerParser()

        parser.process_document_file(self._test_document_file)

        self.assertTrue(
            TEST_FILE_OFFICE_CONTENT in self._test_document_file.pages.first().content.content
        )

    def test_office_file_parser_with_text_file(self):
        self._test_document_path = TEST_FILE_TEXT_PATH
        self._upload_test_document()

        parser = OfficePopplerParser()

        parser.process_document_file(self._test_document_file)

        self.assertTrue(
            TEST_FILE_TEXT_CONTENT in self._test_document_file.pages.first().content.content
        )

    def test_poppler_parser_with_pdf(self):
        self._test_document_path = TEST_FILE_HYBRID_PDF_PATH
        self._upload_test_document()

        parser = PopplerParser()

        parser.process_document_file(self._test_document_file)

        self.assertTrue(
            TEST_FILE_HYBRID_PDF_CONTENT in self._test_document_file.pages.first().content.content
        )
