from django.test import override_settings

from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.documents.tests.literals import TEST_DEU_DOCUMENT_PATH

from .literals import (
    TEST_DOCUMENT_VERSION_OCR_CONTENT, TEST_DOCUMENT_VERSION_OCR_CONTENT_DEU_1,
    TEST_DOCUMENT_VERSION_OCR_CONTENT_DEU_2
)


@override_settings(OCR_AUTO_OCR=True)
class DocumentOCRTestCase(GenericDocumentTestCase):
    def test_ocr_language_backends_eng(self):
        content = self.test_document_version.pages.first().ocr_content.content
        self.assertTrue(TEST_DOCUMENT_VERSION_OCR_CONTENT in content)


@override_settings(OCR_AUTO_OCR=True)
class GermanOCRSupportTestCase(GenericDocumentTestCase):
    test_document_language = 'deu'
    test_document_path = TEST_DEU_DOCUMENT_PATH

    def test_ocr_language_backends_end(self):
        content = self.test_document.version_active.pages.first().ocr_content.content

        self.assertTrue(
            TEST_DOCUMENT_VERSION_OCR_CONTENT_DEU_1 in content
        )
        self.assertTrue(
            TEST_DOCUMENT_VERSION_OCR_CONTENT_DEU_2 in content
        )
