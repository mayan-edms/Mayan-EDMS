from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..models.document_type_models import DocumentType
from ..permissions import (
    permission_document_type_create, permission_document_type_delete,
    permission_document_type_edit
)

from .literals import (
    TEST_DOCUMENT_TYPE_LABEL, TEST_DOCUMENT_TYPE_LABEL_EDITED
)
from .mixins.document_mixins import DocumentTestMixin
from .mixins.document_type_mixins import DocumentTypeAPIViewTestMixin


class DocumentTypeAPIViewTestCase(
    DocumentTypeAPIViewTestMixin, DocumentTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False
    auto_create_test_document_type = False

    def test_document_type_create_api_view_no_permission(self):
        response = self._request_test_document_type_create_api_view()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(DocumentType.objects.all().count(), 0)

    def test_document_type_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_document_type_create)

        response = self._request_test_document_type_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(DocumentType.objects.all().count(), 1)
        self.assertEqual(
            DocumentType.objects.all().first().label,
            TEST_DOCUMENT_TYPE_LABEL
        )

    def test_document_type_delete_api_view_no_permission(self):
        self.test_document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

        response = self._request_test_document_type_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_type_delete_api_view_with_access(self):
        self.test_document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_delete
        )

        response = self._request_test_document_type_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(DocumentType.objects.all().count(), 0)

    def test_document_type_edit_via_patch_api_view_no_permission(self):
        self.test_document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

        response = self._request_test_document_type_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_type_edit_via_patch_api_view_with_access(self):
        self.test_document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        response = self._request_test_document_type_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_document_type.label, TEST_DOCUMENT_TYPE_LABEL_EDITED
        )

    def test_document_type_edit_via_put_api_view_no_permission(self):
        self._create_test_document_type()

        response = self._request_test_document_type_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_type_edit_via_put_api_view_with_access(self):
        self.test_document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        response = self._request_test_document_type_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_document_type.label, TEST_DOCUMENT_TYPE_LABEL_EDITED
        )
