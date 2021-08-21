from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.documents.tests.mixins.document_mixins import DocumentSearchTestMixin
from mayan.apps.documents.permissions import permission_document_view

from .mixins import DocumentVersionOCRTestMixin


class DocumentVersionOCRSearchTestCase(
    DocumentSearchTestMixin, DocumentVersionOCRTestMixin,
    GenericDocumentViewTestCase
):
    def test_document_search_with_access(self):
        self._create_test_document_version_ocr_content()

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self._perform_document_search(
            query={
                'versions__version_pages__ocr_content__content': self.test_document_version_page.ocr_content.content
            }
        )
        self.assertTrue(self.test_document in queryset)
