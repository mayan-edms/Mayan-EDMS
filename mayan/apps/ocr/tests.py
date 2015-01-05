from __future__ import absolute_import

from django.conf import settings
from django.core.files.base import File
from django.test import TestCase

from documents.models import Document, DocumentType
from documents.tests import TEST_SMALL_DOCUMENT_PATH, TEST_DOCUMENT_TYPE

from .api import do_document_ocr
from .models import DocumentQueue, QueueDocument


class DocumentSearchTestCase(TestCase):
    def setUp(self):
        self.document_type = DocumentType.objects.create(name=TEST_DOCUMENT_TYPE, ocr=False)

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = Document.objects.new_document(file_object=File(file_object), document_type=self.document_type)[0].document

        # Clear OCR queue
        QueueDocument.objects.all().delete()

    def _test_ocr_language_issue_16(self, language, result):
        """
        Reusable OCR test for a specific language
        """

        # Clear the document's first page content and switch language
        self.document.language = language
        self.document.save()
        first_page = self.document.pages.first()
        first_page.content = ''
        first_page.save()

        # Queue document for OCR
        self.document.submit_for_ocr()

        # Make sure content was extracted
        self.assertTrue(result in self.document.pages.first().content)

    def test_ocr_language_backends(self):
        self._test_ocr_language_issue_16('deu', 'Mayan EDMS')
        self._test_ocr_language_issue_16('eng', 'Mayan EDMS')
        self._test_ocr_language_issue_16('spa', 'Mayan EDMS')
        self._test_ocr_language_issue_16('rus', '')

    def tearDown(self):
        self.document.delete()
        self.document_type.delete()
