# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from json import loads
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from .models import Document, DocumentType

TEST_ADMIN_PASSWORD = 'test_admin_password'
TEST_ADMIN_USERNAME = 'test_admin'
TEST_ADMIN_EMAIL = 'admin@admin.com'
TEST_SMALL_DOCUMENT_FILENAME = 'title_page.png'
TEST_NON_ASCII_DOCUMENT_FILENAME = 'I18N_title_áéíóúüñÑ.png'
TEST_NON_ASCII_COMPRESSED_DOCUMENT_FILENAME = 'I18N_title_áéíóúüñÑ.png.zip'
TEST_DOCUMENT_PATH = os.path.join(settings.BASE_DIR, 'contrib', 'sample_documents', 'mayan_11_1.pdf')
TEST_SIGNED_DOCUMENT_PATH = os.path.join(settings.BASE_DIR, 'contrib', 'sample_documents', 'mayan_11_1.pdf.gpg')
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

    def test_document_creation(self):
        self.failUnlessEqual(self.document_type.label, TEST_DOCUMENT_TYPE)

        self.failUnlessEqual(self.document.exists(), True)
        self.failUnlessEqual(self.document.size, 272213)

        self.failUnlessEqual(self.document.file_mimetype, 'application/pdf')
        self.failUnlessEqual(self.document.file_mime_encoding, 'binary')
        self.failUnlessEqual(self.document.label, 'mayan_11_1.pdf')
        self.failUnlessEqual(self.document.checksum, 'c637ffab6b8bb026ed3784afdb07663fddc60099853fae2be93890852a69ecf3')
        self.failUnlessEqual(self.document.page_count, 47)

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document.new_version(file_object=File(file_object))

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document.new_version(file_object=File(file_object), comment='test comment 1')

        self.failUnlessEqual(self.document.versions.count(), 3)

    def tearDown(self):
        self.document.delete()
        self.document_type.delete()
