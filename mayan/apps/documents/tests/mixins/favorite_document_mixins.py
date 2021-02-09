from django.db.models import Q

from ...models.favorite_document_models import FavoriteDocument


class FavoriteDocumentAPIViewTestMixin:
    def _request_test_favorite_document_create_api_view(self):
        pk_list = list(FavoriteDocument.objects.values_list('pk', flat=True))

        response = self.post(
            viewname='rest_api:favoritedocument-list', data={
                'document_id': self.test_document.pk
            }
        )

        try:
            self.test_favorite_document = FavoriteDocument.objects.get(
                ~Q(pk__in=pk_list)
            )
        except FavoriteDocument.DoesNotExist:
            self.test_favorite_document = None

        return response

    def _request_test_favorite_document_delete_api_view(self):
        return self.delete(
            viewname='rest_api:favoritedocument-detail', kwargs={
                'favorite_document_id': self.test_favorite_document.pk
            }
        )

    def _request_test_favorite_document_detail_api_view(self):
        return self.get(
            viewname='rest_api:favoritedocument-detail', kwargs={
                'favorite_document_id': self.test_favorite_document.pk
            }
        )

    def _request_test_favorite_document_list_api_view(self):
        return self.get(viewname='rest_api:favoritedocument-list')


class FavoriteDocumentTestMixin:
    def _test_document_favorite_add(self):
        self.test_favorite_document = FavoriteDocument.objects.add_for_user(
            document=self.test_document, user=self._test_case_user
        )


class FavoriteDocumentsViewTestMixin:
    def _request_test_document_favorite_add_view(self):
        return self.post(
            viewname='documents:document_favorite_add',
            kwargs={'document_id': self.test_document.pk}
        )

    def _request_test_document_favorites_list_view(self):
        return self.get(
            viewname='documents:document_favorite_list',
        )

    def _request_test_document_favorite_remove_view(self):
        return self.post(
            viewname='documents:document_favorite_remove',
            kwargs={'document_id': self.test_document.pk}
        )
