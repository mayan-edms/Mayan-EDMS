from django.test import override_settings

from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.documents.tests.literals import TEST_DEU_DOCUMENT_PATH

from .literals import (
    TEST_DOCUMENT_VERSION_OCR_CONTENT, TEST_DOCUMENT_VERSION_OCR_CONTENT_DEU_1,
    TEST_DOCUMENT_VERSION_OCR_CONTENT_DEU_2
)


@override_settings(OCR_AUTO_OCR=True)
class DocumentOCRTestCase(GenericDocumentTestCase):
    # PyOCR's leak descriptor in get_available_languages and image_to_string
    # Disable descriptor leak test until fixed in upstream
    _skip_file_descriptor_test = True

    def test_ocr_language_backends_eng(self):
        content = self.test_document_version.pages.first().ocr_content.content
        self.assertTrue(TEST_DOCUMENT_VERSION_OCR_CONTENT in content)


@override_settings(OCR_AUTO_OCR=True)
class GermanOCRSupportTestCase(GenericDocumentTestCase):
    # PyOCR's leak descriptor in get_available_languages and image_to_string
    # Disable descriptor leak test until fixed in upstream
    _skip_file_descriptor_test = True

    auto_upload_test_document = False

    def setUp(self):
        super().setUp()

        with open(file=TEST_DEU_DOCUMENT_PATH, mode='rb') as file_object:
            self.test_document = self.test_document_type.new_document(
                file_object=file_object, language='deu'
            )

    def test_ocr_language_backends_end(self):
        content = self.test_document.latest_version.pages.first().ocr_content.content

        self.assertTrue(
            TEST_DOCUMENT_VERSION_OCR_CONTENT_DEU_1 in content
        )
        self.assertTrue(
            TEST_DOCUMENT_VERSION_OCR_CONTENT_DEU_2 in content
        )
