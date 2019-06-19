from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text

from mayan.apps.converter.models import Transformation
from mayan.apps.converter.permissions import permission_transformation_delete

from ..models import DeletedDocument, Document, DocumentType
from ..permissions import (
    permission_document_create, permission_document_download,
    permission_document_print, permission_document_properties_edit,
    permission_document_tools, permission_document_view,
    permission_empty_trash
)

from .base import GenericDocumentViewTestCase
from .literals import (
    TEST_DOCUMENT_TYPE_2_LABEL, TEST_SMALL_DOCUMENT_FILENAME,
    TEST_TRANSFORMATION_ARGUMENT, TEST_TRANSFORMATION_NAME,
)
from .mixins import DocumentViewTestMixin


class DocumentsViewsTestCase(DocumentViewTestMixin, GenericDocumentViewTestCase):
    def test_document_view_no_permissions(self):
        response = self._request_document_properties_view()
        self.assertEqual(response.status_code, 404)

    def test_document_view_with_permissions(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_document_properties_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )

    def test_document_list_view_no_permissions(self):
        response = self._request_test_document_list_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['object_list'].count(), 0)

    def test_document_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_document_list_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )

    def test_document_document_type_change_post_view_no_permissions(self):
        self.assertEqual(
            self.test_document.document_type, self.test_document_type
        )

        document_type_2 = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2_LABEL
        )

        response = self._request_test_document_type_edit_post_view(
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

        response = self._request_test_document_type_edit_post_view(
            document_type=document_type_2
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Document.objects.get(pk=self.test_document.pk).document_type,
            document_type_2
        )

    def test_document_document_type_change_view_get_no_permissions(self):
        response = self._request_test_document_type_edit_get_view(
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
        response = self._request_test_document_type_edit_get_view(
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

        response = self._request_multiple_document_type_edit(
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

        response = self._request_multiple_document_type_edit(
            document_type=document_type_2
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Document.objects.first().document_type, document_type_2
        )

    def test_document_download_form_view_no_permission(self):
        response = self._request_document_download_form_view()
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )

    def test_document_download_form_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_download
        )

        response = self._request_document_download_form_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )

    def test_document_download_view_no_permission(self):
        response = self._request_document_download_view()
        self.assertEqual(response.status_code, 403)

    def test_document_download_view_with_permission(self):
        # Set the expected_content_type for
        # common.tests.mixins.ContentTypeCheckMixin
        self.expected_content_type = '{}; charset=utf-8'.format(
            self.test_document.file_mimetype
        )

        self.grant_access(
            obj=self.test_document, permission=permission_document_download
        )

        response = self._request_document_download_view()
        self.assertEqual(response.status_code, 200)

        with self.test_document.open() as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
                basename=TEST_SMALL_DOCUMENT_FILENAME,
                mime_type=self.test_document.file_mimetype
            )

    def test_document_multiple_download_view_no_permission(self):
        response = self._request_document_multiple_download_view()
        self.assertEqual(response.status_code, 403)

    def test_document_multiple_download_view_with_permission(self):
        # Set the expected_content_type for
        # common.tests.mixins.ContentTypeCheckMixin
        self.expected_content_type = '{}; charset=utf-8'.format(
            self.test_document.file_mimetype
        )
        self.grant_access(
            obj=self.test_document, permission=permission_document_download
        )

        response = self._request_document_multiple_download_view()
        self.assertEqual(response.status_code, 200)

        with self.test_document.open() as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
                basename=TEST_SMALL_DOCUMENT_FILENAME,
                mime_type=self.test_document.file_mimetype
            )

    def test_document_version_download_view_no_permission(self):
        response = self._request_document_version_download()
        self.assertEqual(response.status_code, 403)

    def test_document_version_download_view_with_permission(self):
        # Set the expected_content_type for
        # common.tests.mixins.ContentTypeCheckMixin
        self.expected_content_type = '{}; charset=utf-8'.format(
            self.test_document.latest_version.mimetype
        )

        self.grant_access(
            obj=self.test_document, permission=permission_document_download
        )

        response = self._request_document_version_download()
        self.assertEqual(response.status_code, 200)

        with self.test_document.open() as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
                basename=force_text(self.test_document.latest_version),
                mime_type='{}; charset=utf-8'.format(
                    self.test_document.latest_version.mimetype
                )
            )

    def test_document_version_download_preserve_extension_view_with_permission(self):
        # Set the expected_content_type for
        # common.tests.mixins.ContentTypeCheckMixin
        self.expected_content_type = '{}; charset=utf-8'.format(
            self.test_document.latest_version.mimetype
        )

        self.grant_access(
            obj=self.test_document, permission=permission_document_download
        )

        response = self._request_document_version_download(
            data={'preserve_extension': True}
        )
        self.assertEqual(response.status_code, 200)

        with self.test_document.open() as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
                basename=self.test_document.latest_version.get_rendered_string(
                    preserve_extension=True
                ), mime_type='{}; charset=utf-8'.format(
                    self.test_document.latest_version.mimetype
                )
            )

    def test_document_update_page_count_view_no_permission(self):
        self.test_document.pages.all().delete()
        self.assertEqual(self.test_document.pages.count(), 0)

        response = self._request_document_update_page_count_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(self.test_document.pages.count(), 0)

    def test_document_update_page_count_view_with_permission(self):
        # TODO: Revise permission association

        page_count = self.test_document.pages.count()
        self.test_document.pages.all().delete()
        self.assertEqual(self.test_document.pages.count(), 0)

        self.grant_permission(permission=permission_document_tools)

        response = self._request_document_update_page_count_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.test_document.pages.count(), page_count)

    def test_document_multiple_update_page_count_view_no_permission(self):
        self.test_document.pages.all().delete()
        self.assertEqual(self.test_document.pages.count(), 0)

        response = self._request_document_multiple_update_page_count_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(self.test_document.pages.count(), 0)

    def test_document_multiple_update_page_count_view_with_permission(self):
        page_count = self.test_document.pages.count()
        self.test_document.pages.all().delete()
        self.assertEqual(self.test_document.pages.count(), 0)

        self.grant_permission(permission=permission_document_tools)

        response = self._request_document_multiple_update_page_count_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.test_document.pages.count(), page_count)

    def test_document_clear_transformations_view_no_permission(self):
        document_page = self.test_document.pages.first()
        content_type = ContentType.objects.get_for_model(model=document_page)
        transformation = Transformation.objects.create(
            content_type=content_type, object_id=document_page.pk,
            name=TEST_TRANSFORMATION_NAME,
            arguments=TEST_TRANSFORMATION_ARGUMENT
        )

        self.assertQuerysetEqual(
            Transformation.objects.get_for_object(obj=document_page),
            (repr(transformation),)
        )

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_document_clear_transformations_view()
        self.assertEqual(response.status_code, 404)

        self.assertQuerysetEqual(
            Transformation.objects.get_for_object(obj=document_page),
            (repr(transformation),)
        )

    def test_document_clear_transformations_view_with_access(self):
        document_page = self.test_document.pages.first()
        content_type = ContentType.objects.get_for_model(model=document_page)
        transformation = Transformation.objects.create(
            content_type=content_type, object_id=document_page.pk,
            name=TEST_TRANSFORMATION_NAME,
            arguments=TEST_TRANSFORMATION_ARGUMENT
        )
        self.assertQuerysetEqual(
            Transformation.objects.get_for_object(obj=document_page),
            (repr(transformation),)
        )

        self.grant_access(
            obj=self.test_document, permission=permission_transformation_delete
        )
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_document_clear_transformations_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Transformation.objects.get_for_object(obj=document_page).count(), 0
        )

    def test_document_multiple_clear_transformations_view_no_permission(self):
        document_page = self.test_document.pages.first()
        content_type = ContentType.objects.get_for_model(model=document_page)
        transformation = Transformation.objects.create(
            content_type=content_type, object_id=document_page.pk,
            name=TEST_TRANSFORMATION_NAME,
            arguments=TEST_TRANSFORMATION_ARGUMENT
        )

        self.assertQuerysetEqual(
            Transformation.objects.get_for_object(obj=document_page),
            (repr(transformation),)
        )

        self.grant_permission(permission=permission_document_view)

        response = self._request_document_multiple_clear_transformations()
        self.assertEqual(response.status_code, 404)
        self.assertQuerysetEqual(
            Transformation.objects.get_for_object(obj=document_page),
            (repr(transformation),)
        )

    def test_document_multiple_clear_transformations_view_with_access(self):
        document_page = self.test_document.pages.first()
        content_type = ContentType.objects.get_for_model(model=document_page)
        transformation = Transformation.objects.create(
            content_type=content_type, object_id=document_page.pk,
            name=TEST_TRANSFORMATION_NAME,
            arguments=TEST_TRANSFORMATION_ARGUMENT
        )

        self.assertQuerysetEqual(
            Transformation.objects.get_for_object(obj=document_page),
            (repr(transformation),)
        )

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_document, permission=permission_transformation_delete
        )

        response = self._request_document_multiple_clear_transformations()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Transformation.objects.get_for_object(obj=document_page).count(), 0
        )

    def test_trash_can_empty_view_no_permission(self):
        self.test_document.delete()
        self.assertEqual(DeletedDocument.objects.count(), 1)

        response = self._request_empty_trash_view()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(DeletedDocument.objects.count(), 1)

    def test_trash_can_empty_view_with_permission(self):
        self.test_document.delete()
        self.assertEqual(DeletedDocument.objects.count(), 1)

        self.grant_permission(permission=permission_empty_trash)

        response = self._request_empty_trash_view()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DeletedDocument.objects.count(), 0)
        self.assertEqual(Document.objects.count(), 0)

    def test_document_print_view_no_access(self):
        response = self._request_document_print_view()
        self.assertEqual(response.status_code, 403)

    def test_document_print_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_print
        )

        response = self._request_document_print_view()
        self.assertEqual(response.status_code, 200)
