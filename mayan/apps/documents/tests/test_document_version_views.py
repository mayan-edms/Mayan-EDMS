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

    def test_document_version_list_no_permission(self):
        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document.new_version(
                comment=TEST_VERSION_COMMENT, file_object=file_object
            )

        response = self.get(
            'documents:document_version_list', args=(self.document.pk,)
        )

        self.assertEqual(response.status_code, 403)

    def test_document_version_list_with_access(self):
        self.grant_access(
            obj=self.document, permission=permission_document_version_view
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document.new_version(
                comment=TEST_VERSION_COMMENT, file_object=file_object
            )

        response = self.get(
            'documents:document_version_list', args=(self.document.pk,)
        )

        self.assertContains(response, TEST_VERSION_COMMENT, status_code=200)

    def test_document_version_revert_no_permission(self):
        first_version = self.document.latest_version

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document.new_version(
                file_object=file_object
            )

        response = self.post(
            'documents:document_version_revert', args=(first_version.pk,)
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.document.versions.count(), 2)

    def test_document_version_revert_with_access(self):
        first_version = self.document.latest_version

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document.new_version(
                file_object=file_object
            )

        self.grant_access(
            obj=self.document, permission=permission_document_version_revert
        )

        response = self.post(
            'documents:document_version_revert', args=(first_version.pk,),
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.document.versions.count(), 1)
