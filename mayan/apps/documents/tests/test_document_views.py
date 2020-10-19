from django.test import override_settings

from mayan.apps.converter.layers import layer_saved_transformations
from mayan.apps.converter.permissions import permission_transformation_delete
from mayan.apps.converter.tests.mixins import LayerTestMixin

from ..models import Document, DocumentType
from ..permissions import (
    permission_document_create, permission_document_version_print,
    permission_document_properties_edit, permission_document_view
)

from .base import GenericDocumentViewTestCase
from .literals import TEST_DOCUMENT_TYPE_2_LABEL
from .mixins.document_mixins import DocumentViewTestMixin


class DocumentViewTestCase(
    LayerTestMixin, DocumentViewTestMixin, GenericDocumentViewTestCase
):
    def test_document_properties_view_no_permission(self):
        response = self._request_test_document_properties_view()
        self.assertEqual(response.status_code, 404)

    def test_document_properties_view_with_permissions(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_document_properties_view()
        self.assertContains(
            response=response, status_code=200, text=self.test_document.label
        )

    @override_settings(DOCUMENTS_LANGUAGE='fra')
    def test_document_properties_view_setting_non_us_language_with_permissions(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_document_properties_view()
        self.assertContains(
            response=response, status_code=200, text=self.test_document.label
        )
        self.assertContains(
            response=response, status_code=200,
            text='Language:</label>\n                \n                \n                    English'
        )

    @override_settings(DOCUMENTS_LANGUAGE='fra')
    def test_document_properties_edit_get_view_setting_non_us_language_with_permissions(self):
        self.grant_access(
            permission=permission_document_properties_edit,
            obj=self.test_document_type
        )
        response = self._request_test_document_properties_edit_get_view()
        self.assertContains(
            response=response, status_code=200,
            text='<option value="eng" selected>English</option>',
        )

    def test_document_list_view_no_permission(self):
        response = self._request_test_document_list_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['object_list'].count(), 0)

    def test_document_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_document_list_view()
        self.assertContains(
            response=response, status_code=200, text=self.test_document.label
        )

    def test_document_document_type_change_post_view_no_permission(self):
        self.assertEqual(
            self.test_document.document_type, self.test_document_type
        )

        document_type_2 = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2_LABEL
        )

        response = self._request_test_document_type_change_post_view(
            document_type=document_type_2
        )
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            Document.objects.get(pk=self.test_document.pk).document_type,
            self.test_document_type
        )

    def test_document_document_type_change_post_view_with_permissions(self):
        self.assertEqual(
            self.test_document.document_type, self.test_document_type
        )

        document_type_2 = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2_LABEL
        )

        self.grant_access(
            obj=self.test_document, permission=permission_document_properties_edit
        )
        self.grant_access(
            obj=document_type_2, permission=permission_document_create
        )

        response = self._request_test_document_type_change_post_view(
            document_type=document_type_2
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Document.objects.get(pk=self.test_document.pk).document_type,
            document_type_2
        )

    def test_document_document_type_change_view_get_no_permission(self):
        response = self._request_test_document_type_change_get_view(
        )
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            Document.objects.get(pk=self.test_document.pk).document_type,
            self.test_document_type
        )

    def test_document_document_type_change_view_get_with_permissions(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_properties_edit
        )
        response = self._request_test_document_type_change_get_view(
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            Document.objects.get(pk=self.test_document.pk).document_type,
            self.test_document_type
        )

    def test_document_multiple_document_type_change_view_no_permission(self):
        self.assertEqual(
            Document.objects.first().document_type, self.test_document_type
        )

        document_type_2 = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2_LABEL
        )

        response = self._request_test_document_multiple_type_change(
            document_type=document_type_2
        )
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            Document.objects.first().document_type, self.test_document_type
        )

    def test_document_multiple_document_type_change_view_with_permission(self):
        self.assertEqual(
            Document.objects.first().document_type, self.test_document_type
        )

        document_type_2 = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2_LABEL
        )

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_properties_edit
        )
        self.grant_access(
            obj=document_type_2, permission=permission_document_create
        )

        response = self._request_test_document_multiple_type_change(
            document_type=document_type_2
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Document.objects.first().document_type, document_type_2
        )
    '''
    def test_document_clear_transformations_view_no_permission(self):
        self._create_document_transformation()

        transformation_count = layer_saved_transformations.get_transformations_for(
            obj=self.test_document.pages.first()
        ).count()

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_document_clear_transformations_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            transformation_count,
            layer_saved_transformations.get_transformations_for(
                obj=self.test_document.pages.first()
            ).count()
        )

    def test_document_clear_transformations_view_with_access(self):
        self._create_document_transformation()

        transformation_count = layer_saved_transformations.get_transformations_for(
            obj=self.test_document.pages.first()
        ).count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_transformation_delete
        )
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_document_clear_transformations_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            transformation_count - 1,
            layer_saved_transformations.get_transformations_for(
                obj=self.test_document.pages.first()
            ).count()
        )

    def test_document_multiple_clear_transformations_view_no_permission(self):
        self._create_document_transformation()

        transformation_count = layer_saved_transformations.get_transformations_for(
            obj=self.test_document.pages.first()
        ).count()

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_document_multiple_clear_transformations()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            transformation_count,
            layer_saved_transformations.get_transformations_for(
                obj=self.test_document.pages.first()
            ).count()
        )

    def test_document_multiple_clear_transformations_view_with_access(self):
        self._create_document_transformation()

        transformation_count = layer_saved_transformations.get_transformations_for(
            obj=self.test_document.pages.first()
        ).count()

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_document, permission=permission_transformation_delete
        )

        response = self._request_test_document_multiple_clear_transformations()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            transformation_count - 1,
            layer_saved_transformations.get_transformations_for(
                obj=self.test_document.pages.first()
            ).count()
        )
    '''
    '''
    def test_document_print_form_view_no_permission(self):
        response = self._request_test_document_print_form_view()
        self.assertEqual(response.status_code, 404)

    def test_document_print_form_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_print
        )

        response = self._request_test_document_print_form_view()
        self.assertEqual(response.status_code, 200)

    def test_document_print_view_no_permission(self):
        response = self._request_test_document_print_view()
        self.assertEqual(response.status_code, 404)

    def test_document_print_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_print
        )

        response = self._request_test_document_print_view()
        self.assertEqual(response.status_code, 200)
    '''
    def test_document_preview_view_no_permission(self):
        response = self._request_test_document_preview_view()
        self.assertEqual(response.status_code, 404)

    def test_document_preview_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_document_preview_view()
        self.assertContains(
            response=response, status_code=200, text=self.test_document.label
        )
