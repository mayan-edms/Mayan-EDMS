from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.documents.tests.mixins import DocumentLinkTestMixin

from ..links import link_document_parsing_errors_list
from ..permissions import permission_parse_document


class DocumentContentLinkTestCase(
    DocumentLinkTestMixin, GenericDocumentViewTestCase
):
    def test_document_parsing_errors_list_link_no_permission(self):
        resolved_link = self._resolve_test_document_link(
            test_link=link_document_parsing_errors_list
        )
        self.assertEqual(resolved_link, None)

    def test_document_parsing_errors_list_link_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_parse_document
        )
        resolved_link = self._resolve_test_document_link(
            test_link=link_document_parsing_errors_list
        )
        self.assertNotEqual(resolved_link, None)
