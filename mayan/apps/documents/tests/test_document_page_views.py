from __future__ import unicode_literals

from django.utils.encoding import force_text

from ..permissions import (
    permission_document_edit, permission_document_view
)

from .base import GenericDocumentViewTestCase


class DocumentPageDisableViewTestMixin(object):
    def _disable_test_document_page(self):
        self.test_document_page.enabled = False
        self.test_document_page.save()

    def _request_test_document_page_disable_view(self):
        return self.post(
            viewname='documents:document_page_disable', kwargs={
                'pk': self.test_document_page.pk
            }
        )

    def _request_test_document_page_enable_view(self):
        return self.post(
            viewname='documents:document_page_enable', kwargs={
                'pk': self.test_document_page.pk
            }
        )

    def _request_test_document_page_multiple_disable_view(self):
        return self.post(
            viewname='documents:document_page_multiple_disable', data={
                'id_list': self.test_document_page.pk
            }
        )

    def _request_test_document_page_multiple_enable_view(self):
        return self.post(
            viewname='documents:document_page_multiple_enable', data={
                'id_list': self.test_document_page.pk
            }
        )


class DocumentPageDisableViewTestCase(
    DocumentPageDisableViewTestMixin, GenericDocumentViewTestCase
):
    def test_document_page_disable_view_no_permission(self):
        test_document_page_count = self.test_document.pages.count()

        response = self._request_test_document_page_disable_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            test_document_page_count, self.test_document.pages.count()
        )

    def test_document_page_disable_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_edit
        )

        test_document_page_count = self.test_document.pages.count()

        response = self._request_test_document_page_disable_view()
        self.assertEqual(response.status_code, 302)

        self.assertNotEqual(
            test_document_page_count, self.test_document.pages.count()
        )

    def test_document_page_multiple_disable_view_no_permission(self):
        test_document_page_count = self.test_document.pages.count()

        response = self._request_test_document_page_multiple_disable_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            test_document_page_count, self.test_document.pages.count()
        )

    def test_document_page_multiple_disable_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_edit
        )

        test_document_page_count = self.test_document.pages.count()

        response = self._request_test_document_page_multiple_disable_view()
        self.assertEqual(response.status_code, 302)

        self.assertNotEqual(
            test_document_page_count, self.test_document.pages.count()
        )

    def test_document_page_enable_view_no_permission(self):
        self._disable_test_document_page()

        test_document_page_count = self.test_document.pages.count()

        response = self._request_test_document_page_enable_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            test_document_page_count, self.test_document.pages.count()
        )

    def test_document_page_enable_view_with_access(self):
        self._disable_test_document_page()
        self.grant_access(
            obj=self.test_document, permission=permission_document_edit
        )

        test_document_page_count = self.test_document.pages.count()

        response = self._request_test_document_page_enable_view()
        self.assertEqual(response.status_code, 302)

        self.assertNotEqual(
            test_document_page_count, self.test_document.pages.count()
        )

    def test_document_page_multiple_enable_view_no_permission(self):
        self._disable_test_document_page()
        test_document_page_count = self.test_document.pages.count()

        response = self._request_test_document_page_multiple_enable_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            test_document_page_count, self.test_document.pages.count()
        )

    def test_document_page_multiple_enable_view_with_access(self):
        self._disable_test_document_page()
        self.grant_access(
            obj=self.test_document, permission=permission_document_edit
        )

        test_document_page_count = self.test_document.pages.count()

        response = self._request_test_document_page_multiple_enable_view()
        self.assertEqual(response.status_code, 302)

        self.assertNotEqual(
            test_document_page_count, self.test_document.pages.count()
        )


class DocumentPageViewTestMixin(object):
    def _request_test_document_page_list_view(self):
        return self.get(
            viewname='documents:document_pages', kwargs={
                'pk': self.test_document.pk
            }
        )

    def _request_test_document_page_view(self, document_page):
        return self.get(
            viewname='documents:document_page_view', kwargs={
                'pk': document_page.pk,
            }
        )


class DocumentPageViewTestCase(
    DocumentPageViewTestMixin, GenericDocumentViewTestCase
):
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
