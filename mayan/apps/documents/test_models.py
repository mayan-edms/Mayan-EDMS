# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.conf import settings
from django.core.files import File
from django.test import TestCase

from .models import DeletedDocument, Document, DocumentType

TEST_ADMIN_PASSWORD = 'test_admin_password'
TEST_ADMIN_USERNAME = 'test_admin'
TEST_ADMIN_EMAIL = 'admin@admin.com'
TEST_SMALL_DOCUMENT_FILENAME = 'title_page.png'
TEST_NON_ASCII_DOCUMENT_FILENAME = 'I18N_title_áéíóúüñÑ.png'
TEST_NON_ASCII_COMPRESSED_DOCUMENT_FILENAME = 'I18N_title_áéíóúüñÑ.png.zip'
TEST_DOCUMENT_PATH = os.path.join(settings.BASE_DIR, 'contrib', 'sample_documents', 'mayan_11_1.pdf')
TEST_SMALL_DOCUMENT_PATH = os.path.join(settings.BASE_DIR, 'contrib', 'sample_documents', TEST_SMALL_DOCUMENT_FILENAME)
TEST_NON_ASCII_DOCUMENT_PATH = os.path.join(settings.BASE_DIR, 'contrib', 'sample_documents', TEST_NON_ASCII_DOCUMENT_FILENAME)
TEST_NON_ASCII_COMPRESSED_DOCUMENT_PATH = os.path.join(settings.BASE_DIR, 'contrib', 'sample_documents', TEST_NON_ASCII_COMPRESSED_DOCUMENT_FILENAME)
TEST_DOCUMENT_DESCRIPTION = 'test description'
TEST_DOCUMENT_TYPE = 'test_document_type'


class DocumentTestCase(TestCase):
    def setUp(self):
        self.document_type = DocumentType.objects.create(label=TEST_DOCUMENT_TYPE)

        ocr_settings = self.document_type.ocr_settings
        ocr_settings.auto_ocr = False
        ocr_settings.save()

        with open(TEST_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(file_object=File(file_object), label='mayan_11_1.pdf')

    def tearDown(self):
        self.document_type.delete()

    def test_document_creation(self):
        self.assertEqual(self.document_type.label, TEST_DOCUMENT_TYPE)

        self.assertEqual(self.document.exists(), True)
        self.assertEqual(self.document.size, 272213)

        self.assertEqual(self.document.file_mimetype, 'application/pdf')
        self.assertEqual(self.document.file_mime_encoding, 'binary')
        self.assertEqual(self.document.label, 'mayan_11_1.pdf')
        self.assertEqual(self.document.checksum, 'c637ffab6b8bb026ed3784afdb07663fddc60099853fae2be93890852a69ecf3')
        self.assertEqual(self.document.page_count, 47)

    def test_version_creation(self):
        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document.new_version(file_object=File(file_object))

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document.new_version(file_object=File(file_object), comment='test comment 1')

        self.assertEqual(self.document.versions.count(), 3)

    def test_restoring_documents(self):
        self.assertEqual(Document.objects.count(), 1)

        # Trash the document
        self.document.delete()
        self.assertEqual(DeletedDocument.objects.count(), 1)
        self.assertEqual(Document.objects.count(), 0)

        # Restore the document
        self.document.restore()
        self.assertEqual(DeletedDocument.objects.count(), 0)
        self.assertEqual(Document.objects.count(), 1)

    def test_trashing_documents(self):
        self.assertEqual(Document.objects.count(), 1)

        # Trash the document
        self.document.delete()
        self.assertEqual(DeletedDocument.objects.count(), 1)
        self.assertEqual(Document.objects.count(), 0)

        # Delete the document
        self.document.delete()
        self.assertEqual(DeletedDocument.objects.count(), 0)
        self.assertEqual(Document.objects.count(), 0)
