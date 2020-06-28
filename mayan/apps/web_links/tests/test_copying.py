from mayan.apps.common.tests.mixins import ObjectCopyTestMixin
from mayan.apps.documents.tests.mixins import DocumentTestMixin
from mayan.apps.tests.tests.base import BaseTestCase

from .mixins import WebLinkTestMixin


class WebLinkCopyTestCase(
    DocumentTestMixin, WebLinkTestMixin, ObjectCopyTestMixin, BaseTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_web_link()
        self.test_web_link.document_types.add(self.test_document_type)
        self.test_object = self.test_web_link
