from mayan.apps.common.tests.mixins import ObjectCopyTestMixin
from mayan.apps.documents.tests.mixins import DocumentTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import SmartLinkTestMixin


class SmartLinkCopyTestCase(
    SmartLinkTestMixin, DocumentTestMixin, ObjectCopyTestMixin, BaseTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_smart_link()
        self._create_test_smart_link_condition()
        self.test_smart_link.document_types.add(self.test_document_type)
        self.test_object = self.test_smart_link
