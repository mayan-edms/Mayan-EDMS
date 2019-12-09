from __future__ import unicode_literals

from django.utils.encoding import force_text

from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.documents.tests.mixins import DocumentViewTestMixin
from mayan.apps.documents.permissions import permission_document_view

from ..permissions import permission_tag_view

from .mixins import TagTestMixin


class DocumentTagHTMLWidgetTestCase(
    DocumentViewTestMixin, TagTestMixin, GenericDocumentViewTestCase
):
    def test_document_tags_widget_no_permissions(self):
        self._create_test_tag()

        self.test_tag.documents.add(self.test_document)

        response = self._request_test_document_list_view()
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_tag.label, status_code=200
        )

    def test_document_tags_widget_with_document_access(self):
        self._create_test_tag()

        self.test_tag.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_document_list_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )
        self.assertNotContains(
            response=response, text=force_text(self.test_tag), status_code=200
        )

    def test_document_tags_widget_with_tag_access(self):
        self._create_test_tag()

        self.test_tag.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_tag, permission=permission_tag_view
        )

        response = self._request_test_document_list_view()
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_tag.label, status_code=200
        )

    def test_document_tags_widget_with_full_access(self):
        self._create_test_tag()

        self.test_tag.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_tag, permission=permission_tag_view
        )

        response = self._request_test_document_list_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )
        self.assertContains(
            response=response, text=self.test_tag.label, status_code=200
        )
