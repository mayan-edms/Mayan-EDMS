from __future__ import unicode_literals

from django.core.files.base import File
from django.test import TestCase, override_settings

from documents.models import DocumentType
from documents.tests import TEST_DOCUMENT_TYPE, TEST_SMALL_DOCUMENT_PATH

from ..models import Tag

from .literals import TEST_TAG_COLOR, TEST_TAG_LABEL


@override_settings(OCR_AUTO_OCR=False)
class TagTestCase(TestCase):
    def setUp(self):
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=File(file_object)
            )

    def tearDown(self):
        self.document.delete()
        self.document_type.delete()

    def runTest(self):
        tag = Tag.objects.create(color=TEST_TAG_COLOR, label=TEST_TAG_LABEL)
        self.assertEqual(tag.label, TEST_TAG_LABEL)
        self.assertEqual(tag.get_color_code(), 'red')

    def test_addition_and_deletion_of_documents(self):
        tag = Tag.objects.create(color=TEST_TAG_COLOR, label=TEST_TAG_LABEL)

        tag.documents.add(self.document)

        self.assertEqual(tag.documents.count(), 1)
        self.assertEqual(list(tag.documents.all()), [self.document])

        tag.documents.remove(self.document)

        self.assertEqual(tag.documents.count(), 0)
        self.assertEqual(list(tag.documents.all()), [])

        tag.delete()
