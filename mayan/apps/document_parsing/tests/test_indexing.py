from mayan.apps.documents.tests.literals import TEST_HYBRID_DOCUMENT
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.document_indexing.models import (
    IndexInstanceNode, IndexTemplate
)
from mayan.apps.document_indexing.tests.literals import TEST_INDEX_TEMPLATE_LABEL
from mayan.apps.testing.tests.base import BaseTransactionTestCase

from .literals import TEST_PARSING_INDEX_NODE_TEMPLATE


class DocumentFileParsingIndexingTestCase(
    DocumentTestMixin, BaseTransactionTestCase
):
    auto_upload_test_document = False
    test_document_filename = TEST_HYBRID_DOCUMENT

    def test_parsing_indexing(self):
        self.test_index_template = IndexTemplate.objects.create(
            label=TEST_INDEX_TEMPLATE_LABEL
        )

        self.test_index_template.document_types.add(self.test_document_type)

        root = self.test_index_template.template_root
        self.test_index_template.node_templates.create(
            parent=root, expression=TEST_PARSING_INDEX_NODE_TEMPLATE,
            link_documents=True
        )

        self._upload_test_document()
        self.test_document_file.submit_for_parsing()

        self.assertTrue(
            self.test_document in IndexInstanceNode.objects.get(
                value='sample'
            ).documents.all()
        )
