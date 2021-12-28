from django.db.utils import IntegrityError

from mayan.apps.documents.tests.base import (
    GenericDocumentTestCase, GenericTransactionDocumentTestCase
)
from mayan.apps.documents.tests.literals import (
    TEST_DOCUMENT_DESCRIPTION, TEST_DOCUMENT_DESCRIPTION_EDITED,
    TEST_DOCUMENT_LABEL_EDITED
)
from mayan.apps.metadata.models import MetadataType, DocumentTypeMetadataType

from ..models import (
    IndexInstance, IndexInstanceNode, IndexTemplate, IndexTemplateNode
)

from .literals import (
    TEST_INDEX_TEMPLATE_DOCUMENT_DESCRIPTION_EXPRESSION,
    TEST_INDEX_TEMPLATE_DOCUMENT_LABEL_EXPRESSION,
    TEST_INDEX_TEMPLATE_DOCUMENT_TYPE_EXPRESSION,
    TEST_INDEX_TEMPLATE_METADATA_EXPRESSION, TEST_METADATA_TYPE_LABEL,
    TEST_METADATA_TYPE_NAME
)
from .mixins import IndexTemplateTestMixin


class IndexTemplateTestCase(IndexTemplateTestMixin, GenericDocumentTestCase):
    auto_upload_test_document = False

    def test_method_get_absolute_url(self):
        self._create_test_index_template()
        self.assertTrue(self.test_index_template.get_absolute_url())


