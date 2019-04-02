from __future__ import unicode_literals

from django.test import override_settings
from django.utils.encoding import force_text

from common.tests import BaseTestCase
from documents.tests import DocumentTestMixin, TEST_SMALL_DOCUMENT_PATH
from documents.tests.literals import (
    TEST_DOCUMENT_DESCRIPTION, TEST_DOCUMENT_DESCRIPTION_EDITED,
    TEST_DOCUMENT_LABEL_EDITED
)
from metadata.models import MetadataType, DocumentTypeMetadataType

from ..models import Index, IndexInstanceNode, IndexTemplateNode

from .literals import (
    TEST_INDEX_TEMPLATE_DOCUMENT_DESCRIPTION_EXPRESSION,
    TEST_INDEX_TEMPLATE_DOCUMENT_LABEL_EXPRESSION,
    TEST_INDEX_TEMPLATE_METADATA_EXPRESSION, TEST_METADATA_TYPE_LABEL,
    TEST_METADATA_TYPE_NAME
)
from .mixins import DocumentIndexingTestMixin


@override_settings(OCR_AUTO_OCR=False)
class IndexTestCase(DocumentIndexingTestMixin, DocumentTestMixin, BaseTestCase):
    def test_document_description_index(self):
        self._create_index()

        self.index.node_templates.create(
            parent=self.index.template_root,
            expression=TEST_INDEX_TEMPLATE_DOCUMENT_DESCRIPTION_EXPRESSION,
            link_documents=True
        )

        self.document.description = TEST_DOCUMENT_DESCRIPTION
        self.document.save()

        self.index.rebuild()

        self.assertEqual(
            IndexInstanceNode.objects.last().value, self.document.description
        )
        self.document.description = TEST_DOCUMENT_DESCRIPTION_EDITED
        self.document.save()

        self.assertEqual(
            IndexInstanceNode.objects.last().value, self.document.description
        )

    def test_document_label_index(self):
        self._create_index()

        self.index.node_templates.create(
            parent=self.index.template_root,
            expression=TEST_INDEX_TEMPLATE_DOCUMENT_LABEL_EXPRESSION,
            link_documents=True
        )

        self.index.rebuild()

        self.assertEqual(
            IndexInstanceNode.objects.last().value, self.document.label
        )
        self.document.label = TEST_DOCUMENT_LABEL_EDITED
        self.document.save()

        self.assertEqual(
            IndexInstanceNode.objects.last().value, self.document.label
        )

    def test_date_based_index(self):
        self._create_index()

        level_year = self.index.node_templates.create(
            parent=self.index.template_root,
            expression='{{ document.date_added|date:"Y" }}',
            link_documents=False
        )

        self.index.node_templates.create(
            parent=level_year,
            expression='{{ document.date_added|date:"m" }}',
            link_documents=True
        )
        # Index the document created by default
        Index.objects.rebuild()

        self.document.delete()

        # Uploading a new should not trigger an error
        document = self.upload_document()

        self.assertEqual(
            list(IndexInstanceNode.objects.values_list('value', flat=True)),
            [
                '', force_text(document.date_added.year),
                '{:02}'.format(document.date_added.month)
            ]
        )

        self.assertTrue(
            document in IndexInstanceNode.objects.last().documents.all()
        )

    def test_dual_level_dual_document_index(self):
        """
        Test creation of an index instance with two first levels with different
        values and two second levels with the same value but as separate
        children of each of the first levels. GitLab issue #391
        """
        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.document_2 = self.document_type.new_document(
                file_object=file_object
            )

        self._create_index()

        # Create simple index template
        root = self.index.template_root
        level_1 = self.index.node_templates.create(
            parent=root, expression='{{ document.uuid }}',
            link_documents=False
        )

        self.index.node_templates.create(
            parent=level_1, expression='{{ document.label }}',
            link_documents=True
        )

        Index.objects.rebuild()

        # Typecast to sets to make sorting irrelevant in the comparison.
        self.assertEqual(
            set(IndexInstanceNode.objects.values_list('value', flat=True)),
            set(
                [
                    '', force_text(self.document_2.uuid), self.document_2.label,
                    force_text(self.document.uuid), self.document.label
                ]
            )
        )

    def test_metadata_indexing(self):
        metadata_type = MetadataType.objects.create(
            name=TEST_METADATA_TYPE_NAME, label=TEST_METADATA_TYPE_LABEL
        )
        DocumentTypeMetadataType.objects.create(
            document_type=self.document_type, metadata_type=metadata_type
        )

        self._create_index()

        # Create simple index template
        root = self.index.template_root
        self.index.node_templates.create(
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

    def test_multi_level_template_with_no_result_parent(self):
        """
        On a two level template if the first level doesn't return a result
        the indexing should stop. GitLab issue #391.
        """
        self._create_index()

        level_1 = self.index.node_templates.create(
            parent=self.index.template_root,
            expression='',
            link_documents=True
        )

        self.index.node_templates.create(
            parent=level_1, expression='{{ document.label }}',
            link_documents=True
        )

        Index.objects.rebuild()

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

        self._create_index()

        # Create simple index template
        root = self.index.template_root
        self.index.node_templates.create(
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
