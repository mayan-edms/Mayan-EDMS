from ..models import TrashedDocument, Document, DocumentType

from .base import GenericDocumentTestCase


class DocumentTypeDeletionPoliciesTestCase(GenericDocumentTestCase):
    def test_auto_trashing(self):
        """
        Test document type trashing policies. Documents are moved to the
        trash, x amount of time after being uploaded
        """
        self.test_document_type.trash_time_period = 1
        # 'seconds' is not a choice via the model, used here for convenience
        self.test_document_type.trash_time_unit = 'seconds'
        self.test_document_type.save()

        self._test_delay(seconds=1.01)

        self.assertEqual(Document.valid.count(), 1)
        self.assertEqual(TrashedDocument.objects.count(), 0)

        DocumentType.objects.check_trash_periods()

        self.assertEqual(Document.valid.count(), 0)
        self.assertEqual(TrashedDocument.objects.count(), 1)

    def test_auto_delete(self):
        """
        Test document type deletion policies. Documents are deleted from the
        trash, x amount of time after being trashed
        """
        self.test_document_type.delete_time_period = 1
        # 'seconds' is not a choice via the model, used here for convenience
        self.test_document_type.delete_time_unit = 'seconds'
        self.test_document_type.save()

        self.assertEqual(Document.valid.count(), 1)
        self.assertEqual(TrashedDocument.objects.count(), 0)

        self.test_document.delete()

        self.assertEqual(Document.valid.count(), 0)
        self.assertEqual(TrashedDocument.objects.count(), 1)

        self._test_delay(seconds=1.01)

        DocumentType.objects.check_delete_periods()

        self.assertEqual(Document.valid.count(), 0)
        self.assertEqual(TrashedDocument.objects.count(), 0)


class DocumentTypeModelTestCase(GenericDocumentTestCase):
    auto_upload_test_document = False

    def test_method_get_absolute_url(self):
        self.assertTrue(self.test_document_type.get_absolute_url())

    def test_original_filename_backend(self):
        self.test_document_type.filename_generator_backend = 'original'
        self.test_document_type.save()
        self._upload_test_document()
        self.assertEqual(
            self.test_document_filename,
            self.test_document.file_latest.file
        )
