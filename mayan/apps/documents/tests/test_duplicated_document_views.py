# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ..permissions import permission_document_view

from .base import GenericDocumentViewTestCase
from .literals import (
    TEST_SMALL_DOCUMENT_FILENAME, TEST_SMALL_DOCUMENT_PATH,
)


class DuplicatedDocumentsViewsTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(DuplicatedDocumentsViewsTestCase, self).setUp()
        self.login_user()

    def _upload_duplicate_document(self):
        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.document_duplicate = self.document_type.new_document(
                file_object=file_object, label=TEST_SMALL_DOCUMENT_FILENAME
            )

    def _request_duplicated_document_list_view(self):
        return self.get(viewname='documents:duplicated_document_list')

    def _request_document_duplicates_list_view(self):
        return self.get(
            viewname='documents:document_duplicates_list',
            args=(self.document.pk,)
        )

    def test_duplicated_document_list_no_permissions(self):
        self._upload_duplicate_document()
        response = self._request_duplicated_document_list_view()

        self.assertNotContains(
            response=response, text=self.document.label, status_code=200
        )

    def test_duplicated_document_list_with_access(self):
        self._upload_duplicate_document()
        self.grant_access(
            obj=self.document, permission=permission_document_view
        )
        self.grant_access(
            obj=self.document_duplicate,
            permission=permission_document_view
        )
        response = self._request_duplicated_document_list_view()

        self.assertContains(
            response=response, text=self.document.label, status_code=200
        )

    def test_document_duplicates_list_no_permissions(self):
        self._upload_duplicate_document()
        response = self._request_document_duplicates_list_view()

        self.assertEqual(response.status_code, 403)

    def test_document_duplicates_list_with_access(self):
        self._upload_duplicate_document()
        self.grant_access(
            obj=self.document, permission=permission_document_view
        )
        self.grant_access(
            obj=self.document_duplicate,
            permission=permission_document_view
        )
        response = self._request_document_duplicates_list_view()

        self.assertContains(
            response=response, text=self.document.label, status_code=200
        )
