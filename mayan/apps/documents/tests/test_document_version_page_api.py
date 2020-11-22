from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..permissions import permission_document_version_view

from .mixins.document_mixins import DocumentTestMixin
from .mixins.document_version_mixins import (
    DocumentVersionPageAPIViewTestMixin
)


class DocumentVersionPageAPIViewTestCase(
    DocumentVersionPageAPIViewTestMixin, DocumentTestMixin, BaseAPITestCase
):
    def test_document_version_page_image_api_view_no_permission(self):
        response = self._request_test_document_version_page_image_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_version_page_image_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_view
        )

        response = self._request_test_document_version_page_image_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
