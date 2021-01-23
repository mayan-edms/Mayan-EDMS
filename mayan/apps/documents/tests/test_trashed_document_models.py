from ..models import Document, TrashedDocument

from .base import GenericDocumentTestCase


class TrashedDocumentTestCase(GenericDocumentTestCase):
    def test_restoring_documents(self):
        self.assertEqual(Document.valid.count(), 1)

        # Trash the document
        self.test_document.delete()
        self.assertEqual(TrashedDocument.objects.count(), 1)
        self.assertEqual(Document.valid.count(), 0)

        # Restore the document
        TrashedDocument.objects.get(pk=self.test_document.pk).restore()
        self.assertEqual(TrashedDocument.objects.count(), 0)
        self.assertEqual(Document.valid.count(), 1)

    def test_trashing_documents(self):
        self.assertEqual(Document.valid.count(), 1)

        # Trash the document
        self.test_document.delete()
        self.assertEqual(TrashedDocument.objects.count(), 1)
        self.assertEqual(Document.valid.count(), 0)

        # Delete the document
        self.test_document.delete()
        self.assertEqual(TrashedDocument.objects.count(), 0)
        self.assertEqual(Document.valid.count(), 0)

    def test_trashed_document_page_count(self):
        page_count = self.test_document.version_active.pages.count()
        self.test_document.delete()
        test_trashed_document = TrashedDocument.objects.get(
            pk=self.test_document.pk
        )
        self.assertTrue(
            test_trashed_document.version_active.pages.count(), page_count
        )


class TrashedDocumentAPITestCase(GenericDocumentTestCase):
    def test_trashed_document_api_image_url(self):
        self.test_document.delete()
        test_trashed_document = TrashedDocument.objects.get(
            pk=self.test_document.pk
        )
        self.assertTrue(test_trashed_document.get_api_image_url())
