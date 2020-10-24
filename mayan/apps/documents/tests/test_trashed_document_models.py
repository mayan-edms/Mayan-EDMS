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
