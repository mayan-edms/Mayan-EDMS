from __future__ import unicode_literals

from django.test import override_settings

from common.tests import BaseTestCase
from documents.tests import DocumentTestMixin, TEST_HYBRID_DOCUMENT

from document_indexing.models import Index, IndexInstanceNode
from document_indexing.tests.literals import TEST_INDEX_LABEL

from .literals import TEST_PARSING_INDEX_NODE_TEMPLATE


@override_settings(DOCUMENT_PARSING_AUTO_PARSING=False)
@override_settings(OCR_AUTO_OCR=False)
class ParsingIndexingTestCase(DocumentTestMixin, BaseTestCase):
    auto_upload_document = False
    test_document_filename = TEST_HYBRID_DOCUMENT

    def test_parsing_indexing(self):
        index = Index.objects.create(label=TEST_INDEX_LABEL)

        index.document_types.add(self.document_type)

        root = index.template_root
        index.node_templates.create(
            parent=root, expression=TEST_PARSING_INDEX_NODE_TEMPLATE,
            link_documents=True
        )

        self.document = self.upload_document()
        self.document.submit_for_parsing()

        self.assertTrue(
            self.document in IndexInstanceNode.objects.get(
                value='sample'
            ).documents.all()
        )
