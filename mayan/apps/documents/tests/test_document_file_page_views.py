from django.utils.encoding import force_text

from ..permissions import (
    permission_document_file_tools, permission_document_file_view
)

from .base import GenericDocumentViewTestCase
from .mixins.document_file_mixins import DocumentFilePageViewTestMixin


class DocumentFilePageViewTestCase(
    DocumentFilePageViewTestMixin, GenericDocumentViewTestCase
):
    def test_document_file_page_count_update_view_no_permission(self):
        self.test_document_file.pages.all().delete()
        page_count = self.test_document_file.pages.count()

        response = self._request_test_document_file_page_count_update_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(self.test_document_file.pages.count(), page_count)

    def test_document_file_page_count_update_view_with_access(self):
        self.test_document_file.pages.all().delete()
        page_count = self.test_document_file.pages.count()

        self.grant_access(
            obj=self.test_document, permission=permission_document_file_tools
        )

        response = self._request_test_document_file_page_count_update_view()
        self.assertEqual(response.status_code, 302)

        self.assertNotEqual(self.test_document_file.pages.count(), page_count)

    def test_trashed_document_file_page_count_update_view_with_access(self):
        self.test_document_file.pages.all().delete()
        page_count = self.test_document_file.pages.count()

        self.grant_access(
            obj=self.test_document, permission=permission_document_file_tools
        )

        self.test_document.delete()

        response = self._request_test_document_file_page_count_update_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(self.test_document_file.pages.count(), page_count)

    def test_document_file_multiple_page_count_update_view_no_permission(self):
        self.test_document_file.pages.all().delete()
        page_count = self.test_document_file.pages.count()

        response = self._request_test_document_file_multiple_page_count_update_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(self.test_document_file.pages.count(), page_count)

    def test_document_file_multiple_page_count_update_view_with_access(self):
        self.test_document_file.pages.all().delete()
        page_count = self.test_document_file.pages.count()

        self.grant_access(
            obj=self.test_document_file,
            permission=permission_document_file_tools
        )

        response = self._request_test_document_file_multiple_page_count_update_view()
        self.assertEqual(response.status_code, 302)

        self.assertNotEqual(self.test_document_file.pages.count(), page_count)

    def test_trashed_document_file_multiple_page_count_update_view_with_access(self):
        self.test_document_file.pages.all().delete()
        page_count = self.test_document_file.pages.count()

        self.grant_access(
            obj=self.test_document_file,
            permission=permission_document_file_tools
        )

        self.test_document.delete()

        response = self._request_test_document_file_multiple_page_count_update_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(self.test_document_file.pages.count(), page_count)

    def test_document_file_page_list_view_no_permission(self):
        response = self._request_test_document_file_page_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_page_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        response = self._request_test_document_file_page_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=str(self.test_document_file)
        )

    def test_trashed_document_file_page_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self.test_document.delete()

        response = self._request_test_document_file_page_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_page_rotate_left_view_no_permission(self):
        response = self._request_test_document_file_page_rotate_left_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_page_rotate_left_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        response = self._request_test_document_file_page_rotate_left_view()
        self.assertEqual(response.status_code, 302)

    def test_trashed_document_file_page_rotate_left_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self.test_document.delete()

        response = self._request_test_document_file_page_rotate_left_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_page_rotate_right_view_no_permission(self):
        response = self._request_test_document_file_page_rotate_right_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_page_rotate_right_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        response = self._request_test_document_file_page_rotate_right_view()
        self.assertEqual(response.status_code, 302)

    def test_trashed_document_file_page_rotate_right_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self.test_document.delete()

        response = self._request_test_document_file_page_rotate_right_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_page_view_no_permission(self):
        response = self._request_test_document_file_page_view(
            document_file_page=self.test_document_file.pages.first()
        )
        self.assertEqual(response.status_code, 404)

    def test_document_file_page_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        response = self._request_test_document_file_page_view(
            document_file_page=self.test_document_file.pages.first()
        )
        self.assertContains(
            response=response, status_code=200, text=force_text(
                s=self.test_document_file.pages.first()
            )
        )

    def test_trashed_document_file_page_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self.test_document.delete()

        response = self._request_test_document_file_page_view(
            document_file_page=self.test_document_file.pages.first()
        )
        self.assertEqual(response.status_code, 404)

    def test_document_file_page_zoom_in_view_no_permission(self):
        response = self._request_test_document_file_page_zoom_in_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_page_zoom_in_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        response = self._request_test_document_file_page_zoom_in_view()
        self.assertEqual(response.status_code, 302)

    def test_trashed_document_file_page_zoom_in_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self.test_document.delete()

        response = self._request_test_document_file_page_zoom_in_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_page_zoom_out_view_no_permission(self):
        response = self._request_test_document_file_page_zoom_out_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_page_zoom_out_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        response = self._request_test_document_file_page_zoom_out_view()
        self.assertEqual(response.status_code, 302)

    def test_trashed_document_file_page_zoom_out_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self.test_document.delete()

        response = self._request_test_document_file_page_zoom_out_view()
        self.assertEqual(response.status_code, 404)
