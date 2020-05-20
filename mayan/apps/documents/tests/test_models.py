from datetime import timedelta
import time

from django.test import override_settings

from mayan.apps.common.tests.base import BaseTestCase
from mayan.apps.converter.layers import layer_saved_transformations

from ..models import (
    DeletedDocument, Document, DocumentType, DuplicatedDocument
)
from ..settings import setting_stub_expiration_interval

from .base import GenericDocumentTestCase
from .literals import (
    TEST_DOCUMENT_TYPE_LABEL, TEST_MULTI_PAGE_TIFF,
    TEST_OFFICE_DOCUMENT, TEST_PDF_INDIRECT_ROTATE_LABEL,
    TEST_PDF_ROTATE_ALTERNATE_LABEL, TEST_SMALL_DOCUMENT_CHECKSUM,
    TEST_SMALL_DOCUMENT_FILENAME, TEST_SMALL_DOCUMENT_MIMETYPE,
    TEST_SMALL_DOCUMENT_PATH, TEST_SMALL_DOCUMENT_SIZE
)


class DocumentTestCase(GenericDocumentTestCase):
    def test_document_creation(self):
        self.assertEqual(
            self.test_document_type.label, TEST_DOCUMENT_TYPE_LABEL
        )

        self.assertEqual(self.test_document.exists(), True)
        self.assertEqual(self.test_document.size, TEST_SMALL_DOCUMENT_SIZE)

        self.assertEqual(
            self.test_document.file_mimetype, TEST_SMALL_DOCUMENT_MIMETYPE
        )
        self.assertEqual(self.test_document.file_mime_encoding, 'binary')
        self.assertEqual(
            self.test_document.label, TEST_SMALL_DOCUMENT_FILENAME
        )
        self.assertEqual(
            self.test_document.checksum, TEST_SMALL_DOCUMENT_CHECKSUM
        )
        self.assertEqual(self.test_document.page_count, 1)

    def test_version_creation(self):
        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.test_document.new_version(file_object=file_object)

        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.test_document.new_version(
                file_object=file_object, comment='test comment 1'
            )

        self.assertEqual(self.test_document.versions.count(), 3)

    def test_restoring_documents(self):
        self.assertEqual(Document.objects.count(), 1)

        # Trash the document
        self.test_document.delete()
        self.assertEqual(DeletedDocument.objects.count(), 1)
        self.assertEqual(Document.objects.count(), 0)

        # Restore the document
        self.test_document.restore()
        self.assertEqual(DeletedDocument.objects.count(), 0)
        self.assertEqual(Document.objects.count(), 1)

    def test_trashing_documents(self):
        self.assertEqual(Document.objects.count(), 1)

        # Trash the document
        self.test_document.delete()
        self.assertEqual(DeletedDocument.objects.count(), 1)
        self.assertEqual(Document.objects.count(), 0)

        # Delete the document
        self.test_document.delete()
        self.assertEqual(DeletedDocument.objects.count(), 0)
        self.assertEqual(Document.objects.count(), 0)

    def test_auto_trashing(self):
        """
        Test document type trashing policies. Documents are moved to the
        trash, x amount of time after being uploaded
        """
        self.test_document_type.trash_time_period = 1
        # 'seconds' is not a choice via the model, used here for convenience
        self.test_document_type.trash_time_unit = 'seconds'
        self.test_document_type.save()

        # Needed by MySQL as milliseconds value is not store in timestamp
        # field
        time.sleep(1.01)

        self.assertEqual(Document.objects.count(), 1)
        self.assertEqual(DeletedDocument.objects.count(), 0)

        DocumentType.objects.check_trash_periods()

        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(DeletedDocument.objects.count(), 1)

    def test_auto_delete(self):
        """
        Test document type deletion policies. Documents are deleted from the
        trash, x amount of time after being trashed
        """
        self.test_document_type.delete_time_period = 1
        # 'seconds' is not a choice via the model, used here for convenience
        self.test_document_type.delete_time_unit = 'seconds'
        self.test_document_type.save()

        self.assertEqual(Document.objects.count(), 1)
        self.assertEqual(DeletedDocument.objects.count(), 0)

        self.test_document.delete()

        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(DeletedDocument.objects.count(), 1)

        # Needed by MySQL as milliseconds value is not stored in timestamp
        # field
        time.sleep(1.01)

        DocumentType.objects.check_delete_periods()

        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(DeletedDocument.objects.count(), 0)

    def test_method_get_absolute_url(self):
        self._upload_test_document()

        self.assertTrue(self.test_document.get_absolute_url())


