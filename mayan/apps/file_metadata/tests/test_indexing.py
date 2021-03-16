from mayan.apps.document_indexing.models import (
    IndexInstanceNode, IndexTemplate
)
from mayan.apps.document_indexing.tests.literals import TEST_INDEX_TEMPLATE_LABEL
from mayan.apps.documents.tests.base import DocumentTestMixin
from mayan.apps.testing.tests.base import BaseTransactionTestCase

from .literals import (
    TEST_FILE_METADATA_INDEX_NODE_TEMPLATE, TEST_FILE_METADATA_VALUE
)


class IndexingTestCase(DocumentTestMixin, BaseTransactionTestCase):
    auto_upload_test_document = False

    def test_indexing(self):
        self.test_index_template = IndexTemplate.objects.create(
            label=TEST_INDEX_TEMPLATE_LABEL
        )
        self.test_index_template.document_types.add(self.test_document_type)

        root = self.test_index_template.template_root
        self.test_index_template.node_templates.create(
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
