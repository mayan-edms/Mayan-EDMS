from __future__ import unicode_literals

from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..permissions import permission_template_sandbox


class DocumentTemplateSandboxViewTestMixin(object):
    def _request_document_template_sandbox_view(self):
        return self.get(
            viewname='templating:document_template_sandbox',
            kwargs={'pk': self.test_document.pk}
        )


class DocumentTemplateSandboxViewTestCase(
    DocumentTemplateSandboxViewTestMixin, GenericDocumentViewTestCase
):
    def test_document_template_sanbox_view_no_permissions(self):
        response = self._request_document_template_sandbox_view()
        self.assertEqual(response.status_code, 404)

    def test_document_template_sanbox_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_template_sandbox
        )

        response = self._request_document_template_sandbox_view()
        self.assertEqual(response.status_code, 200)
