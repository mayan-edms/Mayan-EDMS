from __future__ import unicode_literals

from mayan.apps.common.tests import BaseTestCase
from mayan.apps.documents.tests import DocumentTestMixin, TEST_HYBRID_DOCUMENT
from mayan.apps.document_indexing.models import Index, IndexInstanceNode
from mayan.apps.document_indexing.tests.literals import TEST_INDEX_LABEL

from .literals import TEST_PARSING_INDEX_NODE_TEMPLATE


class ParsingIndexingTestCase(DocumentTestMixin, BaseTestCase):
    auto_upload_document = False
    test_document_filename = TEST_HYBRID_DOCUMENT

    def test_parsing_indexing(self):
        index = Index.objects.create(label=TEST_INDEX_LABEL)

        index.document_types.add(self.test_document_type)

        root = index.template_root
        index.node_templates.create(
            parent=root, expression=TEST_PARSING_INDEX_NODE_TEMPLATE,
            link_documents=True
        )

        self.upload_document()
        self.test_document.submit_for_parsing()

        self.assertTrue(
            self.test_document in IndexInstanceNode.objects.get(
                value='sample'
            ).documents.all()
        )
