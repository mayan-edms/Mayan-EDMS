from __future__ import unicode_literals

from django.test import override_settings

from rest_framework import status

from mayan.apps.documents.tests import DocumentTestMixin, TEST_HYBRID_DOCUMENT
from mayan.apps.rest_api.tests import BaseAPITestCase

from ..permissions import permission_content_view

from .literals import TEST_DOCUMENT_CONTENT


@override_settings(DOCUMENT_PARSING_AUTO_PARSING=True)
class DocumentParsingAPITestCase(DocumentTestMixin, BaseAPITestCase):
    test_document_filename = TEST_HYBRID_DOCUMENT

    def _request_document_page_content_view(self):
        return self.get(
            viewname='rest_api:document-page-content-view', kwargs={
                'document_pk': self.test_document.pk,
                'version_pk': self.test_document.latest_version.pk,
                'page_pk': self.test_document.latest_version.pages.first().pk
            }
        )

    def test_get_document_version_page_content_no_access(self):
        response = self._request_document_page_content_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_document_version_page_content_with_access(self):
        self.grant_access(
            permission=permission_content_view, obj=self.test_document
        )

        response = self._request_document_page_content_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(
            TEST_DOCUMENT_CONTENT in response.data['content']
        )
