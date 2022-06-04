from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.document_indexing.models.index_instance_models import IndexInstanceNode
from mayan.apps.document_indexing.tests.mixins import IndexTemplateTestMixin

from .literals import TEST_CHECKOUT_INDEX_NODE_TEMPLATE
from .mixins import DocumentCheckoutTestMixin


class CheckoutIndexingTestCase(
    DocumentCheckoutTestMixin, IndexTemplateTestMixin,
    GenericDocumentTestCase
):
    _test_index_template_node_expression = TEST_CHECKOUT_INDEX_NODE_TEMPLATE
    auto_create_test_document_stub = True
    auto_upload_test_document = False

    def test_indexing_no_checkout(self):
        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
            ).exists()
        )

    def test_indexing_document_check_in(self):
        self._check_out_test_document()

        self._check_in_test_document()

        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
            ).exists()
        )

    def test_indexing_document_check_out(self):
        self._check_out_test_document()

        self.assertTrue(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
            ).exists()
        )
