from mayan.apps.tests.tests.base import BaseTestCase
from mayan.apps.documents.tests.literals import TEST_HYBRID_DOCUMENT
from mayan.apps.documents.tests.mixins import DocumentTestMixin

from ..parsers import PopplerParser

from .literals import TEST_DOCUMENT_CONTENT


class ParserTestCase(DocumentTestMixin, BaseTestCase):
    test_document_filename = TEST_HYBRID_DOCUMENT

    def test_poppler_parser(self):
        parser = PopplerParser()

        parser.process_document_version(self.test_document.latest_version)

        self.assertTrue(
            TEST_DOCUMENT_CONTENT in self.test_document.pages.first().content.content
        )
