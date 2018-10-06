from __future__ import unicode_literals

from django.test import override_settings
from django.urls import reverse

from rest_framework import status

from documents.search import document_search
from documents.permissions import permission_document_view
from documents.tests import DocumentTestMixin
from rest_api.tests import BaseAPITestCase

from ..classes import SearchModel


@override_settings(OCR_AUTO_OCR=False)
class SearchAPITestCase(DocumentTestMixin, BaseAPITestCase):
    auto_upload_document = False

    def setUp(self):
        super(SearchAPITestCase, self).setUp()
        self.login_user()

    def _request_search_view(self):
        return self.get(
            path='{}?q={}'.format(
                reverse(
                    'rest_api:search-view', args=(
                        document_search.get_full_name(),
                    )
                ), self.document.label
            )
        )

    def test_search_no_access(self):
        self.document = self.upload_document()
        response = self._request_search_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_search_with_access(self):
        self.document = self.upload_document()
        self.grant_access(
            permission=permission_document_view, obj=self.document
        )
        response = self._request_search_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['results'][0]['label'], self.document.label
        )
        self.assertEqual(response.data['count'], 1)

    def test_search_models_view(self):
        response = self.get(
            viewname='rest_api:searchmodel-list'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            [search_model['pk'] for search_model in response.data['results']],
            [search_model.pk for search_model in SearchModel.all()]
        )
