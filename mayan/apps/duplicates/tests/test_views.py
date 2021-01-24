from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from .mixins import (
    DuplicatedDocumentTestMixin, DuplicatedDocumentViewTestMixin
)


class DocumentsDuplicateListViewsTestCase(
    DuplicatedDocumentTestMixin, DuplicatedDocumentViewTestMixin,
    GenericDocumentViewTestCase
):
    def test_document_duplicates_list_no_permission(self):
        self._upload_duplicate_document()

        response = self._request_test_document_duplicates_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_duplicates_list_with_source_access(self):
        self._upload_duplicate_document()
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_view
        )

        response = self._request_test_document_duplicates_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=self.test_documents[0].label
        )
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_documents[1].label
        )

    def test_document_duplicates_list_with_target_access(self):
        self._upload_duplicate_document()

        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_view
        )

        response = self._request_test_document_duplicates_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_duplicates_list_with_full_access(self):
        self._upload_duplicate_document()
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_view
        )

        response = self._request_test_document_duplicates_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=self.test_documents[0].label
        )
        self.assertContains(
            response=response, status_code=200,
            text=self.test_documents[1].label
        )

    def test_document_duplicates_list_trashed_source_with_full_access(self):
        self._upload_duplicate_document()
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_view
        )

        self.test_documents[0].delete()

        response = self._request_test_document_duplicates_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_duplicates_list_trashed_target_with_full_access(self):
        self._upload_duplicate_document()
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_view
        )

        self.test_documents[1].delete()

        response = self._request_test_document_duplicates_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=self.test_documents[0].label
        )
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_documents[1].label
        )


class DuplicatedDocumentListViewsTestCase(
    DuplicatedDocumentTestMixin, DuplicatedDocumentViewTestMixin,
    GenericDocumentViewTestCase
):
    def test_duplicated_document_list_no_permission(self):
        self._upload_duplicate_document()

        response = self._request_test_duplicated_document_list_view()
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_documents[0].label
        )

    def test_duplicated_document_list_with_source_access(self):
        self._upload_duplicate_document()
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_view
        )

        response = self._request_test_duplicated_document_list_view()
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_documents[0].label
        )
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_documents[1].label
        )

    def test_duplicated_document_list_with_target_access(self):
        self._upload_duplicate_document()
        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_view
        )

        response = self._request_test_duplicated_document_list_view()
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_documents[0].label
        )
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_documents[1].label
        )

    def test_duplicated_document_list_with_full_access(self):
        self._upload_duplicate_document()
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_view
        )

        response = self._request_test_duplicated_document_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=self.test_documents[0].label
        )
        self.assertContains(
            response=response, status_code=200,
            text=self.test_documents[1].label
        )

    def test_duplicated_document_list_trashed_source_with_full_access(self):
        self._upload_duplicate_document()
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_view
        )

        self.test_documents[0].delete()

        response = self._request_test_duplicated_document_list_view()
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_documents[0].label
        )
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_documents[1].label
        )

    def test_duplicated_document_list_trashed_target_with_full_access(self):
        self._upload_duplicate_document()
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_view
        )

        self.test_documents[1].delete()

        response = self._request_test_duplicated_document_list_view()
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_documents[0].label
        )
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_documents[1].label
        )
