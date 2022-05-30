from django.db.utils import IntegrityError

from mayan.apps.documents.models.trashed_document_models import TrashedDocument
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
    TEST_INDEX_TEMPLATE_DOCUMENT_TYPE_EXPRESSION
)
from .mixins import IndexTemplateTestMixin


class IndexTemplateTestCase(IndexTemplateTestMixin, GenericDocumentTestCase):
    auto_upload_test_document = False

    def test_method_get_absolute_url(self):
        self._create_test_index_template()
        self.assertTrue(self._test_index_template.get_absolute_url())


class IndexInstanceBasicTestCase(
    IndexTemplateTestMixin, GenericDocumentTestCase
):
    _test_index_template_node_expression = TEST_INDEX_TEMPLATE_DOCUMENT_LABEL_EXPRESSION
    auto_upload_test_document = False

    def test_index_instance_on_document_creation(self):
        self._create_test_document_stub()

        self.assertTrue(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
            ).exists()
        )

        test_document_id = self._test_document.pk
        self._test_document.delete()

        self.assertTrue(
            IndexInstanceNode.objects.filter(
                documents=test_document_id
            ).exists()
        )

        TrashedDocument.objects.get(pk=self._test_document.pk).restore()
        self._test_document.refresh_from_db()

        self.assertTrue(
            IndexInstanceNode.objects.filter(
                documents=test_document_id
            ).exists()
        )

        self._test_document.delete()
        self._test_document.delete()

        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=test_document_id
            ).exists()
        )

    def test_index_instance_node_id_persistence(self):
        self._create_test_document_stub()

        index_instance_node_id = IndexInstanceNode.objects.get(
            documents=self._test_document
        ).pk

        IndexInstance.objects.document_add(document=self._test_document)

        self.assertEqual(
            IndexInstanceNode.objects.get(documents=self._test_document).pk,
            index_instance_node_id
        )

    def test_index_instance_node_cleanup(self):
        self._create_test_document_stub()

        document_index_instance_node_count = IndexInstanceNode.objects.count()

        self._test_document.label = TEST_DOCUMENT_LABEL_EDITED
        self._test_document.save()

        self.assertEqual(
            IndexInstanceNode.objects.count(),
            document_index_instance_node_count
        )


class IndexInstanceTestCase(IndexTemplateTestMixin, GenericDocumentTestCase):
    auto_upload_test_document = False
    auto_create_test_index_template_node = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_date_based_index(self):
        level_year = self._test_index_template.index_template_nodes.create(
            parent=self._test_index_template.index_template_root_node,
            expression='{{ document.datetime_created|date:"Y" }}',
            link_documents=False
        )

        self._test_index_template.index_template_nodes.create(
            parent=level_year,
            expression='{{ document.datetime_created|date:"m" }}',
            link_documents=True
        )
        # Index the document created by default.
        IndexTemplate.objects.rebuild()

        self._test_document.delete()

        # Uploading a new should not trigger an error.
        self._upload_test_document()

        self.assertEqual(
            list(IndexInstanceNode.objects.values_list('value', flat=True)),
            [
                '', str(self._test_document.datetime_created.year),
                '{:02}'.format(self._test_document.datetime_created.month)
            ]
        )

        self.assertTrue(
            self._test_document in IndexInstanceNode.objects.last().documents.all()
        )

    def test_dual_level_dual_document_index(self):
        """
        Test creation of an index instance with two first levels with different
        values and two second levels with the same value but as separate
        children of each of the first levels. GitLab issue #391
        """
        self._create_test_document_stub()

        # Create simple index template
        level_1 = self._test_index_template.index_template_nodes.create(
            expression='{{ document.uuid }}', link_documents=False,
            parent=self._test_index_template_root_node
        )

        self._test_index_template.index_template_nodes.create(
            expression='{{ document.label }}', link_documents=True,
            parent=level_1
        )

        IndexTemplate.objects.rebuild()

        # Typecast to sets to make sorting irrelevant in the comparison.
        self.assertEqual(
            set(IndexInstanceNode.objects.values_list('value', flat=True)),
            {
                '', str(self._test_documents[1].uuid),
                self._test_documents[1].label,
                str(self._test_documents[0].uuid),
                self._test_documents[0].label
            }
        )

    def test_document_description_index(self):
        self._create_test_index_template_node(
            expression=TEST_INDEX_TEMPLATE_DOCUMENT_DESCRIPTION_EXPRESSION
        )

        self._test_document.description = TEST_DOCUMENT_DESCRIPTION
        self._test_document.save()

        self._test_index_template.rebuild()

        self.assertEqual(
            IndexInstanceNode.objects.last().value,
            self._test_document.description
        )
        self._test_document.description = TEST_DOCUMENT_DESCRIPTION_EDITED
        self._test_document.save()

        self.assertEqual(
            IndexInstanceNode.objects.last().value,
            self._test_document.description
        )

    def test_document_label_index(self):
        self._create_test_index_template_node(
            expression=TEST_INDEX_TEMPLATE_DOCUMENT_LABEL_EXPRESSION
        )

        self._test_index_template.rebuild()

        self.assertEqual(
            IndexInstanceNode.objects.last().value, self._test_document.label
        )
        self._test_document.label = TEST_DOCUMENT_LABEL_EDITED
        self._test_document.save()

        self.assertEqual(
            IndexInstanceNode.objects.last().value, self._test_document.label
        )

    def test_document_type_index(self):
        self._create_test_index_template_node(
            expression=TEST_INDEX_TEMPLATE_DOCUMENT_TYPE_EXPRESSION
        )

        self._test_index_template.rebuild()

        self.assertEqual(
            IndexInstanceNode.objects.last().value,
            self._test_document_types[0].label
        )

        self._create_test_document_type()
        self._test_index_template.document_types.add(self._test_document_type)

        self._test_document.document_type_change(
            document_type=self._test_document_type
        )

        self.assertEqual(
            IndexInstanceNode.objects.last().value,
            self._test_document_types[1].label
        )

    def test_method_get_absolute_url(self):
        test_index_instance = IndexInstance.objects.first()
        self.assertTrue(test_index_instance.get_absolute_url())

    def test_multi_level_template_with_no_result_parent(self):
        """
        On a two level template if the first level doesn't return a result
        the indexing should stop. GitLab issue #391.
        """
        level_1 = self._test_index_template.index_template_nodes.create(
            expression='', link_documents=True,
            parent=self._test_index_template_root_node,
        )

        self._test_index_template.index_template_nodes.create(
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
            document_type=self._test_document_type,
            metadata_type=metadata_type
        )

        # Add document metadata value.
        self._test_document.metadata.create(
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
            instance_node.documents.all(), [repr(self._test_document)]
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

        self._test_index_template.rebuild()

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
