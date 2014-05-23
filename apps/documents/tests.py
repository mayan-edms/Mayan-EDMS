from __future__ import absolute_import

import os

from django.utils import unittest
from django.conf import settings
from django.core.files.base import File

# from django_gpg.api import SIGNATURE_STATE_VALID

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
        # return File(file(self.filepath, 'rb'), name=self.filename)

        file_object = open(os.path.join(settings.PROJECT_ROOT, 'contrib', 'mayan_11_1.pdf'))
        new_version = self.document.new_version(file=File(file_object, name='mayan_11_1.pdf'))
        file_object.close()

    def test_document_creation(self):
        self.failUnlessEqual(self.document_type.name, 'test doc type')

        self.failUnlessEqual(self.document.exists(), True)
        self.failUnlessEqual(self.document.size, 272213)

        self.failUnlessEqual(self.document.file_mimetype, 'application/pdf')
        self.failUnlessEqual(self.document.file_mime_encoding, 'binary')
        self.failUnlessEqual(self.document.file_filename, 'mayan_11_1.pdf')
        self.failUnlessEqual(self.document.checksum, 'c637ffab6b8bb026ed3784afdb07663fddc60099853fae2be93890852a69ecf3')
        self.failUnlessEqual(self.document.page_count, 47)

        self.failUnlessEqual(self.document.latest_version.get_formated_version(), '1.0')
        # self.failUnlessEqual(self.document.has_detached_signature(), False)

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
        # self.failUnlessEqual(self.document.has_detached_signature(), False)

        # self.failUnlessEqual(self.document.verify_signature().status, SIGNATURE_STATE_VALID)

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

        # GPGVerificationError
        # self.failUnlessEqual(self.document.verify_signature(), None)

        # file_object = open(os.path.join(settings.PROJECT_ROOT, 'contrib', 'mayan_11_1.pdf.sig'), 'rb')
        # new_version = self.document.add_detached_signature(File(file_object))
        # file_object.close()

        # self.failUnlessEqual(self.document.has_detached_signature(), True)
        # self.failUnlessEqual(self.document.verify_signature().status, SIGNATURE_STATE_VALID)

    def tearDown(self):
        self.document.delete()
        self.document_type.delete()


class DocumentSearchTestCase(unittest.TestCase):
    def setUp(self):
        from ocr.parsers import parse_document_page
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
        # Text extraction on the first page only
        parse_document_page(self.document.latest_version.pages.all()[0])

    def test_simple_search_after_related_name_change(self):
        from . import document_search
        """
        Test that simple search works after related_name changes to
        document versions and document version pages
        """
        model_list, flat_list, shown_result_count, result_count, elapsed_time = document_search.simple_search('Mayan')
        self.assertEqual(result_count, 1)
        self.assertEqual(flat_list, [self.document])

    def test_advanced_search_after_related_name_change(self):
        from . import document_search
        # Test versions__filename
        model_list, flat_list, shown_result_count, result_count, elapsed_time = document_search.advanced_search({'versions__filename': self.document.filename})
        self.assertEqual(result_count, 1)
        self.assertEqual(flat_list, [self.document])

        # Test versions__mimetype
        model_list, flat_list, shown_result_count, result_count, elapsed_time = document_search.advanced_search({'versions__mimetype': self.document.file_mimetype})
        self.assertEqual(result_count, 1)
        self.assertEqual(flat_list, [self.document])

        # Test versions__pages__content
        # Search by the first 20 characters of the content of the first page of the uploaded document
        model_list, flat_list, shown_result_count, result_count, elapsed_time = document_search.advanced_search({'versions__pages__content': self.document.latest_version.pages.all()[0].content[0:20]})
        self.assertEqual(result_count, 1)
        self.assertEqual(flat_list, [self.document])

    def tearDown(self):
        self.document.delete()
        self.document_type.delete()
