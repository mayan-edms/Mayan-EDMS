from __future__ import unicode_literals

from django.utils.encoding import force_text

from ..permissions import permission_document_view

from .base import GenericDocumentViewTestCase


class DocumentPageViewTestCase(GenericDocumentViewTestCase):
    def _request_test_document_page_list_view(self):
        return self.get(
            viewname='documents:document_pages', kwargs={
                'pk': self.test_document.pk
            }
        )

    def test_document_page_list_view_no_permission(self):
        response = self._request_test_document_page_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_page_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_document_page_list_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )

    def _request_test_document_page_view(self, document_page):
        return self.get(
            viewname='documents:document_page_view', kwargs={
                'pk': document_page.pk,
            }
        )

    def test_document_page_view_no_permissions(self):
        response = self._request_test_document_page_view(
            document_page=self.test_document.pages.first()
        )
        self.assertEqual(response.status_code, 404)

    def test_document_page_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_document_page_view(
            document_page=self.test_document.pages.first()
        )
        self.assertContains(
            response=response, text=force_text(
                self.test_document.pages.first()
            ), status_code=200
        )
