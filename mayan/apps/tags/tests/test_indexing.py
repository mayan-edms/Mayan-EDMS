from __future__ import unicode_literals

from django.core.files.base import File
from django.test import override_settings

from common.tests import BaseTestCase
from documents.models import DocumentType
from documents.tests import TEST_DOCUMENT_TYPE_LABEL, TEST_SMALL_DOCUMENT_PATH
from document_indexing.models import Index, IndexInstanceNode
from document_indexing.tests.literals import TEST_INDEX_LABEL

from ..models import Tag

from .literals import (
    TEST_TAG_COLOR, TEST_TAG_LABEL, TEST_TAG_INDEX_HAS_TAG,
    TEST_TAG_INDEX_NO_TAG, TEST_TAG_INDEX_NODE_TEMPLATE
)


@override_settings(OCR_AUTO_OCR=False)
class TagSignalIndexingTestCase(BaseTestCase):
    def setUp(self):
        super(TagSignalIndexingTestCase, self).setUp()
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

    def tearDown(self):
        self.document.delete()
        self.document_type.delete()
        super(TagSignalIndexingTestCase, self).tearDown()

    def _create_document(self):
        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=File(file_object)
            )

    def test_tag_indexing(self):
        index = Index.objects.create(label=TEST_INDEX_LABEL)

        index.document_types.add(self.document_type)

        root = index.template_root
        index.node_templates.create(
            parent=root, expression=TEST_TAG_INDEX_NODE_TEMPLATE,
            link_documents=True
        )

        tag = Tag.objects.create(color=TEST_TAG_COLOR, label=TEST_TAG_LABEL)
        self._create_document()

        self.assertTrue(
            self.document in IndexInstanceNode.objects.get(
                value=TEST_TAG_INDEX_NO_TAG
            ).documents.all()
        )

        tag.documents.add(self.document)

        self.assertTrue(
            self.document in IndexInstanceNode.objects.get(
                value=TEST_TAG_INDEX_HAS_TAG
            ).documents.all()
        )

        tag.delete()

        self.assertTrue(
            self.document in IndexInstanceNode.objects.get(
                value=TEST_TAG_INDEX_NO_TAG
            ).documents.all()
        )
