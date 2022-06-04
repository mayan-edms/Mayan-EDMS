from mayan.apps.document_indexing.models import IndexInstanceNode
from mayan.apps.document_indexing.tests.mixins import IndexTemplateTestMixin
from mayan.apps.documents.tests.base import GenericDocumentTestCase

from .literals import (
    TEST_FILE_METADATA_INDEX_NODE_TEMPLATE, TEST_FILE_METADATA_VALUE
)


class IndexingTestCase(IndexTemplateTestMixin, GenericDocumentTestCase):
    _test_index_template_node_expression = TEST_FILE_METADATA_INDEX_NODE_TEMPLATE
    auto_upload_test_document = False

    def test_indexing(self):
        self._upload_test_document()

        self._test_document.submit_for_file_metadata_processing()

        self.assertTrue(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=TEST_FILE_METADATA_VALUE
            ).exists()
        )
