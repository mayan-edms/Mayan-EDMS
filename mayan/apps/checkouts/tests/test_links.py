from __future__ import unicode_literals

from mayan.apps.documents.tests import GenericDocumentViewTestCase

from ..links import link_check_out_document, link_check_out_info
from ..permissions import (
    permission_document_check_out, permission_document_check_out_detail_view
)

from .mixins import DocumentCheckoutTestMixin


class CheckoutLinksTestCase(DocumentCheckoutTestMixin, GenericDocumentViewTestCase):
    def _resolve_checkout_link(self):
        self.add_test_view(test_object=self.test_document)
        context = self.get_test_view()
        context['user'] = self._test_case_user
        return link_check_out_document.resolve(context=context)

    def test_checkout_link_no_access(self):
        resolved_link = self._resolve_checkout_link()
        self.assertEqual(resolved_link, None)

    def test_checkout_link_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_check_out
        )
        resolved_link = self._resolve_checkout_link()
        self.assertNotEqual(resolved_link, None)

    def _resolve_checkout_info_link(self):
        self.add_test_view(test_object=self.test_document)
        context = self.get_test_view()
        context['user'] = self._test_case_user
        return link_check_out_info.resolve(context=context)

    def test_checkout_info_link_no_access(self):
        resolved_link = self._resolve_checkout_info_link()
        self.assertEqual(resolved_link, None)

    def test_checkout_info_link_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_check_out_detail_view
        )
        resolved_link = self._resolve_checkout_info_link()
        self.assertNotEqual(resolved_link, None)
