from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..permissions import (
    permission_document_file_delete, permission_document_file_new,
    permission_document_file_view
)

from .mixins.document_mixins import DocumentTestMixin
from .mixins.document_file_mixins import (
    DocumentFileTestMixin, DocumentFilePageAPIViewTestMixin
)


class DocumentFilePageAPIViewTestCase(
    DocumentFilePageAPIViewTestMixin, DocumentTestMixin, BaseAPITestCase
):
    def test_document_file_page_image_api_view_no_permission(self):
        response = self._request_test_document_file_page_image_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_file_page_image_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        response = self._request_test_document_file_page_image_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
