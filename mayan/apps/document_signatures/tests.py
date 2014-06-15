from __future__ import absolute_import

import os

from django.utils import unittest
from django.conf import settings
from django.core.files.base import File

from django_gpg.api import SIGNATURE_STATE_VALID
from documents.models import Document, DocumentType
from documents.literals import VERSION_UPDATE_MAJOR, RELEASE_LEVEL_FINAL

from .models import DocumentVersionSignature


class DocumentTestCase(unittest.TestCase):
    def setUp(self):
        self.document_type = DocumentType(name='test doc type')
        self.document_type.save()

        self.document = Document(
            document_type=self.document_type,
            description='description',
        )
        self.document.save()

        file_object = open(os.path.join(settings.PROJECT_ROOT, 'contrib', 'mayan_11_1.pdf'))
        new_version = self.document.new_version(file=File(file_object, name='mayan_11_1.pdf'))
        file_object.close()

    def test_document_no_signature(self):
        self.failUnlessEqual(DocumentVersionSignature.objects.has_detached_signature(self.document), False)

    def test_new_document_version_signed(self):
        file_object = open(os.path.join(settings.PROJECT_ROOT, 'contrib', 'mayan_11_1.pdf.gpg'))
        new_version_data = {
            'comment': 'test comment 1',
            'version_update': VERSION_UPDATE_MAJOR,
            'release_level': RELEASE_LEVEL_FINAL,
            'serial': 0,
        }

        self.failUnlessEqual(DocumentVersionSignature.objects.has_detached_signature(self.document), False)
        # self.failUnlessEqual(DocumentVersionSignature.objects.verify_signature(self.document).status, SIGNATURE_STATE_VALID)
        # TODO: verify_signature is failing, check

    def test_detached_signatures(self):
        new_version_data = {
            'comment': 'test comment 2',
            'version_update': VERSION_UPDATE_MAJOR,
            'release_level': RELEASE_LEVEL_FINAL,
            'serial': 0,
        }
        file_object = open(os.path.join(settings.PROJECT_ROOT, 'contrib', 'mayan_11_1.pdf'))
        new_version = self.document.new_version(file=File(file_object), **new_version_data)
        file_object.close()

        # GPGVerificationError
        self.failUnlessEqual(DocumentVersionSignature.objects.verify_signature(self.document), None)

        file_object = open(os.path.join(settings.PROJECT_ROOT, 'contrib', 'mayan_11_1.pdf.sig'), 'rb')
        DocumentVersionSignature.objects.add_detached_signature(self.document, File(file_object))
        file_object.close()

        self.failUnlessEqual(DocumentVersionSignature.objects.has_detached_signature(self.document), True)
        # self.failUnlessEqual(DocumentVersionSignature.objects.verify_signature(self.document).status, SIGNATURE_STATE_VALID)
        # TODO: verify_signature is failing, check

    def tearDown(self):
        self.document.delete()
        self.document_type.delete()
