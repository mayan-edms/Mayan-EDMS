from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..links import link_document_ocr_content_delete
from ..permissions import permission_ocr_document

from .mixins import DocumentOCRLinkTestMixin


class DocumentOCRLinkTestCase(
    DocumentOCRLinkTestMixin, GenericDocumentViewTestCase
):
    def test_link_document_ocr_content_delete_no_permission(self):
        resolved_link = self._resolve_test_document_link(
            test_link=link_document_ocr_content_delete
        )
        self.assertEqual(resolved_link, None)

    def test_link_document_ocr_content_delete_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_ocr_document
        )
        resolved_link = self._resolve_test_document_link(
            test_link=link_document_ocr_content_delete
        )
        self.assertNotEqual(resolved_link, None)
