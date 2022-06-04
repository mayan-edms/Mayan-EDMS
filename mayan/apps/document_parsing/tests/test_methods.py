from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.documents.tests.literals import TEST_FILE_HYBRID_PDF_CONTENT

from .mixins import DocumentFileContentTestMixin


class DocumentFileContentMethodTestCase(
    DocumentFileContentTestMixin, GenericDocumentTestCase
):
    auto_upload_test_document = False

    def test_document_file_parsed_content(self):
        self._upload_test_document()

        self._create_test_document_file_parsed_content()
        value = ' '.join(self._test_document_file.content())

        self.assertEqual(value, TEST_FILE_HYBRID_PDF_CONTENT)

    def test_document_parsed_content(self):
        self._upload_test_document()
        self._create_test_document_file_parsed_content()
        value = ' '.join(self._test_document.content())

        self.assertEqual(value, TEST_FILE_HYBRID_PDF_CONTENT)

    def test_document_stub_parsed_content(self):
        self._create_test_document_stub()

        value = ' '.join(self._test_document.content())

        self.assertFalse(value)
