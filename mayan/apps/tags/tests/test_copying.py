from mayan.apps.common.tests.mixins import ObjectCopyTestMixin
from mayan.apps.documents.tests.mixins import DocumentTestMixin
from mayan.apps.tests.tests.base import BaseTestCase

from .mixins import TagTestMixin


class TagCopyTestCase(
    DocumentTestMixin, TagTestMixin, ObjectCopyTestMixin, BaseTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_tag()
        self.test_tag.documents.add(self.test_document)
        self.test_object = self.test_tag
