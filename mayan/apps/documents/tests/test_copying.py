from mayan.apps.common.tests.mixins import ObjectCopyTestMixin
from mayan.apps.tests.tests.base import BaseTestCase

from .mixins import DocumentTestMixin


class DocumentTypeCopyTestCase(
    DocumentTestMixin, ObjectCopyTestMixin, BaseTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self.test_object = self.test_document_type
