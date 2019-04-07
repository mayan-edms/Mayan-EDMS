from __future__ import unicode_literals

from documents.tests import GenericDocumentViewTestCase

from ..links import link_checkout_document, link_checkout_info
from ..permissions import (
    permission_document_checkout, permission_document_checkout_detail_view
)

from .mixins import DocumentCheckoutTestMixin


class CheckoutLinksTestCase(DocumentCheckoutTestMixin, GenericDocumentViewTestCase):
    def setUp(self):
        super(CheckoutLinksTestCase, self).setUp()
        self.login_user()

    def _resolve_checkout_link(self):
        self.add_test_view(test_object=self.document)
        context = self.get_test_view()
        context['user'] = self.user
        return link_checkout_document.resolve(context=context)

    def test_checkout_link_no_access(self):
        resolved_link = self._resolve_checkout_link()
        self.assertEqual(resolved_link, None)

    def test_checkout_link_with_access(self):
        self.grant_access(
            obj=self.document, permission=permission_document_checkout
        )
        resolved_link = self._resolve_checkout_link()
        self.assertNotEqual(resolved_link, None)

    def _resolve_checkout_info_link(self):
        self.add_test_view(test_object=self.document)
        context = self.get_test_view()
        context['user'] = self.user
        return link_checkout_info.resolve(context=context)

    def test_checkout_info_link_no_access(self):
        resolved_link = self._resolve_checkout_info_link()
        self.assertEqual(resolved_link, None)

    def test_checkout_info_link_with_access(self):
        self.grant_access(
            obj=self.document, permission=permission_document_checkout_detail_view
        )
        resolved_link = self._resolve_checkout_info_link()
        self.assertNotEqual(resolved_link, None)
