from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.document_indexing.models.index_instance_models import IndexInstanceNode
from mayan.apps.document_indexing.tests.mixins import IndexTemplateTestMixin

from .literals import (
    TEST_METADATA_INDEX_NODE_TEMPLATE, TEST_METADATA_VALUE,
    TEST_METADATA_TYPE_LABEL_EDITED, TEST_METADATA_VALUE_EDITED
)
from .mixins import DocumentMetadataMixin, MetadataTypeTestMixin


class MetadataIndexingTestCase(
    IndexTemplateTestMixin, DocumentMetadataMixin, MetadataTypeTestMixin,
    GenericDocumentTestCase
):
    _test_index_template_node_expression = TEST_METADATA_INDEX_NODE_TEMPLATE
    auto_create_test_document_stub = True
    auto_create_test_metadata_type = True
    auto_upload_test_document = False

    def test_indexing_no_metadata(self):
        value = '{}-{}'.format(
            self._test_metadata_type.label, TEST_METADATA_VALUE
        )

        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=self._test_document, value=value
            ).exists()
        )

    def test_indexing_metadata_add(self):
        self._create_test_document_metadata()
        value = '{}-{}'.format(
            self._test_metadata_type.label,
            self._test_document_metadata.value
        )

        self.assertTrue(
            IndexInstanceNode.objects.filter(
                documents=self._test_document, value=value
            ).exists()
        )

    def test_indexing_metadata_edit(self):
        self._create_test_document_metadata()
        value = '{}-{}'.format(
            self._test_metadata_type.label,
            self._test_document_metadata.value
        )

        self._test_document_metadata.value = TEST_METADATA_VALUE_EDITED
        self._test_document_metadata.save()
        value_edited = '{}-{}'.format(
            self._test_metadata_type.label,
            self._test_document_metadata.value
        )

        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=self._test_document, value=value
            ).exists()
        )
        self.assertTrue(
            IndexInstanceNode.objects.filter(
                documents=self._test_document, value=value_edited
            ).exists()
        )

    def test_indexing_metadata_remove(self):
        self._create_test_document_metadata()
        value = '{}-{}'.format(
            self._test_metadata_type.label,
            self._test_document_metadata.value
        )

        self._test_document_metadata.delete()

        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=self._test_document, value=value
            ).exists()
        )

    def test_indexing_metadata_type_delete(self):
        self._create_test_document_metadata()
        value = '{}-{}'.format(
            self._test_metadata_type.label,
            self._test_document_metadata.value
        )

        self._test_metadata_type.delete()

        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=self._test_document, value=value
            ).exists()
        )

    def test_indexing_metadata_type_edit(self):
        self._create_test_document_metadata()
        value = '{}-{}'.format(
            self._test_metadata_type.label,
            self._test_document_metadata.value
        )

        self._test_metadata_type.label = TEST_METADATA_TYPE_LABEL_EDITED
        self._test_metadata_type.save()
        value_edited = '{}-{}'.format(
            self._test_metadata_type.label,
            self._test_document_metadata.value
        )

        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=self._test_document, value=value
            ).exists()
        )
        self.assertTrue(
            IndexInstanceNode.objects.filter(
                documents=self._test_document, value=value_edited
            ).exists()
        )
