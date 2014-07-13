from __future__ import absolute_import

import os

from django.conf import settings
from django.core.files.base import File
from django.utils import unittest

from documents.models import Document, DocumentType

from .api import do_document_ocr
from .models import DocumentQueue, QueueDocument

TEST_DOCUMENT_PATH = os.path.join(settings.BASE_DIR, 'contrib', 'sample_documents', 'title_page.png')


class DocumentSearchTestCase(unittest.TestCase):
    def setUp(self):
        # Start the OCR queue
        self.default_queue = DocumentQueue.objects.get(name='default')
        self.document_type = DocumentType.objects.create(name='test doc type')
        self.document = Document(
            document_type=self.document_type,
            description='description',
        )
        self.document.save()

        with open(TEST_DOCUMENT_PATH) as file_object:
            self.document.new_version(file=File(file_object, name='title_page.png'))

        # Clear OCR queue
        QueueDocument.objects.all().delete()

    def reload_ocr_runtime(self, language):
        """
        Forces the reloading of the language_backend for different languages
        """

        from ocr.conf import settings
        from ocr import runtime

        setattr(settings, 'LANGUAGE', language)

        reload(runtime)
        from .runtime import language_backend
        self.assertEqual(unicode(language_backend.__class__), u"<class 'ocr.lang.{0}.LanguageBackend'>".format(language))

    def _test_ocr_language_issue_16(self, language):
        """
        Reusable OCR test for a specific language
        """

        self.reload_ocr_runtime(language)

        # Clear the document's first page content
        first_page = self.document.pages.first()
        first_page.content = ''
        first_page.save()

        # Make sure no documents are queued for OCR
        self.failUnlessEqual(self.default_queue.queuedocument_set.count(), 0)
        DocumentQueue.objects.queue_document(self.document)
        # Make sure our document is queued for OCR
        self.failUnlessEqual(self.default_queue.queuedocument_set.count(), 1)

        do_document_ocr(self.default_queue.queuedocument_set.first())

        # Make sure content was extracted
        self.assertTrue(u'Mayan EDMS' in self.document.pages.first().content)

    def test_ocr_language_german(self):
        self._test_ocr_language_issue_16('deu')

    def test_ocr_language_english(self):
        self._test_ocr_language_issue_16('eng')

    def test_ocr_language_russian(self):
        self._test_ocr_language_issue_16('rus')

    def test_ocr_language_spanish(self):
        self._test_ocr_language_issue_16('spa')

    def tearDown(self):
        self.document.delete()
        self.document_type.delete()
