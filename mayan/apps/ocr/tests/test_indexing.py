from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.documents.tests.mixins.document_version_mixins import DocumentVersionTestMixin
from mayan.apps.document_indexing.models.index_instance_models import IndexInstanceNode
from mayan.apps.document_indexing.tests.mixins import IndexTemplateTestMixin

from .literals import (
    TEST_DOCUMENT_VERSION_OCR_INDEX_NODE_TEMPLATE,
    TEST_DOCUMENT_VERSION_PAGE_OCR_CONTENT_UPDATED
)
from .mixins import DocumentVersionOCRTestMixin


class DocumentVersionOCRIndexingTestCase(
    DocumentVersionOCRTestMixin, DocumentVersionTestMixin,
    IndexTemplateTestMixin, GenericDocumentTestCase
):
    _test_index_template_node_expression = TEST_DOCUMENT_VERSION_OCR_INDEX_NODE_TEMPLATE
    auto_create_test_document_stub = True
    auto_create_test_document_version = True
    auto_upload_test_document = False

    def test_indexing_not_document_version_ocr(self):
        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=self._test_document
            ).exists()
        )

    def test_indexing_document_version_ocr_delete(self):
        self._create_test_document_version_ocr_content()
        value = ' '.join(self._test_document.version_active.ocr_content())

        self._do_test_document_version_ocr_content_delete()

        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=value
            ).exists()
        )

    def test_indexing_document_version_ocr_edit(self):
        self._create_test_document_version_ocr_content()
        value = ' '.join(self._test_document.version_active.ocr_content())

        self._test_document_version_page.ocr_content.content = TEST_DOCUMENT_VERSION_PAGE_OCR_CONTENT_UPDATED
        self._test_document_version_page.ocr_content.save()
        value_edited = ' '.join(self._test_document.version_active.ocr_content())

        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=value
            ).exists()
        )
        self.assertTrue(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=value_edited
            ).exists()
        )

    def test_indexing_document_version_ocr_finished(self):
        self._create_test_document_version_ocr_content()
        value = ' '.join(self._test_document.version_active.ocr_content())

        self.assertTrue(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=value
            ).exists()
        )
