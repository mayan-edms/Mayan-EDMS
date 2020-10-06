from ..models import DeletedDocument, Document

from .base import GenericDocumentTestCase


class TrashedDocumentTestCase(GenericDocumentTestCase):
    def test_restoring_documents(self):
        self.assertEqual(Document.valid.count(), 1)

        # Trash the document
        self.test_document.delete()
        self.assertEqual(DeletedDocument.objects.count(), 1)
        self.assertEqual(Document.valid.count(), 0)

        # Restore the document
        self.test_document.restore()
        self.assertEqual(DeletedDocument.objects.count(), 0)
        self.assertEqual(Document.valid.count(), 1)

    def test_trashing_documents(self):
        self.assertEqual(Document.valid.count(), 1)

        # Trash the document
        self.test_document.delete()
        self.assertEqual(DeletedDocument.objects.count(), 1)
        self.assertEqual(Document.valid.count(), 0)

        # Delete the document
        self.test_document.delete()
        self.assertEqual(DeletedDocument.objects.count(), 0)
        self.assertEqual(Document.valid.count(), 0)
