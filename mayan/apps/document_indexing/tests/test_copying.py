from mayan.apps.common.tests.mixins import ObjectCopyTestMixin
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import IndexTemplateTestMixin


class IndexTemplateCopyTestCase(
    IndexTemplateTestMixin, DocumentTestMixin, ObjectCopyTestMixin,
    BaseTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_index_template()
        self._create_test_index_template_node()
        self._test_index_template.document_types.add(self._test_document_type)
        self._test_object = self._test_index_template
