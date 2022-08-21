from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.document_indexing.models.index_instance_models import IndexInstanceNode
from mayan.apps.document_indexing.tests.mixins import IndexTemplateTestMixin

from .literals import TEST_TAG_LABEL_EDITED, TEST_TAG_INDEX_NODE_TEMPLATE
from .mixins import TagTestMixin


class TagIndexingTestCase(
    IndexTemplateTestMixin, TagTestMixin, GenericDocumentTestCase
):
    _test_index_template_node_expression = TEST_TAG_INDEX_NODE_TEMPLATE
    auto_create_test_document_stub = True
    auto_create_test_tag = True
    auto_upload_test_document = False

    def test_indexing_not_tag(self):
        value = self._test_tag.label

        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=value
            ).exists()
        )

    def test_indexing_tag_attach(self):
        self._test_tag.attach_to(document=self._test_document)

        value = self._test_tag.label

        self.assertTrue(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=value
            ).exists()
        )

    def test_indexing_tag_delete(self):
        self._test_tag.attach_to(document=self._test_document)

        value = self._test_tag.label

        self._test_tag.delete()

        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=value
            ).exists()
        )

    def test_indexing_tag_edit(self):
        self._test_tag.attach_to(document=self._test_document)
        value = self._test_tag.label

        self._test_tag.label = TEST_TAG_LABEL_EDITED
        self._test_tag.save()
        value_edited = self._test_tag.label

        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=value
            ).exists()
        )
        self.assertTrue(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=value_edited
            ).exists()
        )

    def test_indexing_tag_remove(self):
        self._test_tag.attach_to(document=self._test_document)
        self._test_tag.remove_from(document=self._test_document)
        value = self._test_tag.label

        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=value
            ).exists()
        )
