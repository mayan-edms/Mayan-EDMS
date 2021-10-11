from django.test import override_settings

from ..models.favorite_document_models import FavoriteDocument

from .base import GenericDocumentTestCase
from .mixins.favorite_document_mixins import FavoriteDocumentTestMixin


@override_settings(DOCUMENTS_FAVORITE_COUNT=2)
class FavoriteDocumentModelTestCase(
    FavoriteDocumentTestMixin, GenericDocumentTestCase
):
    auto_upload_test_document = False

    def test_favorite_documents_deletion_ordering(self):
        self._create_test_document_stub()
        self._test_document_favorite_add()

        first_favorite_document = self.test_favorite_document.document

        self._create_test_document_stub()
        self._test_document_favorite_add()

        self._create_test_document_stub()
        self._test_document_favorite_add()

        self.assertFalse(
            FavoriteDocument.valid.filter(document=first_favorite_document).exists()
        )

    def test_trashed_document_favorite_document_add(self):
        self._create_test_document_stub()
        self.test_document.delete()
        self._test_document_favorite_add()

        self.assertFalse(
            FavoriteDocument.valid.filter(document=self.test_document).exists()
        )
