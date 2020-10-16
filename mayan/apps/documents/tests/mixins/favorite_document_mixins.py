from ...models.misc_models import FavoriteDocument


class FavoriteDocumentsTestMixin:
    def _document_add_to_favorites(self):
        FavoriteDocument.objects.add_for_user(
            document=self.test_document, user=self._test_case_user
        )


class FavoriteDocumentsViewTestMixin:
    def _request_test_document_favorites_add_view(self):
        return self.post(
            viewname='documents:document_add_to_favorites',
            kwargs={'document_id': self.test_document.pk}
        )

    def _request_test_document_favorites_list_view(self):
        return self.get(
            viewname='documents:document_list_favorites',
        )

    def _request_test_document_favorites_remove_view(self):
        return self.post(
            viewname='documents:document_remove_from_favorites',
            kwargs={'document_id': self.test_document.pk}
        )
