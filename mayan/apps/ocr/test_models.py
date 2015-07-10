from __future__ import unicode_literals

from django.core.files.base import File
from django.test import TransactionTestCase

from documents.models import DocumentType
from documents.test_models import TEST_SMALL_DOCUMENT_PATH, TEST_DOCUMENT_TYPE


class DocumentOCRTestCase(TransactionTestCase):
    def setUp(self):
        self.document_type = DocumentType.objects.create(label=TEST_DOCUMENT_TYPE)

        ocr_settings = self.document_type.ocr_settings
        ocr_settings.auto_ocr = False
        ocr_settings.save()

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(file_object=File(file_object))

    def tearDown(self):
        self.document.delete()
        self.document_type.delete()

    def test_ocr_language_backends_end(self):
        self.document.submit_for_ocr()
        self.assertTrue('Mayan EDMS Documentation' in self.document.pages.first().ocr_content.content)
