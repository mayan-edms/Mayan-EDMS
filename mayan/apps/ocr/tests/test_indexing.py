from mayan.apps.tests.tests.base import BaseTransactionTestCase
from mayan.apps.documents.tests.mixins import DocumentTestMixin
from mayan.apps.document_indexing.models import Index, IndexInstanceNode
from mayan.apps.document_indexing.tests.literals import TEST_INDEX_LABEL

from .literals import (
    TEST_OCR_INDEX_NODE_TEMPLATE, TEST_OCR_INDEX_NODE_TEMPLATE_LEVEL
)


class OCRIndexingTestCase(DocumentTestMixin, BaseTransactionTestCase):
    auto_upload_test_document = False

    def test_ocr_indexing(self):
        self.test_index = Index.objects.create(label=TEST_INDEX_LABEL)

        self.test_index.document_types.add(self.test_document_type)

        root = self.test_index.template_root
        self.test_index.node_templates.create(
            parent=root, expression=TEST_OCR_INDEX_NODE_TEMPLATE,
            link_documents=True
        )

        self._upload_test_document()
        self.test_document.submit_for_ocr()

        self.assertTrue(
            self.test_document in IndexInstanceNode.objects.get(
                value=TEST_OCR_INDEX_NODE_TEMPLATE_LEVEL
            ).documents.all()
        )
