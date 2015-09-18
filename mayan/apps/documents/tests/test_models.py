from __future__ import unicode_literals

import time

from django.core.files import File
from django.test import TestCase, override_settings

from .literals import (
    TEST_DOCUMENT_TYPE, TEST_DOCUMENT_PATH, TEST_MULTI_PAGE_TIFF_PATH,
    TEST_OFFICE_DOCUMENT_PATH, TEST_SMALL_DOCUMENT_PATH
)
from ..models import DeletedDocument, Document, DocumentType


@override_settings(OCR_AUTO_OCR=False)
class DocumentTestCase(TestCase):
    def setUp(self):
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=File(file_object), label='mayan_11_1.pdf'
            )

    def tearDown(self):
        self.document_type.delete()

    def test_document_creation(self):
        self.assertEqual(self.document_type.label, TEST_DOCUMENT_TYPE)

        self.assertEqual(self.document.exists(), True)
        self.assertEqual(self.document.size, 272213)

        self.assertEqual(self.document.file_mimetype, 'application/pdf')
        self.assertEqual(self.document.file_mime_encoding, 'binary')
        self.assertEqual(self.document.label, 'mayan_11_1.pdf')
        self.assertEqual(
            self.document.checksum,
            'c637ffab6b8bb026ed3784afdb07663fddc60099853fae2be93890852a69ecf3'
        )
        self.assertEqual(self.document.page_count, 47)

    def test_version_creation(self):
        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document.new_version(file_object=File(file_object))

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document.new_version(
                file_object=File(file_object), comment='test comment 1'
            )

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


@override_settings(OCR_AUTO_OCR=False)
class OfficeDocumentTestCase(TestCase):
    def setUp(self):
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_OFFICE_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=File(file_object)
            )

    def tearDown(self):
        self.document_type.delete()

    def test_document_creation(self):
        self.assertEqual(self.document.file_mimetype, 'application/msword')
        self.assertEqual(self.document.file_mime_encoding, 'application/mswordbinary')
        self.assertEqual(
            self.document.checksum,
            '03a7e9071d2c6ae05a6588acd7dff1d890fac2772cf61abd470c9ffa6ef71f03'
        )
        self.assertEqual(self.document.page_count, 2)


@override_settings(OCR_AUTO_OCR=False)
class MultiPageTiffTestCase(TestCase):
    def setUp(self):
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_MULTI_PAGE_TIFF_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=File(file_object)
            )

    def tearDown(self):
        self.document_type.delete()

    def test_document_creation(self):
        self.assertEqual(self.document.file_mimetype, 'image/tiff')
        self.assertEqual(self.document.file_mime_encoding, 'binary')
        self.assertEqual(
            self.document.checksum,
            '40adaa9d658b65c70a7f002dfe084a8354bb77c0dfbf1993e31fb024a285fb1d'
        )
        self.assertEqual(self.document.page_count, 2)


@override_settings(OCR_AUTO_OCR=False)
class DocumentVersionTestCase(TestCase):
    def setUp(self):
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=File(file_object)
            )

    def tearDown(self):
        self.document_type.delete()

    def test_add_new_version(self):
        self.assertEqual(self.document.versions.count(), 1)

        with open(TEST_DOCUMENT_PATH) as file_object:
            self.document.new_version(
                file_object=File(file_object)
            )

        self.assertEqual(self.document.versions.count(), 2)

        self.assertEqual(
            self.document.checksum,
            'c637ffab6b8bb026ed3784afdb07663fddc60099853fae2be93890852a69ecf3'
        )

    def test_revert_version(self):
        self.assertEqual(self.document.versions.count(), 1)

        # Needed by MySQL as milliseconds value is not store in timestamp field
        time.sleep(1)

        with open(TEST_DOCUMENT_PATH) as file_object:
            self.document.new_version(
                file_object=File(file_object)
            )

        self.assertEqual(self.document.versions.count(), 2)

        self.document.versions.first().revert()

        self.assertEqual(self.document.versions.count(), 1)
