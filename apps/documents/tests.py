from __future__ import absolute_import

import os

from django.utils import unittest
from django.conf import settings
from django.core.files.base import File

from django_gpg.api import SIGNATURE_STATE_VALID

from .models import Document, DocumentType
from .literals import VERSION_UPDATE_MAJOR, RELEASE_LEVEL_FINAL


class DocumentTestCase(unittest.TestCase):
    def setUp(self):
        self.document_type = DocumentType(name='test doc type')
        self.document_type.save()

        self.document = Document(
            document_type=self.document_type,
            description='description',
        )
        self.document.save()
        #return File(file(self.filepath, 'rb'), name=self.filename)

        file_object = open(os.path.join(settings.PROJECT_ROOT, 'contrib', 'mayan_11_1.pdf'))
        new_version = self.document.new_version(file=File(file_object, name='mayan_11_1.pdf'))
        file_object.close()

    def runTest(self):
        self.failUnlessEqual(self.document_type.name, 'test doc type')

        self.failUnlessEqual(self.document.exists(), True)
        self.failUnlessEqual(self.document.size, 272213)

        self.failUnlessEqual(self.document.file_mimetype, 'application/pdf')
        self.failUnlessEqual(self.document.file_mime_encoding, 'binary')
        self.failUnlessEqual(self.document.file_filename, 'mayan_11_1.pdf')
        self.failUnlessEqual(self.document.checksum, 'c637ffab6b8bb026ed3784afdb07663fddc60099853fae2be93890852a69ecf3')
        self.failUnlessEqual(self.document.page_count, 47)

        self.failUnlessEqual(self.document.latest_version.get_formated_version(), '1.0')
        self.failUnlessEqual(self.document.has_detached_signature(), False)

        file_object = open(os.path.join(settings.PROJECT_ROOT, 'contrib', 'mayan_11_1.pdf.gpg'))
        new_version_data = {
            'comment': 'test comment 1',
            'version_update': VERSION_UPDATE_MAJOR,
            'release_level': RELEASE_LEVEL_FINAL,
            'serial': 0,
        }

        new_version = self.document.new_version(file=File(file_object, name='mayan_11_1.pdf.gpg'), **new_version_data)
        file_object.close()

        self.failUnlessEqual(self.document.latest_version.get_formated_version(), '2.0')
        self.failUnlessEqual(self.document.has_detached_signature(), False)

        self.failUnlessEqual(self.document.verify_signature().status, SIGNATURE_STATE_VALID)

        new_version_data = {
            'comment': 'test comment 2',
            'version_update': VERSION_UPDATE_MAJOR,
            'release_level': RELEASE_LEVEL_FINAL,
            'serial': 0,
        }
        file_object = open(os.path.join(settings.PROJECT_ROOT, 'contrib', 'mayan_11_1.pdf'))
        new_version = self.document.new_version(file=File(file_object), **new_version_data)
        file_object.close()

        self.failUnlessEqual(self.document.latest_version.get_formated_version(), '3.0')

        #GPGVerificationError
        self.failUnlessEqual(self.document.verify_signature(), None)

        file_object = open(os.path.join(settings.PROJECT_ROOT, 'contrib', 'mayan_11_1.pdf.sig'), 'rb')
        new_version = self.document.add_detached_signature(File(file_object))
        file_object.close()

        self.failUnlessEqual(self.document.has_detached_signature(), True)
        self.failUnlessEqual(self.document.verify_signature().status, SIGNATURE_STATE_VALID)

    def tearDown(self):
        self.document.delete()
