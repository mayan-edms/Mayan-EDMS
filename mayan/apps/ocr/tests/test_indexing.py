from __future__ import unicode_literals

from mayan.apps.common.tests.base import BaseTestCase
from mayan.apps.documents.tests.mixins import DocumentTestMixin
from mayan.apps.document_indexing.models import Index, IndexInstanceNode
from mayan.apps.document_indexing.tests.literals import TEST_INDEX_LABEL

from .literals import (
    TEST_OCR_INDEX_NODE_TEMPLATE, TEST_OCR_INDEX_NODE_TEMPLATE_LEVEL
)


class OCRIndexingTestCase(DocumentTestMixin, BaseTestCase):
    auto_upload_document = False

    def test_ocr_indexing(self):
        index = Index.objects.create(label=TEST_INDEX_LABEL)

        index.document_types.add(self.test_document_type)

        root = index.template_root
        index.node_templates.create(
            parent=root, expression=TEST_OCR_INDEX_NODE_TEMPLATE,
            link_documents=True
        )

        self.upload_document()
        self.test_document.submit_for_ocr()

        self.assertTrue(
            self.test_document in IndexInstanceNode.objects.get(
                value=TEST_OCR_INDEX_NODE_TEMPLATE_LEVEL
            ).documents.all()
        )
