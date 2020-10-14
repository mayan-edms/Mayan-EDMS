from ...models.misc_models import FavoriteDocument


class FavoriteDocumentsTestMixin:
    def _document_add_to_favorites(self):
        FavoriteDocument.objects.add_for_user(
            document=self.test_document, user=self._test_case_user
        )


class FavoriteDocumentsViewTestMixin:
    def _request_document_add_to_favorites_view(self):
        return self.post(
            viewname='documents:document_add_to_favorites',
            kwargs={'document_id': self.test_document.pk}
        )

    def _document_add_to_favorites(self):
        FavoriteDocument.objects.add_for_user(
            document=self.test_document, user=self._test_case_user
        )

    def _request_document_list_favorites(self):
        return self.get(
            viewname='documents:document_list_favorites',
        )

    def _request_document_remove_from_favorites(self):
        return self.post(
            viewname='documents:document_remove_from_favorites',
            kwargs={'document_id': self.test_document.pk}
        )
