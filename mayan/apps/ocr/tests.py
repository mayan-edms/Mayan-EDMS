from __future__ import absolute_import

import os

from django.conf import settings
from django.core.files.base import File
from django.utils import unittest

from documents.models import Document, DocumentType

from .api import do_document_ocr
from .models import DocumentQueue

TEST_DOCUMENT_PATH = os.path.join(settings.BASE_DIR, 'contrib', 'sample_documents', 'title_page.png')


class DocumentSearchTestCase(unittest.TestCase):
    def setUp(self):
        # Start the OCR queue
        self.default_queue = DocumentQueue.objects.get(name='default')

    def test_do_document_ocr(self):
        self.document_type = DocumentType(name='test doc type')
        self.document_type.save()

        self.document = Document(
            document_type=self.document_type,
            description='description',
        )
        self.document.save()

        with open(TEST_DOCUMENT_PATH) as file_object:
            self.document.new_version(file=File(file_object, name='title_page.png'))

        self.failUnlessEqual(self.default_queue.queuedocument_set.count(), 1)

        do_document_ocr(self.default_queue.queuedocument_set.all()[0])

        self.assertTrue(u'Mayan EDMS' in self.document.pages.all()[0].content)

    def tearDown(self):
        self.document.delete()
        self.document_type.delete()
