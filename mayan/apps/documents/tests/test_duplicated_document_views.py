from __future__ import unicode_literals

from ..permissions import permission_document_view

from .base import GenericDocumentViewTestCase


class DuplicatedDocumentsViewsTestCase(GenericDocumentViewTestCase):
    def _upload_duplicate_document(self):
        self.test_duplicated_document = self.upload_document()

    def _request_duplicated_document_list_view(self):
        return self.get(viewname='documents:duplicated_document_list')

    def _request_document_duplicates_list_view(self):
        return self.get(
            viewname='documents:document_duplicates_list',
            kwargs={'pk': self.test_document.pk}
        )

    def test_duplicated_document_list_no_permissions(self):
        self._upload_duplicate_document()

        response = self._request_duplicated_document_list_view()
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )

    def test_duplicated_document_list_with_access(self):
        self._upload_duplicate_document()
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_duplicated_document,
            permission=permission_document_view
        )

        response = self._request_duplicated_document_list_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )

    def test_document_duplicates_list_no_permissions(self):
        self._upload_duplicate_document()

        response = self._request_document_duplicates_list_view()
        self.assertEqual(response.status_code, 403)

    def test_document_duplicates_list_with_access(self):
        self._upload_duplicate_document()
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_duplicated_document,
            permission=permission_document_view
        )

        response = self._request_document_duplicates_list_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )
