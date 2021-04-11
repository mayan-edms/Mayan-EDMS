from datetime import timedelta

from ..models.document_models import Document
from ..settings import setting_stub_expiration_interval

from .base import GenericDocumentTestCase
from .literals import (
    TEST_SMALL_DOCUMENT_CHECKSUM, TEST_SMALL_DOCUMENT_FILENAME,
    TEST_SMALL_DOCUMENT_MIMETYPE, TEST_SMALL_DOCUMENT_SIZE
)


class DocumentTestCase(GenericDocumentTestCase):
    def test_document_creation(self):
        self.assertEqual(
            self.test_document.document_type.label,
            self.test_document_type.label
        )

        self.assertEqual(self.test_document.file_latest.exists(), True)
        self.assertEqual(
            self.test_document.file_latest.size,
            TEST_SMALL_DOCUMENT_SIZE
        )

        self.assertEqual(
            self.test_document.file_latest.mimetype,
            TEST_SMALL_DOCUMENT_MIMETYPE
        )
        self.assertEqual(
            self.test_document.file_latest.encoding, 'binary'
        )
        self.assertEqual(
            self.test_document.file_latest.checksum,
            TEST_SMALL_DOCUMENT_CHECKSUM
        )
        self.assertEqual(self.test_document.file_latest.pages.count(), 1)
        self.assertEqual(
            self.test_document.label, TEST_SMALL_DOCUMENT_FILENAME
        )

    def test_method_get_absolute_url(self):
        self._upload_test_document()

        self.assertTrue(self.test_document.get_absolute_url())


class DocumentManagerTestCase(GenericDocumentTestCase):
    auto_upload_test_document = False

    def test_document_stubs_deletion(self):
        document_stub = Document.objects.create(
            document_type=self.test_document_type
        )

        Document.objects.delete_stubs()

        self.assertEqual(Document.objects.count(), 1)

        document_stub.datetime_created = document_stub.datetime_created - timedelta(
            seconds=setting_stub_expiration_interval.value + 1
        )
        document_stub.save()

        Document.objects.delete_stubs()

        self.assertEqual(Document.objects.count(), 0)
