# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ..permissions import (
    permission_document_version_revert, permission_document_version_view,
)

from .base import GenericDocumentViewTestCase
from .literals import (
    TEST_SMALL_DOCUMENT_PATH, TEST_VERSION_COMMENT
)


class DocumentVersionTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(DocumentVersionTestCase, self).setUp()
        self.login_user()

    def _upload_new_version(self):
        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.document.new_version(
                comment=TEST_VERSION_COMMENT, file_object=file_object
            )

    def _request_document_version_list_view(self):
        return self.get(
            viewname='documents:document_version_list',
            args=(self.document.pk,)
        )

    def test_document_version_list_no_permission(self):
        self._upload_new_version()
        response = self._request_document_version_list_view()
        self.assertEqual(response.status_code, 403)

    def test_document_version_list_with_access(self):
        self._upload_new_version()
        self.grant_access(
            obj=self.document, permission=permission_document_version_view
        )
        response = self._request_document_version_list_view()
        self.assertContains(
            response=response, text=TEST_VERSION_COMMENT, status_code=200
        )

    def _request_document_version_revert_view(self, document_version):
        return self.post(
            viewname='documents:document_version_revert',
            args=(document_version.pk,)
        )

    def test_document_version_revert_no_permission(self):
        first_version = self.document.latest_version
        self._upload_new_version()

        response = self._request_document_version_revert_view(
            document_version=first_version
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.document.versions.count(), 2)

    def test_document_version_revert_with_access(self):
        first_version = self.document.latest_version
        self._upload_new_version()

        self.grant_access(
            obj=self.document, permission=permission_document_version_revert
        )

        response = self._request_document_version_revert_view(
            document_version=first_version
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.document.versions.count(), 1)
