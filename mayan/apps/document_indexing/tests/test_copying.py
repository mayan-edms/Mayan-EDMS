from mayan.apps.common.tests.mixins import ObjectCopyTestMixin
from mayan.apps.documents.tests.mixins import DocumentTestMixin
from mayan.apps.tests.tests.base import BaseTestCase

from .mixins import IndexTestMixin


class IndexTemplateCopyTestCase(
    IndexTestMixin, DocumentTestMixin, ObjectCopyTestMixin, BaseTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_index()
        self._create_test_index_template_node()
        self.test_index.document_types.add(self.test_document_type)
        self.test_object = self.test_index
