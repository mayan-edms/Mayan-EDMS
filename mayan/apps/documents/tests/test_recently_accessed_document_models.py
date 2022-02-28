from ..models.recently_accessed_document_models import RecentlyAccessedDocument

from .base import GenericDocumentTestCase


class RecentlyAccessedDocumentModelTestCase(GenericDocumentTestCase):
    auto_upload_test_document = False

    def test_trashed_document_accessed_document_add(self):
        self._create_test_document_stub()
        self._test_document.delete()
        self._test_document.add_as_recent_document_for_user(
            user=self._test_case_user
        )

        self.assertFalse(
            RecentlyAccessedDocument.valid.filter(
                document=self._test_document
            ).exists()
        )
