from mayan.apps.tests.tests.base import BaseTransactionTestCase
from mayan.apps.document_indexing.models import Index, IndexInstanceNode
from mayan.apps.document_indexing.tests.literals import TEST_INDEX_LABEL
from mayan.apps.documents.tests.base import DocumentTestMixin

from .literals import (
    TEST_FILE_METADATA_INDEX_NODE_TEMPLATE, TEST_FILE_METADATA_VALUE
)


class IndexingTestCase(DocumentTestMixin, BaseTransactionTestCase):
    auto_upload_test_document = False

    def test_indexing(self):
        self.test_index = Index.objects.create(label=TEST_INDEX_LABEL)
        self.test_index.document_types.add(self.test_document_type)

        root = self.test_index.template_root
        self.test_index.node_templates.create(
            parent=root, expression=TEST_FILE_METADATA_INDEX_NODE_TEMPLATE,
            link_documents=True
        )

        self._upload_test_document()

        self.test_document.submit_for_file_metadata_processing()

        self.assertTrue(
            self.test_document in IndexInstanceNode.objects.get(
                value=TEST_FILE_METADATA_VALUE
            ).documents.all()
        )
