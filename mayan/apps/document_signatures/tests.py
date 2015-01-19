from __future__ import unicode_literals

import os

from django.conf import settings
from django.core.files.base import File
from django.test import TestCase

from documents.models import Document, DocumentType
from django_gpg.literals import SIGNATURE_STATE_VALID
from django_gpg.runtime import gpg

from .models import DocumentVersionSignature

TEST_DOCUMENT_PATH = os.path.join(settings.BASE_DIR, 'contrib', 'sample_documents', 'mayan_11_1.pdf')
TEST_SIGNED_DOCUMENT_PATH = os.path.join(settings.BASE_DIR, 'contrib', 'sample_documents', 'mayan_11_1.pdf.gpg')
TEST_SIGNATURE_FILE_PATH = os.path.join(settings.BASE_DIR, 'contrib', 'sample_documents', 'mayan_11_1.pdf.sig')
TEST_KEY_FILE = os.path.join(settings.BASE_DIR, 'contrib', 'sample_documents', 'key0x5F3F7F75D210724D.asc')


class DocumentTestCase(TestCase):
    def setUp(self):
        self.document_type = DocumentType(name='test doc type')
        self.document_type.save()

        self.document = Document(
            document_type=self.document_type,
            description='description',
        )
        self.document.save()

        with open(TEST_DOCUMENT_PATH) as file_object:
            self.document.new_version(file_object=File(file_object, name='mayan_11_1.pdf'))

        with open(TEST_KEY_FILE) as file_object:
            gpg.import_key(file_object.read())

    def test_document_no_signature(self):
        self.failUnlessEqual(DocumentVersionSignature.objects.has_detached_signature(self.document), False)

    def test_new_document_version_signed(self):
        with open(TEST_SIGNED_DOCUMENT_PATH) as file_object:
            new_version_data = {
                'comment': 'test comment 1',
            }

            self.document.new_version(file_object=File(file_object, name='mayan_11_1.pdf.gpg'), **new_version_data)

        self.failUnlessEqual(DocumentVersionSignature.objects.has_detached_signature(self.document), False)
        self.failUnlessEqual(DocumentVersionSignature.objects.verify_signature(self.document).status, SIGNATURE_STATE_VALID)

    def test_detached_signatures(self):
        new_version_data = {
            'comment': 'test comment 2',
        }
        with open(TEST_DOCUMENT_PATH) as file_object:
            self.document.new_version(file_object=File(file_object), **new_version_data)

        # GPGVerificationError
        self.failUnlessEqual(DocumentVersionSignature.objects.verify_signature(self.document), None)

        with open(TEST_SIGNATURE_FILE_PATH, 'rb') as file_object:
            DocumentVersionSignature.objects.add_detached_signature(self.document, File(file_object))

        self.failUnlessEqual(DocumentVersionSignature.objects.has_detached_signature(self.document), True)
        self.failUnlessEqual(DocumentVersionSignature.objects.verify_signature(self.document).status, SIGNATURE_STATE_VALID)

    def tearDown(self):
        self.document.delete()
        self.document_type.delete()
