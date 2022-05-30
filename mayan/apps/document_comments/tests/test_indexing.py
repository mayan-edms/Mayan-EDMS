from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.document_indexing.models.index_instance_models import IndexInstanceNode
from mayan.apps.document_indexing.tests.mixins import IndexTemplateTestMixin

from .literals import (
    TEST_COMMENT_TEXT, TEST_COMMENT_TEXT_EDITED, TEST_INDEX_NODE_TEMPLATE
)
from .mixins import DocumentCommentTestMixin


class DocumentCommentIndexingTestCase(
    DocumentCommentTestMixin, IndexTemplateTestMixin, GenericDocumentTestCase
):
    _test_index_template_node_expression = TEST_INDEX_NODE_TEMPLATE
    auto_create_test_document_stub = True
    auto_upload_test_document = False

    def test_indexing_document_comment_add(self):
        self._create_test_comment(user=self._test_case_user)

        self.assertTrue(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=TEST_COMMENT_TEXT
            ).exists()
        )

    def test_indexing_document_comment_delete(self):
        self._create_test_comment(user=self._test_case_user)
        self._test_document_comment.delete()

        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=TEST_COMMENT_TEXT
            ).exists()
        )

    def test_indexing_document_comment_edit(self):
        self._create_test_comment(user=self._test_case_user)
        self._test_document_comment.text = TEST_COMMENT_TEXT_EDITED
        self._test_document_comment.save()

        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=TEST_COMMENT_TEXT
            ).exists()
        )
        self.assertTrue(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=TEST_COMMENT_TEXT_EDITED
            ).exists()
        )
