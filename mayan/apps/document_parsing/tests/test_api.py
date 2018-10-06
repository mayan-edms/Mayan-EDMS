from __future__ import unicode_literals

from django.test import override_settings

from rest_framework import status

from documents.tests import DocumentTestMixin, TEST_HYBRID_DOCUMENT
from rest_api.tests import BaseAPITestCase

from ..permissions import permission_content_view

TEST_DOCUMENT_CONTENT = 'Sample text'


@override_settings(OCR_AUTO_OCR=False)
class DocumentParsingAPITestCase(DocumentTestMixin, BaseAPITestCase):
    test_document_filename = TEST_HYBRID_DOCUMENT

    def setUp(self):
        super(DocumentParsingAPITestCase, self).setUp()
        self.login_user()

    def _request_document_page_content_view(self):
        return self.get(
            viewname='rest_api:document-page-content-view',
            args=(
                self.document.pk, self.document.latest_version.pk,
                self.document.latest_version.pages.first().pk,
            )
        )

    def test_get_document_version_page_content_no_access(self):
        response = self._request_document_page_content_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_document_version_page_content_with_access(self):
        self.grant_access(
            permission=permission_content_view, obj=self.document
        )
        response = self._request_document_page_content_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            TEST_DOCUMENT_CONTENT in response.data['content']
        )
