from rest_framework import status

from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests.base import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..classes import SearchModel

from .mixins import SearchAPIViewTestMixin


class SearchModelAPIViewTestCase(BaseAPITestCase):
    def test_search_models_api_view(self):
        response = self.get(
            viewname='rest_api:searchmodel-list', query={'page_size': 50}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            [search_model['pk'] for search_model in response.data['results']],
            [search_model.pk for search_model in SearchModel.all()]
        )


class SearchAPIViewTestCase(
    SearchAPIViewTestMixin, DocumentTestMixin, BaseAPITestCase
):
    def test_search_api_view_no_permission(self):
        response = self._request_search_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_search_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_search_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'], self.test_document.label
        )
        self.assertEqual(response.data['count'], 1)

    def test_advanced_search_api_view_no_permission(self):
        response = self._request_advanced_search_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_advanced_search_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_advanced_search_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'], self.test_document.label
        )
        self.assertEqual(response.data['count'], 1)
