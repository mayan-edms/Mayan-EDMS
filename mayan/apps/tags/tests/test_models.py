from __future__ import unicode_literals

from mayan.apps.common.tests.base import BaseTestCase
from mayan.apps.documents.tests.mixins import DocumentTestMixin

from .mixins import TagTestMixin


class TagTestCase(DocumentTestMixin, TagTestMixin, BaseTestCase):
    auto_upload_document = False

    def test_document_addition(self):
        self._create_test_tag()
        self.upload_document()

        self.test_tag.documents.add(self.test_document)

        self.assertTrue(self.test_document in self.test_tag.documents.all())

    def test_document_remove(self):
        self._create_test_tag()
        self.upload_document()

        self.test_tag.documents.remove(self.test_document)

        self.assertTrue(self.test_document not in self.test_tag.documents.all())
