from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.document_indexing.models import IndexInstanceNode
from mayan.apps.document_indexing.tests.mixins import IndexTemplateTestMixin

from .literals import (
    TEST_TAG_INDEX_HAS_TAG, TEST_TAG_INDEX_NO_TAG,
    TEST_TAG_INDEX_NODE_TEMPLATE
)
from .mixins import TagTestMixin


class TagSignalIndexingTestCase(
    IndexTemplateTestMixin, TagTestMixin, GenericDocumentTestCase
):
    _test_index_template_node_expression = TEST_TAG_INDEX_NODE_TEMPLATE
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_tag()
        self._create_test_document_stub()

    def test_tag_indexing_not_tag(self):
        self.assertTrue(
            self.test_document in IndexInstanceNode.objects.get(
                value=TEST_TAG_INDEX_NO_TAG
            ).documents.all()
        )

    def test_tag_indexing_tag_attach(self):
        self.test_tag.documents.add(self.test_document)

        self.assertTrue(
            self.test_document in IndexInstanceNode.objects.get(
                value=TEST_TAG_INDEX_HAS_TAG
            ).documents.all()
        )

    def test_tag_indexing_tag_remove(self):
        self.test_tag.documents.add(self.test_document)
        self.test_tag.delete()

        self.assertTrue(
            self.test_document in IndexInstanceNode.objects.get(
                value=TEST_TAG_INDEX_NO_TAG
            ).documents.all()
        )
