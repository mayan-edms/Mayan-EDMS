from __future__ import unicode_literals

from ..permissions import permission_document_view

from .base import GenericDocumentViewTestCase


class DuplicatedDocumentsViewsTestMixin(object):
    def _upload_duplicate_document(self):
        self.upload_document()

    def _request_duplicated_document_list_view(self):
        return self.get(viewname='documents:duplicated_document_list')

    def _request_document_duplicates_list_view(self):
        return self.get(
            viewname='documents:document_duplicates_list',
            kwargs={'pk': self.test_documents[0].pk}
        )


class DuplicatedDocumentsViewsTestCase(
    DuplicatedDocumentsViewsTestMixin, GenericDocumentViewTestCase
):
    def test_duplicated_document_list_no_permissions(self):
        self._upload_duplicate_document()

        response = self._request_duplicated_document_list_view()
        self.assertNotContains(
            response=response, text=self.test_documents[0].label,
            status_code=200
        )

    def test_duplicated_document_list_with_access(self):
        self._upload_duplicate_document()
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_view
        )

        response = self._request_duplicated_document_list_view()
        self.assertContains(
            response=response, text=self.test_documents[0].label,
            status_code=200
        )

    def test_document_duplicates_list_no_permissions(self):
        self._upload_duplicate_document()

        response = self._request_document_duplicates_list_view()
        self.assertEqual(response.status_code, 403)

    def test_document_duplicates_list_with_access(self):
        self._upload_duplicate_document()
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_view
        )

        response = self._request_document_duplicates_list_view()
        self.assertContains(
            response=response, text=self.test_documents[0].label,
            status_code=200
        )