class IndexInstanceTestCase(IndexTemplateTestMixin, GenericDocumentTestCase):
    auto_upload_test_document = False
    auto_create_test_index_template_node = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_date_based_index(self):
        level_year = self.test_index_template.index_template_nodes.create(
            parent=self.test_index_template.index_template_root_node,
            expression='{{ document.datetime_created|date:"Y" }}',
            link_documents=False
        )

        self.test_index_template.index_template_nodes.create(
            parent=level_year,
            expression='{{ document.datetime_created|date:"m" }}',
            link_documents=True
        )
        # Index the document created by default.
        IndexTemplate.objects.rebuild()

        self.test_document.delete()

        # Uploading a new should not trigger an error.
        self._upload_test_document()

        self.assertEqual(
            list(IndexInstanceNode.objects.values_list('value', flat=True)),
            [
                '', str(self.test_document.datetime_created.year),
                '{:02}'.format(self.test_document.datetime_created.month)
            ]
        )

        self.assertTrue(
            self.test_document in IndexInstanceNode.objects.last().documents.all()
        )

    def test_dual_level_dual_document_index(self):
        """
        Test creation of an index instance with two first levels with different
        values and two second levels with the same value but as separate
        children of each of the first levels. GitLab issue #391
        """
        self._create_test_document_stub()

        # Create simple index template
        level_1 = self.test_index_template.index_template_nodes.create(
            expression='{{ document.uuid }}', link_documents=False,
            parent=self.test_index_template_root_node
        )

        self.test_index_template.index_template_nodes.create(
            expression='{{ document.label }}', link_documents=True,
            parent=level_1
        )

        IndexTemplate.objects.rebuild()

        # Typecast to sets to make sorting irrelevant in the comparison.
        self.assertEqual(
            set(IndexInstanceNode.objects.values_list('value', flat=True)),
            set(
                [
                    '', str(self.test_documents[1].uuid), self.test_documents[1].label,
                    str(self.test_documents[0].uuid), self.test_documents[0].label
                ]
            )
        )

    def test_document_description_index(self):
        self._create_test_index_template_node(
            expression=TEST_INDEX_TEMPLATE_DOCUMENT_DESCRIPTION_EXPRESSION
        )

        self.test_document.description = TEST_DOCUMENT_DESCRIPTION
        self.test_document.save()

        self.test_index_template.rebuild()

        self.assertEqual(
            IndexInstanceNode.objects.last().value,
            self.test_document.description
        )
        self.test_document.description = TEST_DOCUMENT_DESCRIPTION_EDITED
        self.test_document.save()

        self.assertEqual(
            IndexInstanceNode.objects.last().value,
            self.test_document.description
        )

    def test_document_label_index(self):
        self._create_test_index_template_node(
            expression=TEST_INDEX_TEMPLATE_DOCUMENT_LABEL_EXPRESSION
        )

        self.test_index_template.rebuild()

        self.assertEqual(
            IndexInstanceNode.objects.last().value, self.test_document.label
        )
        self.test_document.label = TEST_DOCUMENT_LABEL_EDITED
        self.test_document.save()

        self.assertEqual(
            IndexInstanceNode.objects.last().value, self.test_document.label
        )

    def test_document_type_index(self):
        self._create_test_index_template_node(
            expression=TEST_INDEX_TEMPLATE_DOCUMENT_TYPE_EXPRESSION
        )

        self.test_index_template.rebuild()

        self.assertEqual(
            IndexInstanceNode.objects.last().value,
            self.test_document_types[0].label
        )

        self._create_test_document_type()
        self.test_index_template.document_types.add(self.test_document_type)

        self.test_document.document_type_change(
            document_type=self.test_document_type
        )

        self.assertEqual(
            IndexInstanceNode.objects.last().value,
            self.test_document_types[1].label
        )

    def test_metadata_indexing(self):
        metadata_type = MetadataType.objects.create(
            name=TEST_METADATA_TYPE_NAME, label=TEST_METADATA_TYPE_LABEL
        )
        DocumentTypeMetadataType.objects.create(
            document_type=self.test_document_type,
            metadata_type=metadata_type
        )

        self._create_test_index_template_node(
            expression=TEST_INDEX_TEMPLATE_METADATA_EXPRESSION
        )

        # Add document metadata value to trigger index node instance
        # creation.
        self.test_document.metadata.create(
            metadata_type=metadata_type, value='0001'
        )
        self.assertEqual(
            list(
                IndexInstanceNode.objects.values_list('value', flat=True)
            ), ['', '0001']
        )

        # Check that document is in instance node.
        instance_node = IndexInstanceNode.objects.get(value='0001')
        self.assertQuerysetEqual(
            instance_node.documents.all(), [repr(self.test_document)]
        )

        # Change document metadata value to trigger index node instance
        # update.
        document_metadata = self.test_document.metadata.get(
            metadata_type=metadata_type
        )
        document_metadata.value = '0002'
        document_metadata.save()
        self.assertEqual(
            list(
                IndexInstanceNode.objects.values_list('value', flat=True)
            ), ['', '0002']
        )

        # Check that document is in new instance node.
        instance_node = IndexInstanceNode.objects.get(value='0002')
        self.assertQuerysetEqual(
            instance_node.documents.all(), [repr(self.test_document)]
        )

        # Check node instance is destoyed when no metadata is available.
        self.test_document.metadata.get(metadata_type=metadata_type).delete()
        self.assertEqual(
            list(
                IndexInstanceNode.objects.values_list('value', flat=True)
            ), ['']
        )

        # Add document metadata value again to trigger index node instance
        # creation.
        self.test_document.metadata.create(
            metadata_type=metadata_type, value='0003'
        )
        self.assertEqual(
            list(
                IndexInstanceNode.objects.values_list('value', flat=True)
            ), ['', '0003']
        )

        # Check node instance is destroyed when no documents are contained.
        self.test_document.delete()

        # Document is in trash, index structure should remain unchanged.
        self.assertEqual(
            list(
                IndexInstanceNode.objects.values_list('value', flat=True)
            ), ['', '0003']
        )

        # Document deleted, index structure should update.
        self.test_document.delete()
        self.assertEqual(
            list(
                IndexInstanceNode.objects.values_list('value', flat=True)
            ), ['']
        )

    def test_method_get_absolute_url(self):
        test_index_instance = IndexInstance.objects.first()
        self.assertTrue(test_index_instance.get_absolute_url())

    def test_multi_level_template_with_no_result_parent(self):
        """
        On a two level template if the first level doesn't return a result
        the indexing should stop. GitLab issue #391.
        """
        level_1 = self.test_index_template.index_template_nodes.create(
            expression='', link_documents=True,
            parent=self.test_index_template_root_node,
        )

        self.test_index_template.index_template_nodes.create(
            expression='{{ document.label }}', link_documents=True,
            parent=level_1
        )

        IndexTemplate.objects.rebuild()

    def test_rebuild_all_indexes(self):
        # Add metadata type and connect to document type.
        metadata_type = MetadataType.objects.create(
            name='test', label='test'
        )
        DocumentTypeMetadataType.objects.create(
            document_type=self.test_document_type,
            metadata_type=metadata_type
        )

        # Add document metadata value.
        self.test_document.metadata.create(
            metadata_type=metadata_type, value='0001'
        )

        self._create_test_index_template_node(
            expression='{{ document.metadata_value_of.test }}'
        )

        self.assertEqual(
            list(
                IndexTemplateNode.objects.values_list('expression', flat=True)
            ), ['', '{{ document.metadata_value_of.test }}']
        )

        # There should be only a root index instances nodes.
        self.assertEqual(IndexInstanceNode.objects.count(), 1)
        self.assertEqual(IndexInstanceNode.objects.first().parent, None)

        # Rebuild all indexes.
        IndexTemplate.objects.rebuild()

        # Check that document is in instance node.
        instance_node = IndexInstanceNode.objects.get(value='0001')
        self.assertQuerysetEqual(
            instance_node.documents.all(), [repr(self.test_document)]
        )


class IndexIntegrityTestCase(
    IndexTemplateTestMixin, GenericTransactionDocumentTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_unique_value_per_level(self):
        self._create_test_index_template_node(
            expression=TEST_INDEX_TEMPLATE_DOCUMENT_LABEL_EXPRESSION
        )

        self.test_index_template.rebuild()

        index_instance_node = IndexInstanceNode.objects.last()

        with self.assertRaises(expected_exception=IntegrityError):
            IndexInstanceNode.objects.create(
                parent=index_instance_node.parent,
                index_template_node=index_instance_node.index_template_node,
                value=index_instance_node.value
            )

        # Reset the failed database write to allow the database manager
        # to flush the database during the test tear down.
        IndexInstanceNode.objects.create(
            parent=index_instance_node.parent,
            index_template_node=index_instance_node.index_template_node,
            value='{}_{}'.format(
                index_instance_node.value, index_instance_node.pk
            )
        )
