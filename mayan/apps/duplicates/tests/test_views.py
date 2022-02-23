from mayan.apps.documents.permissions import (
    permission_document_tools, permission_document_view
)
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..classes import DuplicateBackend
from ..models import DuplicateBackendEntry

from .mixins import (
    DuplicatedDocumentTestMixin, DuplicatedDocumentToolViewTestMixin,
    DuplicatedDocumentViewTestMixin
)
from .mocks import TestDuplicateBackend


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
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        DuplicateBackend.register(klass=TestDuplicateBackend)

    def _request_duplicate_backend_list_view(self):
        return self.get(viewname='duplicates:backend_list')

    def _request_duplicate_backend_detail_view(self):
        return self.get(
            viewname='duplicates:backend_detail', kwargs={
                'backend_id': TestDuplicateBackend.get_model_instance().pk
            }
        )

    def test_duplicate_backend_list_view(self):
        response = self._request_duplicate_backend_list_view()
        self.assertContains(
            response=response, text=TestDuplicateBackend.label,
            status_code=200
        )

    def test_duplicate_backend_detail_view_no_permission(self):
        self._create_test_document_stub()
        self._create_test_document_stub()

        response = self._request_duplicate_backend_detail_view()
        self.assertNotContains(
            response=response, text=self.test_documents[0].label,
            status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_documents[1].label,
            status_code=200
        )

    def test_duplicate_backend_detail_view_with_access(self):
        self._create_test_document_stub()
        self._create_test_document_stub()

        self.grant_access(
            obj=self.test_documents[0], permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_documents[1], permission=permission_document_view
        )

        response = self._request_duplicate_backend_detail_view()
        self.assertContains(
            response=response, text=self.test_documents[0].label,
            status_code=200
        )
        self.assertContains(
            response=response, text=self.test_documents[1].label,
            status_code=200
        )

    def test_trashed_document_duplicate_backend_detail_view_with_access(self):
        self._create_test_document_stub()
        self._create_test_document_stub()

        self.test_documents[0].delete()

        self.grant_access(
            obj=self.test_documents[0], permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_documents[1], permission=permission_document_view
        )

        response = self._request_duplicate_backend_detail_view()
        self.assertNotContains(
            response=response, text=self.test_documents[0].label,
            status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_documents[1].label,
            status_code=200
        )

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


class DuplicatedDocumentToolsViewsTestCase(
    DuplicatedDocumentTestMixin, DuplicatedDocumentToolViewTestMixin,
    GenericDocumentViewTestCase
):
    def test_duplicated_document_scan_no_permission(self):
        self._upload_duplicate_document()
        DuplicateBackendEntry.objects.all().delete()

        response = self._request_duplicated_document_scan_view()
        self.assertEqual(response.status_code, 403)

        self.assertFalse(
            self.test_documents[1] in DuplicateBackendEntry.objects.get_duplicates_of(
                document=self.test_documents[0]
            )
        )

    def test_duplicated_document_scan_with_permission(self):
        self._upload_duplicate_document()
        DuplicateBackendEntry.objects.all().delete()

        self.grant_permission(permission=permission_document_tools)

        response = self._request_duplicated_document_scan_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self.test_documents[1] in DuplicateBackendEntry.objects.get_duplicates_of(
                document=self.test_documents[0]
            )
        )
