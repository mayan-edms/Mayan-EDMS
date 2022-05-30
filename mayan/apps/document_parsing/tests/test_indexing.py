from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.document_indexing.models.index_instance_models import IndexInstanceNode
from mayan.apps.document_indexing.tests.mixins import IndexTemplateTestMixin

from .literals import TEST_DOCUMENT_FILE_CONTENT_INDEX_NODE_TEMPLATE
from .mixins import DocumentFileContentTestMixin


class DocumentFileContentIndexingTestCase(
    DocumentFileContentTestMixin, IndexTemplateTestMixin,
    GenericDocumentTestCase
):
    _test_index_template_node_expression = TEST_DOCUMENT_FILE_CONTENT_INDEX_NODE_TEMPLATE
    auto_upload_test_document = True

    def test_indexing_document_file_not_parsed(self):
        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=self._test_document
            ).exists()
        )

    def test_indexing_document_file_parsed_delete(self):
        self._create_test_document_file_parsed_content()
        value = ' '.join(self._test_document.file_latest.content())

        self._do_test_document_file_parsed_content_delete()

        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=value
            ).exists()
        )

    def test_indexing_document_file_parsed_finished(self):
        self._create_test_document_file_parsed_content()
        value = ' '.join(self._test_document.file_latest.content())

        self.assertTrue(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=value
            ).exists()
        )
