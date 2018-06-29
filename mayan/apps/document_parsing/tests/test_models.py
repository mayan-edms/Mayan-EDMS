from __future__ import unicode_literals

from django.test import override_settings

from documents.tests import GenericDocumentTestCase, TEST_DOCUMENT_PATH


class DocumentAutoParsingTestCase(GenericDocumentTestCase):
    test_document_filename = TEST_DOCUMENT_PATH
    auto_create_document_type = False

    @override_settings(DOCUMENT_PARSING_AUTO_PARSING=False)
    def test_disable_auto_parsing(self):
        self.create_document_type()
        self.document = self.upload_document()
        with self.assertRaises(StopIteration):
            self.document.latest_version.content().next()

    @override_settings(DOCUMENT_PARSING_AUTO_PARSING=True)
    def test_enabled_auto_parsing(self):
        self.create_document_type()
        self.document = self.upload_document()
        self.assertTrue('Mayan' in self.document.content().next())
