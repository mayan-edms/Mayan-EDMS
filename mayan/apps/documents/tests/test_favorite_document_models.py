from django.test import override_settings

from ..models.favorite_document_models import FavoriteDocument

from .base import GenericDocumentTestCase
from .mixins.favorite_document_mixins import FavoriteDocumentTestMixin


@override_settings(DOCUMENTS_FAVORITE_COUNT=2)
class TrashedDocumentTestCase(
    FavoriteDocumentTestMixin, GenericDocumentTestCase
):
    auto_upload_test_document = False

    def test_favorite_documents_deletion_ordering(self):
        self._upload_test_document()
        self._test_document_favorite_add()

        first_favorite_document = self.test_favorite_document.document

        self._upload_test_document()
        self._test_document_favorite_add()

        self._upload_test_document()
        self._test_document_favorite_add()

        self.assertFalse(
            FavoriteDocument.objects.filter(document=first_favorite_document).exists()
        )
