from django.utils.encoding import force_text

from ..permissions import (
    permission_document_edit, permission_document_view
)

from .base import GenericDocumentViewTestCase
from .mixins.document_file_mixins import (
    DocumentFilePageDisableViewTestMixin, DocumentFilePageViewTestMixin
)


class DocumentFilePageViewTestCase(
    DocumentFilePageViewTestMixin, GenericDocumentViewTestCase
):
    def test_document_file_page_list_view_no_permission(self):
        response = self._request_test_document_file_page_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_page_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_document_file_page_list_view()
        self.assertContains(
            response=response, status_code=200, text=self.test_document.label
        )

    def test_document_file_page_rotate_left_view_no_permission(self):
        response = self._request_test_document_file_page_rotate_left_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_page_rotate_left_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_document_file_page_rotate_left_view()
        self.assertEqual(response.status_code, 302)

    def test_document_file_page_rotate_right_view_no_permission(self):
        response = self._request_test_document_file_page_rotate_right_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_page_rotate_right_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_document_file_page_rotate_right_view()
        self.assertEqual(response.status_code, 302)

    def test_document_file_page_view_no_permission(self):
        response = self._request_test_document_file_page_view(
            document_file_page=self.test_document.pages.first()
        )
        self.assertEqual(response.status_code, 404)

    def test_document_file_page_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_document_file_page_view(
            document_file_page=self.test_document.pages.first()
        )
        self.assertContains(
            response=response, status_code=200, text=force_text(
                self.test_document.pages.first()
            )
        )

    def test_document_file_page_zoom_in_view_no_permission(self):
        response = self._request_test_document_file_page_zoom_in_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_page_zoom_in_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_document_file_page_zoom_in_view()
        self.assertEqual(response.status_code, 302)

    def test_document_file_page_zoom_out_view_no_permission(self):
        response = self._request_test_document_file_page_zoom_out_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_page_zoom_out_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_document_file_page_zoom_out_view()
        self.assertEqual(response.status_code, 302)
