from __future__ import unicode_literals

from ..permissions import (
    permission_document_version_revert, permission_document_version_view,
)

from .base import GenericDocumentViewTestCase
from .literals import TEST_VERSION_COMMENT
from .mixins import DocumentVersionTestMixin


class DocumentVersionTestCase(DocumentVersionTestMixin, GenericDocumentViewTestCase):
    def _request_document_version_list_view(self):
        return self.get(
            viewname='documents:document_version_list',
            kwargs={'pk': self.test_document.pk}
        )

    def test_document_version_list_no_permission(self):
        self._upload_new_version()

        response = self._request_document_version_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_version_list_with_access(self):
        self._upload_new_version()
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_view
        )

        response = self._request_document_version_list_view()
        self.assertContains(
            response=response, text=TEST_VERSION_COMMENT, status_code=200
        )

    def _request_document_version_revert_view(self, document_version):
        return self.post(
            viewname='documents:document_version_revert',
            kwargs={'pk': document_version.pk}
        )

    def test_document_version_revert_no_permission(self):
        first_version = self.test_document.latest_version
        self._upload_new_version()

        response = self._request_document_version_revert_view(
            document_version=first_version
        )
        self.assertEqual(response.status_code, 404)

        self.assertEqual(self.test_document.versions.count(), 2)

    def test_document_version_revert_with_access(self):
        first_version = self.test_document.latest_version
        self._upload_new_version()

        self.grant_access(
            obj=self.test_document, permission=permission_document_version_revert
        )

        response = self._request_document_version_revert_view(
            document_version=first_version
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.test_document.versions.count(), 1)
