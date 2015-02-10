from __future__ import unicode_literals

from django.core.files.base import File
from django.test import TestCase

from documents.models import Document, DocumentType
from documents.tests import TEST_SMALL_DOCUMENT_PATH, TEST_DOCUMENT_TYPE
from metadata.models import MetadataType, DocumentTypeMetadataType

from .models import Index, IndexInstanceNode, IndexTemplateNode


class IndexTestCase(TestCase):
    def setUp(self):
        self.document_type = DocumentType.objects.create(name=TEST_DOCUMENT_TYPE)

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = Document.objects.new_document(file_object=File(file_object), document_type=self.document_type)[0].document

    def test_indexing(self):
        metadata_type = MetadataType.objects.create(name='test', title='test')
        DocumentTypeMetadataType.objects.create(document_type=self.document_type, metadata_type=metadata_type)

        # Create empty index
        index = Index.objects.create(name='test', title='test')
        self.failUnlessEqual(list(Index.objects.all()), [index])

        # Add our document type to the new index
        index.document_types.add(self.document_type)
        self.failUnlessEqual(list(index.document_types.all()), [self.document_type])

        # Create simple index template
        root = index.template_root
        index.node_templates.create(parent=root, expression='document.metadata_value_of.test', link_documents=True)
        self.failUnlessEqual(list(IndexTemplateNode.objects.values_list('expression', flat=True)), ['', 'document.metadata_value_of.test'])

        # Add document metadata value to trigger index node instance creation
        self.document.metadata.create(metadata_type=metadata_type, value='0001')
        self.failUnlessEqual(list(IndexInstanceNode.objects.values_list('value', flat=True)), ['', '0001'])

        # Check that document is in instance node
        instance_node = IndexInstanceNode.objects.get(value='0001')
        self.failUnlessEqual(list(instance_node.documents.all()), [self.document])

        # Change document metadata value to trigger index node instance update
        document_metadata = self.document.metadata.get(metadata_type=metadata_type)
        document_metadata.value = '0002'
        document_metadata.save()
        self.failUnlessEqual(list(IndexInstanceNode.objects.values_list('value', flat=True)), ['', '0002'])

        # Check that document is in new instance node
        instance_node = IndexInstanceNode.objects.get(value='0002')
        self.failUnlessEqual(list(instance_node.documents.all()), [self.document])

        # Check node instance is destoyed when no metadata is available
        self.document.metadata.get(metadata_type=metadata_type).delete()
        self.failUnlessEqual(list(IndexInstanceNode.objects.values_list('value', flat=True)), [''])

        # Add document metadata value again to trigger index node instance creation
        self.document.metadata.create(metadata_type=metadata_type, value='0003')
        self.failUnlessEqual(list(IndexInstanceNode.objects.values_list('value', flat=True)), ['', '0003'])

        # Check node instance is destroyed when no documents are contained
        self.document.delete()
        self.failUnlessEqual(list(IndexInstanceNode.objects.values_list('value', flat=True)), [''])