@override_settings(DOCUMENTS_FIX_ORIENTATION=True)
class PDFAlternateRotationTestCase(GenericDocumentTestCase):
    test_document_filename = TEST_PDF_ROTATE_ALTERNATE_LABEL

    def test_rotate(self):
        self.assertQuerysetEqual(
            qs=Document.objects.all(), values=(repr(self.test_document),)
        )
        self.assertEqual(
            layer_saved_transformations.get_transformations_for(
                obj=self.test_document.latest_version.pages.first()
            ).count(), 1
        )


@override_settings(DOCUMENTS_FIX_ORIENTATION=True)
class PDFIndirectRotationTestCase(GenericDocumentTestCase):
    test_document_filename = TEST_PDF_INDIRECT_ROTATE_LABEL

    def test_rotate(self):
        self.assertQuerysetEqual(
            qs=Document.objects.all(), values=(repr(self.test_document),)
        )


class OfficeDocumentTestCase(GenericDocumentTestCase):
    test_document_filename = TEST_OFFICE_DOCUMENT

    def test_document_creation(self):
        self.assertEqual(
            self.test_document.file_mimetype, 'application/msword'
        )
        self.assertEqual(
            self.test_document.file_mime_encoding, 'binary'
        )
        self.assertEqual(
            self.test_document.checksum,
            '03a7e9071d2c6ae05a6588acd7dff1d890fac2772cf61abd470c9ffa6ef71f03'
        )
        self.assertEqual(self.test_document.page_count, 2)


class MultiPageTiffTestCase(GenericDocumentTestCase):
    test_document_filename = TEST_MULTI_PAGE_TIFF

    def test_document_creation(self):
        self.assertEqual(self.test_document.file_mimetype, 'image/tiff')
        self.assertEqual(self.test_document.file_mime_encoding, 'binary')
        self.assertEqual(
            self.test_document.checksum,
            '40adaa9d658b65c70a7f002dfe084a8354bb77c0dfbf1993e31fb024a285fb1d'
        )
        self.assertEqual(self.test_document.page_count, 2)


class DocumentVersionTestCase(GenericDocumentTestCase):
    def test_add_new_version(self):
        self.assertEqual(self.test_document.versions.count(), 1)

        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.test_document.new_version(
                file_object=file_object
            )

        self.assertEqual(self.test_document.versions.count(), 2)

        self.assertEqual(
            self.test_document.checksum,
            TEST_SMALL_DOCUMENT_CHECKSUM
        )

    def test_revert_version(self):
        self.assertEqual(self.test_document.versions.count(), 1)

        # Needed by MySQL as milliseconds value is not store in timestamp
        # field
        time.sleep(1.01)

        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.test_document.new_version(
                file_object=file_object
            )

        self.assertEqual(self.test_document.versions.count(), 2)

        self.test_document.versions.first().revert()

        self.assertEqual(self.test_document.versions.count(), 1)

    def test_method_get_absolute_url(self):
        self._upload_test_document()

        self.assertTrue(self.test_document.latest_version.get_absolute_url())


class DocumentManagerTestCase(BaseTestCase):
    def setUp(self):
        super(DocumentManagerTestCase, self).setUp()
        self.test_document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

    def tearDown(self):
        self.test_document_type.delete()
        super(DocumentManagerTestCase, self).tearDown()

    def test_document_stubs_deletion(self):
        document_stub = Document.objects.create(
            document_type=self.test_document_type
        )

        Document.passthrough.delete_stubs()

        self.assertEqual(Document.passthrough.count(), 1)

        document_stub.date_added = document_stub.date_added - timedelta(
            seconds=setting_stub_expiration_interval.value + 1
        )
        document_stub.save()

        Document.passthrough.delete_stubs()

        self.assertEqual(Document.passthrough.count(), 0)


class DocumentTypeModelTestCase(GenericDocumentTestCase):
    auto_upload_test_document = False

    def test_method_get_absolute_url(self):
        self.assertTrue(self.test_document_type.get_absolute_url())


class DuplicatedDocumentsTestCase(GenericDocumentTestCase):
    def test_duplicates_after_delete(self):
        self._upload_test_document()
        self.test_documents[1].delete()
        self.test_documents[1].delete()

        self.assertEqual(
            DuplicatedDocument.objects.filter(
                document=self.test_documents[0]
            ).count(), 0
        )

    def test_duplicates_after_trash(self):
        self._upload_test_document()
        self.test_documents[1].delete()

        self.assertFalse(
            self.test_documents[1] in DuplicatedDocument.objects.get(
                document=self.test_documents[0]
            ).documents.all()
        )

    def test_duplicate_scan(self):
        self._upload_test_document()

        self.assertTrue(
            self.test_documents[1] in DuplicatedDocument.objects.get(
                document=self.test_documents[0]
            ).documents.all()
        )
