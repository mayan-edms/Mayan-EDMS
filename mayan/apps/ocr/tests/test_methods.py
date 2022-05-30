from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.documents.tests.mixins.document_version_mixins import DocumentVersionTestMixin

from .literals import TEST_DOCUMENT_VERSION_OCR_CONTENT
from .mixins import DocumentVersionOCRTestMixin


class DocumentOCRContentMethodTestCase(
    DocumentVersionOCRTestMixin, DocumentVersionTestMixin,
    GenericDocumentTestCase
):
    auto_create_test_document_stub = True
    auto_create_test_document_version = True
    auto_upload_test_document = False

    def test_document_ocr_content(self):
        self._create_test_document_version_ocr_content()
        value = ' '.join(self._test_document.ocr_content())

        self.assertEqual(value, TEST_DOCUMENT_VERSION_OCR_CONTENT)

    def test_document_ocr_content_empty(self):
        value = ' '.join(self._test_document.ocr_content())

        self.assertFalse(value)

    def test_document_version_ocr_content(self):
        self._create_test_document_version_ocr_content()
        value = ' '.join(self._test_document_version.ocr_content())

        self.assertEqual(value, TEST_DOCUMENT_VERSION_OCR_CONTENT)

    def test_document_version_ocr_content_empty(self):
        value = ' '.join(self._test_document_version.ocr_content())

        self.assertFalse(value)
