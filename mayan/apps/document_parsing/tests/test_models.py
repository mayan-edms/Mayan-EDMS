from __future__ import unicode_literals

from django.test import override_settings

from documents.tests import GenericDocumentTestCase, TEST_HYBRID_DOCUMENT

TEST_DOCUMENT_CONTENT = 'Sample text'


class DocumentAutoParsingTestCase(GenericDocumentTestCase):
    test_document_filename = TEST_HYBRID_DOCUMENT
    auto_create_document_type = False

    @override_settings(DOCUMENT_PARSING_AUTO_PARSING=False)
    def test_disable_auto_parsing(self):
        self._create_document_type()
        self.document = self.upload_document()
        with self.assertRaises(StopIteration):
            next(self.document.latest_version.content())

    @override_settings(DOCUMENT_PARSING_AUTO_PARSING=True)
    def test_enabled_auto_parsing(self):
        self._create_document_type()
        self.document = self.upload_document()
        self.assertTrue(
            TEST_DOCUMENT_CONTENT in next(self.document.content())
        )
