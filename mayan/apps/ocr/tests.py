from __future__ import absolute_import

import os
import time

from django.conf import settings
from django.core.files.base import File
from django.utils import unittest

from documents.models import Document, DocumentType

from .literals import (QUEUEDOCUMENT_STATE_PROCESSING,
    DOCUMENTQUEUE_STATE_STOPPED, DOCUMENTQUEUE_STATE_ACTIVE)
from .models import DocumentQueue
from .api import do_document_ocr


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

        file_object = open(os.path.join(settings.SITE_ROOT, 'contrib', 'sample_documents', 'title_page.png'))
        new_version = self.document.new_version(file=File(file_object, name='title_page.png'))
        file_object.close()

        self.failUnlessEqual(self.default_queue.queuedocument_set.count(), 1)

        do_document_ocr(self.default_queue.queuedocument_set.all()[0])

        self.assertTrue(u'Mayan EDMS' in self.document.pages.all()[0].content)

    def tearDown(self):
        self.document.delete()
        self.document_type.delete()
