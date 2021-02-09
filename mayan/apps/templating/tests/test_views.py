from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..permissions import permission_template_sandbox

from .mixins import DocumentTemplateSandboxViewTestMixin


class DocumentTemplateSandboxViewTestCase(
    DocumentTemplateSandboxViewTestMixin, GenericDocumentViewTestCase
):
    def test_document_template_sanbox_get_view_no_permission(self):
        response = self._request_document_template_sandbox_get_view()
        self.assertEqual(response.status_code, 404)

    def test_document_template_sanbox_get_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_template_sandbox
        )

        response = self._request_document_template_sandbox_get_view()
        self.assertEqual(response.status_code, 200)

    def test_document_template_sanbox_post_view_no_permission(self):
        response = self._request_document_template_sandbox_post_view()
        self.assertEqual(response.status_code, 404)

    def test_document_template_sanbox_post_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_template_sandbox
        )

        response = self._request_document_template_sandbox_post_view()
        self.assertEqual(response.status_code, 302)
