from __future__ import unicode_literals

from django.test import override_settings

from common.tests import BaseTestCase
from documents.models import DocumentType
from documents.tests import TEST_SMALL_DOCUMENT_PATH, TEST_DOCUMENT_TYPE
from metadata.models import MetadataType, DocumentTypeMetadataType

from ..models import Index, IndexInstanceNode, IndexTemplateNode

from .literals import (
    TEST_INDEX_LABEL, TEST_INDEX_TEMPLATE_METADATA_EXPRESSION,
    TEST_METADATA_TYPE_LABEL, TEST_METADATA_TYPE_NAME
)


@override_settings(OCR_AUTO_OCR=False)
class IndexTestCase(BaseTestCase):
    def setUp(self):
        super(IndexTestCase, self).setUp()
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=file_object
            )

    def tearDown(self):
        self.document_type.delete()
        super(IndexTestCase, self).tearDown()

    def test_indexing(self):
        metadata_type = MetadataType.objects.create(
            name=TEST_METADATA_TYPE_NAME, label=TEST_METADATA_TYPE_LABEL
        )
        DocumentTypeMetadataType.objects.create(
            document_type=self.document_type, metadata_type=metadata_type
        )

        # Create empty index
        index = Index.objects.create(label=TEST_INDEX_LABEL)

        # Add our document type to the new index
        index.document_types.add(self.document_type)

        # Create simple index template
        root = index.template_root
        index.node_templates.create(
            parent=root, expression=TEST_INDEX_TEMPLATE_METADATA_EXPRESSION,
            link_documents=True
        )

        # Add document metadata value to trigger index node instance creation
        self.document.metadata.create(
            metadata_type=metadata_type, value='0001'
        )
        self.assertEqual(
            list(
                IndexInstanceNode.objects.values_list('value', flat=True)
            ), ['', '0001']
        )

        # Check that document is in instance node
        instance_node = IndexInstanceNode.objects.get(value='0001')
        self.assertQuerysetEqual(
            instance_node.documents.all(), [repr(self.document)]
        )

        # Change document metadata value to trigger index node instance update
        document_metadata = self.document.metadata.get(
            metadata_type=metadata_type
        )
        document_metadata.value = '0002'
        document_metadata.save()
        self.assertEqual(
            list(
                IndexInstanceNode.objects.values_list('value', flat=True)
            ), ['', '0002']
        )

        # Check that document is in new instance node
        instance_node = IndexInstanceNode.objects.get(value='0002')
        self.assertQuerysetEqual(
            instance_node.documents.all(), [repr(self.document)]
        )

        # Check node instance is destoyed when no metadata is available
        self.document.metadata.get(metadata_type=metadata_type).delete()
        self.assertEqual(
            list(
                IndexInstanceNode.objects.values_list('value', flat=True)
            ), ['']
        )

        # Add document metadata value again to trigger index node instance
        # creation
        self.document.metadata.create(
            metadata_type=metadata_type, value='0003'
        )
        self.assertEqual(
            list(
                IndexInstanceNode.objects.values_list('value', flat=True)
            ), ['', '0003']
        )

        # Check node instance is destroyed when no documents are contained
        self.document.delete()

        # Document is in trash, index structure should remain unchanged
        self.assertEqual(
            list(
                IndexInstanceNode.objects.values_list('value', flat=True)
            ), ['', '0003']
        )

        # Document deleted, index structure should update
        self.document.delete()
        self.assertEqual(
            list(
                IndexInstanceNode.objects.values_list('value', flat=True)
            ), ['']
        )

    def test_rebuild_all_indexes(self):
        # Add metadata type and connect to document type
        metadata_type = MetadataType.objects.create(name='test', label='test')
        DocumentTypeMetadataType.objects.create(
            document_type=self.document_type, metadata_type=metadata_type
        )

        # Add document metadata value
        self.document.metadata.create(
            metadata_type=metadata_type, value='0001'
        )

        # Create empty index
        index = Index.objects.create(label='test')
        self.assertEqual(list(Index.objects.all()), [index])

        # Add our document type to the new index
        index.document_types.add(self.document_type)
        self.assertQuerysetEqual(
            index.document_types.all(), [repr(self.document_type)]
        )

        # Create simple index template
        root = index.template_root
        index.node_templates.create(
            parent=root, expression='{{ document.metadata_value_of.test }}',
            link_documents=True
        )
        self.assertEqual(
            list(
                IndexTemplateNode.objects.values_list('expression', flat=True)
            ), ['', '{{ document.metadata_value_of.test }}']
        )

        # There should be no index instances
        self.assertEqual(list(IndexInstanceNode.objects.all()), [])

        # Rebuild all indexes
        Index.objects.rebuild()

        # Check that document is in instance node
        instance_node = IndexInstanceNode.objects.get(value='0001')
        self.assertQuerysetEqual(
            instance_node.documents.all(), [repr(self.document)]
        )
