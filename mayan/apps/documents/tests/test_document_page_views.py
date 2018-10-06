# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ..permissions import permission_document_view

from .base import GenericDocumentViewTestCase


class DocumentPageViewTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(DocumentPageViewTestCase, self).setUp()
        self.login_user()

    def _document_page_list_view(self):
        return self.get(
            viewname='documents:document_pages', args=(self.document.pk,)
        )

    def test_document_page_list_view_no_permission(self):
        response = self._document_page_list_view()
        self.assertEqual(response.status_code, 403)

    def test_document_page_list_view_with_access(self):
        self.grant_access(
            obj=self.document, permission=permission_document_view
        )
        response = self._document_page_list_view()
        self.assertContains(
            response=response, text=self.document.label, status_code=200
        )
