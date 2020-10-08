from ..models import DocumentVersion
from ..permissions import (
    permission_document_version_edit, permission_document_version_view,
)

from .base import GenericDocumentViewTestCase
#from .literals import (
#    TEST_DOCUMENT_TYPE_2_LABEL, TEST_SMALL_DOCUMENT_FILENAME
#)
from .mixins.document_version_mixins import DocumentVersionViewTestMixin



class DocumentVersionViewTestCase(
    DocumentVersionViewTestMixin, GenericDocumentViewTestCase
):
    def test_document_version_edit_view_no_permission(self):
        document_version_comment = self.test_document_version.comment

        response = self._request_test_document_version_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_document_version.refresh_from_db()
        self.assertEqual(
            self.test_document_version.comment,
            document_version_comment
        )

    def test_document_version_edit_view_with_access(self):
        self.grant_access(
            obj=self.test_document_version,
            permission=permission_document_version_edit
        )

        document_version_comment = self.test_document_version.comment

        response = self._request_test_document_version_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_document_version.refresh_from_db()
        self.assertNotEqual(
            self.test_document_version.comment,
            document_version_comment
        )

    def test_document_version_list_view_no_permission(self):
        response = self._request_test_document_version_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_version_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_view
        )

        response = self._request_test_document_version_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=str(self.test_document_version)
        )

    def test_document_version_preview_view_no_permission(self):
        response = self._request_test_document_version_preview_view()
        self.assertEqual(response.status_code, 404)

    def test_document_version_preview_view_with_access(self):
        self.grant_access(
            obj=self.test_document_version,
            permission=permission_document_version_view
        )

        response = self._request_test_document_version_preview_view()
        self.assertContains(
            response=response, status_code=200,
            text=str(self.test_document_version)
        )
