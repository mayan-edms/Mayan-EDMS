from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.documents.tests.literals import TEST_HYBRID_DOCUMENT

from ..parsers import PopplerParser

from .literals import TEST_DOCUMENT_CONTENT


class ParserTestCase(GenericDocumentTestCase):
    test_document_filename = TEST_HYBRID_DOCUMENT

    def test_poppler_parser(self):
        parser = PopplerParser()

        parser.process_document_file(self.test_document_file)

        self.assertTrue(
            TEST_DOCUMENT_CONTENT in self.test_document_file.pages.first().content.content
        )
