from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.documents.tests.mixins.document_file_mixins import DocumentFileLinkTestMixin

from ..links import link_document_file_parsing_errors_list
from ..permissions import permission_document_file_parse


class DocumentFileContentLinkTestCase(
    DocumentFileLinkTestMixin, GenericDocumentViewTestCase
):
    def test_document_file_parsing_errors_list_link_no_permission(self):
        resolved_link = self._resolve_test_document_file_link(
            test_link=link_document_file_parsing_errors_list
        )
        self.assertEqual(resolved_link, None)

    def test_document_file_parsing_errors_list_link_with_access(self):
        self.grant_access(
            obj=self.test_document_file,
            permission=permission_document_file_parse
        )
        resolved_link = self._resolve_test_document_file_link(
            test_link=link_document_file_parsing_errors_list
        )
        self.assertNotEqual(resolved_link, None)
