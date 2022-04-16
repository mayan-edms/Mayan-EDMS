from rest_framework import status

from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..classes import SearchModel

from .mixins import SearchAPIViewTestMixin, SearchTestMixin


class SearchAPIViewBackwardCompatilityTestCase(
    SearchAPIViewTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def test_search_model_name_uppercase_api_view_with_access(self):
        response = self._request_search_view(
            search_model_name='documents.Document', search_term='_'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)


class SearchAPIViewTestCase(
    DocumentTestMixin, SearchAPIViewTestMixin, BaseAPITestCase
):
    def test_search_api_view_no_permission(self):
        response = self._request_search_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_search_api_view_with_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        response = self._request_search_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'], self._test_document.label
        )
        self.assertEqual(response.data['count'], 1)

    def test_advanced_search_api_view_no_permission(self):
        response = self._request_advanced_search_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_advanced_search_api_view_with_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        response = self._request_advanced_search_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'], self._test_document.label
        )
        self.assertEqual(response.data['count'], 1)


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


class RESTAPISearchFilterTestCase(
    DocumentTestMixin, SearchTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub(label='ABCDEFGH')
        self._create_test_document_stub(label='12345678')

    def test_document_list_filter_with_access(self):
        self.grant_access(
            obj=self._test_documents[0], permission=permission_document_view
        )
        self.grant_access(
            obj=self._test_documents[1], permission=permission_document_view
        )

        response = self.get(
            viewname='rest_api:document-list', query={
                'label': self._test_documents[0].label
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'],
            self._test_documents[0].label
        )
        self.assertEqual(response.data['count'], 1)

        response = self.get(
            viewname='rest_api:document-list', query={
                'label': self._test_documents[1].label
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'],
            self._test_documents[1].label
        )
        self.assertEqual(response.data['count'], 1)

    def test_document_list_filter_any_field_with_access(self):
        self.grant_access(
            obj=self._test_documents[0], permission=permission_document_view
        )
        self.grant_access(
            obj=self._test_documents[1], permission=permission_document_view
        )

        response = self.get(
            viewname='rest_api:document-list', query={
                'q': self._test_documents[0].label
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'],
            self._test_documents[0].label
        )
        self.assertEqual(response.data['count'], 1)
