from __future__ import unicode_literals

from django.test import override_settings

from rest_framework import status

from documents.search import document_search
from documents.permissions import permission_document_view
from documents.tests import DocumentTestMixin
from rest_api.tests import BaseAPITestCase

from ..classes import SearchModel


class SearchModelAPITestCase(BaseAPITestCase):
    def test_search_models_view(self):
        response = self.get(
            viewname='rest_api:searchmodel-list'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            [search_model['pk'] for search_model in response.data['results']],
            [search_model.pk for search_model in SearchModel.all()]
        )


@override_settings(OCR_AUTO_OCR=False)
class SearchAPITestCase(DocumentTestMixin, BaseAPITestCase):
    auto_upload_document = False

    def setUp(self):
        super(SearchAPITestCase, self).setUp()
        self.login_user()
        self.test_document = self.upload_document()

    def _request_search_view(self):
        query = {'q': self.test_document.label}
        return self.get(
            viewname='rest_api:search-view', kwargs={
                'search_model': document_search.get_full_name()
            }, query=query
        )

    def test_search_no_permission(self):
        response = self._request_search_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_search_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        response = self._request_search_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['results'][0]['label'], self.test_document.label
        )
        self.assertEqual(response.data['count'], 1)

    def _request_advanced_search_view(self):
        query = {'document_type__label': self.test_document.document_type.label}

        return self.get(
            viewname='rest_api:advanced-search-view', kwargs={
                'search_model': document_search.get_full_name()
            }, query=query
        )

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
