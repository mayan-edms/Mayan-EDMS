from django.utils.encoding import force_text

from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..models import Document, DocumentType
from ..permissions import (
    permission_document_create, permission_document_file_download,
    permission_trashed_document_delete, permission_document_edit,
    permission_document_file_delete, permission_document_file_view,
    permission_document_file_new, permission_document_properties_edit,
    permission_trashed_document_restore, permission_document_trash,
    permission_document_view, permission_document_type_create,
    permission_document_type_delete, permission_document_type_edit,
    permission_document_version_create, permission_document_version_delete,
    permission_document_version_edit, permission_document_version_view,
    permission_document_version_export
)

from .literals import (
    TEST_DOCUMENT_DESCRIPTION_EDITED, TEST_PDF_DOCUMENT_FILENAME,
    TEST_DOCUMENT_TYPE_LABEL, TEST_DOCUMENT_TYPE_2_LABEL,
    TEST_DOCUMENT_TYPE_LABEL_EDITED, TEST_DOCUMENT_VERSION_COMMENT_EDITED,
    TEST_SMALL_DOCUMENT_FILENAME
)
from .mixins.document_mixins import (
    DocumentAPIViewTestMixin, DocumentTestMixin
)
from .mixins.document_file_mixins import (
    DocumentFileAPIViewTestMixin, DocumentFileTestMixin,
    DocumentFilePageAPIViewTestMixin
)
from .mixins.document_type_mixins import DocumentTypeAPIViewTestMixin
from .mixins.document_version_mixins import (
    DocumentVersionAPIViewTestMixin, DocumentVersionTestMixin,
    DocumentVersionPageAPIViewTestMixin
)
from .mixins.trashed_document_mixins import TrashedDocumentAPIViewTestMixin


class DocumentVersionAPIViewTestCase(
    DocumentVersionAPIViewTestMixin, DocumentTestMixin,
    DocumentVersionTestMixin, BaseAPITestCase
):
    def test_document_version_create_api_view_no_permission(self):
        response = self._request_test_document_version_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(self.test_document.versions.count(), 1)
        self.assertEqual(self.test_document.page_count, 1)

    def test_document_version_create_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_create
        )

        response = self._request_test_document_version_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(self.test_document.versions.count(), 2)
        self.assertEqual(self.test_document.page_count, 0)

    def test_document_version_delete_api_view_no_permission(self):
        response = self._request_test_document_version_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(self.test_document.versions.count(), 1)

    def test_document_version_delete_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_delete
        )

        response = self._request_test_document_version_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(self.test_document.versions.count(), 0)

    def test_document_version_edit_via_patch_api_view_no_permission(self):
        response = self._request_test_document_version_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_version_edit_via_patch_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_edit
        )
        response = self._request_test_document_version_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_document.latest_version.refresh_from_db()
        self.assertEqual(self.test_document.versions.count(), 1)
        self.assertEqual(
            self.test_document.latest_version.comment,
            TEST_DOCUMENT_VERSION_COMMENT_EDITED
        )
    def test_document_version_edit_via_put_api_view_no_permission(self):
        response = self._request_test_document_version_edit_via_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_version_edit_via_put_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_edit
        )

        response = self._request_test_document_version_edit_via_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document.latest_version.refresh_from_db()
        self.assertEqual(self.test_document.versions.count(), 1)
        self.assertEqual(
            self.test_document.latest_version.comment,
            TEST_DOCUMENT_VERSION_COMMENT_EDITED
        )

    def test_document_version_export_api_view_no_permission(self):
        response = self._request_test_document_version_export_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_version_export_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_export
        )

        response = self._request_test_document_version_export_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with self.test_document.latest_version.open() as version_object:
            self.assert_export_response(
                response=response, content=version_object.read(),
                versionname=force_text(self.test_document.latest_version),
                mime_type=self.test_document.latest_version.mimetype
            )

    def test_document_version_list_api_view_no_permission(self):
        response = self._request_test_document_version_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_version_list_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_view
        )
        response = self._request_test_document_version_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['results'][0]['id'],
            self.test_document.latest_version.id
        )


class DocumentVersionPageAPIViewTestCase(
    DocumentVersionPageAPIViewTestMixin, DocumentTestMixin, BaseAPITestCase
):
    def test_document_version_page_image_api_view_no_permission(self):
        response = self._request_test_document_version_page_image_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_version_page_image_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_view
        )

        response = self._request_test_document_version_page_image_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
