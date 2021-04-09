import os

from ..models import DocumentType
from ..permissions import (
    permission_document_properties_edit,
    permission_document_type_create, permission_document_type_delete,
    permission_document_type_edit, permission_document_type_view,
)

from .base import GenericDocumentViewTestCase
from .literals import (
    TEST_DOCUMENT_TYPE_LABEL, TEST_DOCUMENT_TYPE_QUICK_LABEL,
    TEST_DOCUMENT_TYPE_QUICK_LABEL_EDITED
)
from .mixins.document_type_mixins import (
    DocumentQuickLabelViewTestMixin,
    DocumentTypeDeletionPoliciesViewTestMixin,
    DocumentTypeFilenameGeneratorViewTestMixin,
    DocumentTypeQuickLabelTestMixin, DocumentTypeQuickLabelViewTestMixin,
    DocumentTypeViewTestMixin
)


class DocumentTypeDeletionPoliciesViewTestCase(
    DocumentTypeDeletionPoliciesViewTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_document_type_deletion_policies_get_view_no_permission(self):
        response = self._request_test_document_type_policies_get_view()
        self.assertEqual(response.status_code, 404)

    def test_document_type_deletion_policies_get_view_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        response = self._request_test_document_type_policies_get_view()
        self.assertEqual(response.status_code, 200)

    def test_document_type_deletion_policies_post_view_no_permission(self):
        response = self._request_test_document_type_policies_post_view()
        self.assertEqual(response.status_code, 404)

    def test_document_type_deletion_policies_post_view_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        response = self._request_test_document_type_policies_post_view()
        self.assertEqual(response.status_code, 302)


class DocumentTypeFilenameGeneratorViewTestCase(
    DocumentTypeFilenameGeneratorViewTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_document_type_filename_generator_get_view_no_permission(self):
        response = self._request_test_document_type_filename_generator_get_view()
        self.assertEqual(response.status_code, 404)

    def test_document_type_filename_generator_get_view_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        response = self._request_test_document_type_filename_generator_get_view()
        self.assertEqual(response.status_code, 200)

    def test_document_type_filename_generator_post_view_no_permission(self):
        response = self._request_test_document_type_filename_generator_post_view()
        self.assertEqual(response.status_code, 404)

    def test_document_type_filename_generator_post_view_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        response = self._request_test_document_type_filename_generator_post_view()
        self.assertEqual(response.status_code, 302)


class DocumentTypeViewsTestCase(
    DocumentTypeViewTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_document_type_create_view_no_permission(self):
        self.test_document_type.delete()

        response = self._request_test_document_type_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(DocumentType.objects.count(), 0)

    def test_document_type_create_view_with_permission(self):
        self.test_document_type.delete()
        self.grant_permission(permission=permission_document_type_create)

        response = self._request_test_document_type_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(DocumentType.objects.count(), 1)
        self.assertEqual(
            DocumentType.objects.first().label, TEST_DOCUMENT_TYPE_LABEL
        )

    def test_document_type_delete_view_no_permission(self):
        response = self._request_test_document_type_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(DocumentType.objects.count(), 1)

    def test_document_type_delete_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_delete
        )

        response = self._request_test_document_type_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(DocumentType.objects.count(), 0)

    def test_document_type_edit_view_no_permission(self):
        test_document_type_label = self.test_document_type.label

        response = self._request_test_document_type_edit_view()

        self.assertEqual(response.status_code, 404)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_document_type.label, test_document_type_label
        )

    def test_document_type_edit_view_with_access(self):
        test_document_type_label = self.test_document_type.label

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        response = self._request_test_document_type_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_document_type.refresh_from_db()
        self.assertNotEqual(
            self.test_document_type.label, test_document_type_label
        )

    def test_document_type_list_view_no_permission(self):
        response = self._request_test_document_type_list_view()
        self.assertNotContains(
            response=response, status_code=200, text=self.test_document_type
        )

    def test_document_type_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_view
        )

        response = self._request_test_document_type_list_view()
        self.assertContains(
            response=response, status_code=200, text=self.test_document_type
        )


class DocumentTypeQuickLabelViewsTestCase(
    DocumentTypeQuickLabelTestMixin, DocumentTypeQuickLabelViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_document_type_quick_label_create_no_permission(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_view
        )

        response = self._request_test_quick_label_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(self.test_document_type.filenames.count(), 0)

    def test_document_type_quick_label_create_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        response = self._request_test_quick_label_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.test_document_type.filenames.count(), 1)

    def test_document_type_quick_label_delete_no_permission(self):
        self._create_test_document_type_quick_label()
        response = self._request_test_quick_label_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document_type.filenames.count(), 1
        )

    def test_document_type_quick_label_delete_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self._create_test_document_type_quick_label()

        response = self._request_test_quick_label_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document_type.filenames.count(), 0
        )

    def test_document_type_quick_label_edit_no_permission(self):
        self._create_test_document_type_quick_label()

        response = self._request_test_quick_label_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_document_type_quick_label.refresh_from_db()
        self.assertEqual(
            self.test_document_type_quick_label.filename,
            TEST_DOCUMENT_TYPE_QUICK_LABEL
        )

    def test_document_type_quick_label_edit_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self._create_test_document_type_quick_label()

        response = self._request_test_quick_label_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_document_type_quick_label.refresh_from_db()
        self.assertEqual(
            self.test_document_type_quick_label.filename,
            TEST_DOCUMENT_TYPE_QUICK_LABEL_EDITED
        )

    def test_document_type_quick_label_list_no_permission(self):
        self._create_test_document_type_quick_label()

        response = self._request_test_quick_label_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_type_quick_label_list_with_access(self):
        self._create_test_document_type_quick_label()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_view
        )

        response = self._request_test_quick_label_list_view()
        self.assertContains(
            response, status_code=200, text=self.test_document_type_quick_label
        )


class DocumentsQuickLabelViewTestCase(
    DocumentQuickLabelViewTestMixin, DocumentTypeQuickLabelTestMixin,
    GenericDocumentViewTestCase
):
    def test_document_quick_label_no_permission(self):
        self._create_test_document_type_quick_label()

        response = self._request_test_document_quick_label_edit_view()
        self.assertEqual(response.status_code, 404)

    def test_document_quick_label_with_access(self):
        self._create_test_document_type_quick_label()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_properties_edit
        )

        response = self._request_test_document_quick_label_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_document.refresh_from_db()
        self.assertEqual(
            self.test_document.label,
            self.test_document_type_quick_label.filename
        )

    def test_document_quick_label_preserve_extension_with_access(self):
        self._create_test_document_type_quick_label()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_properties_edit
        )
        filename, extension = os.path.splitext(self.test_document.label)

        response = self._request_test_document_quick_label_edit_view(
            extra_data={'preserve_extension': True}
        )
        self.assertEqual(response.status_code, 302)

        self.test_document.refresh_from_db()
        self.assertEqual(
            self.test_document.label, '{}{}'.format(
                self.test_document_type_quick_label.filename, extension
            )
        )

    def test_document_quick_label_no_preserve_extension_with_access(self):
        self._create_test_document_type_quick_label()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_properties_edit
        )
        filename, extension = os.path.splitext(self.test_document.label)

        response = self._request_test_document_quick_label_edit_view(
            extra_data={'preserve_extension': False}
        )
        self.assertEqual(response.status_code, 302)

        self.test_document.refresh_from_db()
        self.assertEqual(
            self.test_document.label, self.test_document_type_quick_label.filename
        )
