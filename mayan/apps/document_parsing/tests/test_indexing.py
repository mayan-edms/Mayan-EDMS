from mayan.apps.documents.tests.literals import TEST_FILE_HYBRID_PDF_FILENAME
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.document_indexing.models import (
    IndexInstanceNode, IndexTemplate
)
from mayan.apps.document_indexing.tests.literals import TEST_INDEX_TEMPLATE_LABEL
from mayan.apps.testing.tests.base import BaseTestCase

from .literals import TEST_PARSING_INDEX_NODE_TEMPLATE


class DocumentFileParsingIndexingTestCase(DocumentTestMixin, BaseTestCase):
    _test_document_filename = TEST_FILE_HYBRID_PDF_FILENAME
    auto_upload_test_document = False

    def test_parsing_indexing(self):
        self._test_index_template = IndexTemplate.objects.create(
            label=TEST_INDEX_TEMPLATE_LABEL
        )

        self._test_index_template.document_types.add(self._test_document_type)

        root = self._test_index_template.index_template_root_node
        self._test_index_template.index_template_nodes.create(
            parent=root, expression=TEST_PARSING_INDEX_NODE_TEMPLATE,
            link_documents=True
        )

        self._upload_test_document()
        self._test_document_file.submit_for_parsing()

        self.assertTrue(
            self._test_document in IndexInstanceNode.objects.get(
                value='sample'
            ).documents.all()
        )
