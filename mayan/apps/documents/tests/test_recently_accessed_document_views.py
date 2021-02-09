from ..permissions import permission_document_view

from .base import GenericDocumentViewTestCase
from .mixins.recently_accessed_document_mixins import RecentlyAccessedDocumentViewTestMixin


class RecentlyAccessedDocumentViewTestCase(
    RecentlyAccessedDocumentViewTestMixin, GenericDocumentViewTestCase
):
    def test_recently_accessed_document_list_view_no_permission(self):
        self.test_document.add_as_recent_document_for_user(
            user=self._test_case_user
        )

        response = self._request_test_recently_accessed_document_list_view()
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )

    def test_recently_accessed_document_list_view_with_access(self):
        self.test_document.add_as_recent_document_for_user(
            user=self._test_case_user
        )

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_recently_accessed_document_list_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )

    def test_trashed_recently_accessed_document_list_view_with_access(self):
        self.test_document.add_as_recent_document_for_user(
            user=self._test_case_user
        )
        self.test_document.delete()

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_recently_accessed_document_list_view()
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )
