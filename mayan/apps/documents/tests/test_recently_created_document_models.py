from ..models.document_models import RecentlyCreatedDocument

from .base import GenericDocumentTestCase


class RecentlyCreatedDocumentModelTestCase(GenericDocumentTestCase):
    auto_upload_test_document = False

    def test_trashed_document_created_document_add(self):
        self._create_test_document_stub()
        self._test_document.delete()

        self.assertFalse(
            RecentlyCreatedDocument.valid.filter(
                pk=self._test_document.pk
            ).exists()
        )
