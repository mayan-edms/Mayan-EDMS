from __future__ import absolute_import

from json import loads
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import File
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from documents.models import Document, DocumentType
from documents.tests import (TEST_SMALL_DOCUMENT_PATH, TEST_DOCUMENT_DESCRIPTION,
                             TEST_DOCUMENT_TYPE)
from metadata.models import (MetadataType, DocumentMetadata,
                             DocumentTypeMetadataType)
from .models import Index, IndexInstanceNode, IndexTemplateNode


class IndexTestCase(TestCase):
    def setUp(self):
        self.document_type = DocumentType.objects.create(name=TEST_DOCUMENT_DESCRIPTION)

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
        self.failUnlessEqual(list(IndexTemplateNode.objects.values_list('expression', flat=True)), [u'', u'document.metadata_value_of.test'])

        # Add document metadata value to trigger index node instance creation
        self.document.metadata.create(metadata_type=metadata_type, value='0001')
        self.failUnlessEqual(list(IndexInstanceNode.objects.values_list('value', flat=True)), [u'', u'0001'])
