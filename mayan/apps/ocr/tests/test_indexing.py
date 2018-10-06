from __future__ import unicode_literals

from django.test import override_settings

from common.tests import BaseTestCase
from documents.tests import DocumentTestMixin
from document_indexing.models import Index, IndexInstanceNode
from document_indexing.tests.literals import TEST_INDEX_LABEL

from .literals import (
    TEST_OCR_INDEX_NODE_TEMPLATE, TEST_OCR_INDEX_NODE_TEMPLATE_LEVEL
)


@override_settings(OCR_AUTO_OCR=False)
class OCRIndexingTestCase(DocumentTestMixin, BaseTestCase):
    auto_upload_document = False

    def test_ocr_indexing(self):
        index = Index.objects.create(label=TEST_INDEX_LABEL)

        index.document_types.add(self.document_type)

        root = index.template_root
        index.node_templates.create(
            parent=root, expression=TEST_OCR_INDEX_NODE_TEMPLATE,
            link_documents=True
        )

        self.document = self.upload_document()
        self.document.submit_for_ocr()

        self.assertTrue(
            self.document in IndexInstanceNode.objects.get(
                value=TEST_OCR_INDEX_NODE_TEMPLATE_LEVEL
            ).documents.all()
        )
