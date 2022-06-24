from mayan.apps.documents.tests.base import GenericDocumentTestCase

from .literals import TEST_DOCUMENT_CONTENT
from .mixins import DocumentFileContentTestMixin


class DocumentFileContentMethodTestCase(
    DocumentFileContentTestMixin, GenericDocumentTestCase
):
    auto_upload_test_document = False

    def test_document_file_parsed_content(self):
        self._upload_test_document()

        self._create_test_document_file_parsed_content()
        value = ' '.join(self.test_document_file.content())

        self.assertEqual(value, TEST_DOCUMENT_CONTENT)

    def test_document_parsed_content(self):
        self._upload_test_document()
        self._create_test_document_file_parsed_content()
        value = ' '.join(self.test_document.content())

        self.assertEqual(value, TEST_DOCUMENT_CONTENT)

    def test_document_stub_parsed_content(self):
        self._create_test_document_stub()

        value = ' '.join(self.test_document.content())

        self.assertFalse(value)
