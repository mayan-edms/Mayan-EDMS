from __future__ import unicode_literals

from mayan.apps.common.tests import BaseTestCase
from mayan.apps.document_indexing.models import Index, IndexInstanceNode
from mayan.apps.document_indexing.tests.literals import TEST_INDEX_LABEL
from mayan.apps.documents.tests import DocumentTestMixin

from .literals import (
    TEST_FILE_METADATA_INDEX_NODE_TEMPLATE, TEST_FILE_METADATA_VALUE
)


class IndexingTestCase(DocumentTestMixin, BaseTestCase):
    auto_upload_document = False

    def test_indexing(self):
        index = Index.objects.create(label=TEST_INDEX_LABEL)

        index.document_types.add(self.document_type)

        root = index.template_root
        index.node_templates.create(
            parent=root, expression=TEST_FILE_METADATA_INDEX_NODE_TEMPLATE,
            link_documents=True
        )
        self.document = self.upload_document()
        self.document.submit_for_file_metadata_processing()
        self.assertTrue(
            self.document in IndexInstanceNode.objects.get(
                value=TEST_FILE_METADATA_VALUE
            ).documents.all()
        )
