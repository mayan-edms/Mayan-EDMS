from mayan.apps.documents.tests.base import GenericDocumentTestCase

from ..models import DuplicateBackendEntry, StoredDuplicateBackend

from .mixins import DuplicatedDocumentTestMixin


class DuplicatedDocumentModelTestCase(
    DuplicatedDocumentTestMixin, GenericDocumentTestCase
):
    def test_duplicates_after_delete(self):
        self._upload_duplicate_document()
        self.test_documents[1].delete()
        self.test_documents[1].delete()

        self.assertEqual(
            DuplicateBackendEntry.objects.filter(
                document=self.test_documents[0]
            ).count(), 0
        )

    def test_duplicates_after_trash(self):
        self._upload_duplicate_document()
        self.test_documents[1].delete()

        self.assertFalse(
            self.test_documents[1] in DuplicateBackendEntry.objects.get_duplicates_of(
                document=self.test_documents[0]
            )
        )

    def test_duplicate_scan_after_upload(self):
        self._upload_duplicate_document()

        self.assertTrue(
            self.test_documents[1] in DuplicateBackendEntry.objects.get_duplicates_of(
                document=self.test_documents[0]
            )
        )
        self.assertTrue(
            self.test_documents[0] in DuplicateBackendEntry.objects.get_duplicates_of(
                document=self.test_documents[1]
            )
        )

    def test_double_duplicated_entry_for_a_single_document(self):
        self._upload_duplicate_document()

        # Should not return an error.
        StoredDuplicateBackend.objects.scan_document(
            document=self.test_documents[0]
        )
