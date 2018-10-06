from __future__ import unicode_literals

from django.test import override_settings

from common.tests import BaseTestCase
from documents.tests import DocumentTestMixin

from ..models import Tag

from .literals import TEST_TAG_COLOR, TEST_TAG_LABEL


@override_settings(OCR_AUTO_OCR=False)
class TagTestCase(DocumentTestMixin, BaseTestCase):
    auto_upload_document = False

    def test_addition_and_deletion_of_documents(self):
        tag = Tag.objects.create(color=TEST_TAG_COLOR, label=TEST_TAG_LABEL)
        self.document = self.upload_document()

        tag.documents.add(self.document)

        self.assertEqual(tag.documents.count(), 1)
        self.assertEqual(list(tag.documents.all()), [self.document])

        tag.documents.remove(self.document)

        self.assertEqual(tag.documents.count(), 0)
        self.assertEqual(list(tag.documents.all()), [])

        tag.delete()
