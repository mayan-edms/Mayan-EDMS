from __future__ import unicode_literals

from django.test import override_settings

from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.documents.tests.literals import TEST_HYBRID_DOCUMENT

from .literals import TEST_DOCUMENT_CONTENT


class DocumentAutoParsingTestCase(GenericDocumentTestCase):
    test_document_filename = TEST_HYBRID_DOCUMENT
    auto_create_document_type = False

    def test_disable_auto_parsing(self):
        self._create_document_type()
        self.upload_document()
        with self.assertRaises(StopIteration):
            next(self.test_document.latest_version.content())

    @override_settings(DOCUMENT_PARSING_AUTO_PARSING=True)
    def test_enabled_auto_parsing(self):
        self._create_document_type()
        self.upload_document()
        self.assertTrue(
            TEST_DOCUMENT_CONTENT in next(self.test_document.content())
        )
