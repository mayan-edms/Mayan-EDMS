from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import TagTestMixin


class TagDocumentTestCase(DocumentTestMixin, TagTestMixin, BaseTestCase):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_document_addition(self):
        self._create_test_tag()

        self.test_tag.attach_to(document=self.test_document)

        self.assertTrue(self.test_document in self.test_tag.documents.all())

    def test_document_remove(self):
        self._create_test_tag(add_test_document=True)

        self.test_tag.remove_from(document=self.test_document)

        self.assertTrue(
            self.test_document not in self.test_tag.documents.all()
        )


class TagModuleTestCase(TagTestMixin, BaseTestCase):
    def test_method_get_absolute_url(self):
        self._create_test_tag()

        self.assertTrue(self.test_tag.get_absolute_url())
