# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text

from converter.models import Transformation
from converter.permissions import permission_transformation_delete

from ..literals import PAGE_RANGE_ALL
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


class DocumentsViewsTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(DocumentsViewsTestCase, self).setUp()
        self.login_user()

    def test_document_view_no_permissions(self):
        response = self.get(
            'documents:document_properties', args=(self.document.pk,)
        )

        self.assertEqual(response.status_code, 403)

    def test_document_view_with_permissions(self):
        self.grant_access(
            obj=self.document, permission=permission_document_view
        )
        response = self.get(
            'documents:document_properties', args=(self.document.pk,),
            follow=True
        )

        self.assertContains(
            response, 'roperties for document', status_code=200
        )

    def test_document_list_view_no_permissions(self):
        response = self.get('documents:document_list')
        self.assertContains(response, 'Total: 0', status_code=200)

    def test_document_list_view_with_access(self):
        self.grant_access(
            obj=self.document, permission=permission_document_view
        )
        response = self.get('documents:document_list')
        self.assertContains(response, self.document.label, status_code=200)

    def _request_document_type_edit(self, document_type):
        return self.post(
            'documents:document_document_type_edit',
            args=(self.document.pk,),
            data={'document_type': document_type.pk}
        )

    def test_document_document_type_change_view_no_permissions(self):
        self.assertEqual(
            self.document.document_type, self.document_type
        )

        document_type_2 = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2_LABEL
        )

        response = self._request_document_type_edit(
            document_type=document_type_2
        )

        self.assertContains(
            response, text='Select a valid choice', status_code=200
        )

        self.assertEqual(
            Document.objects.get(pk=self.document.pk).document_type,
            self.document_type
        )

    def test_document_document_type_change_view_with_permissions(self):
        self.assertEqual(
            self.document.document_type, self.document_type
        )

        document_type_2 = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2_LABEL
        )

        self.grant_access(
            obj=self.document, permission=permission_document_properties_edit
        )
        self.grant_access(
            obj=document_type_2, permission=permission_document_create
        )

        response = self._request_document_type_edit(
            document_type=document_type_2
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Document.objects.get(pk=self.document.pk).document_type,
            document_type_2
        )

    def _request_multiple_document_type_edit(self, document_type):
        return self.post(
            'documents:document_multiple_document_type_edit',
            data={
                'id_list': self.document.pk,
                'document_type': document_type.pk
            }
        )

    def test_document_multiple_document_type_change_view_no_permission(self):
        self.assertEqual(
            Document.objects.first().document_type, self.document_type
        )

        document_type_2 = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2_LABEL
        )

        response = self._request_multiple_document_type_edit(
            document_type=document_type_2
        )

        self.assertContains(
            response, text='Select a valid choice.', status_code=200
        )

        self.assertEqual(
            Document.objects.first().document_type, self.document_type
        )

    def test_document_multiple_document_type_change_view_with_permission(self):
        self.assertEqual(
            Document.objects.first().document_type, self.document_type
        )

        document_type_2 = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2_LABEL
        )

        self.grant_access(
            obj=self.document, permission=permission_document_properties_edit
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

    def _request_document_download_form_view(self):
        return self.get(
            'documents:document_download_form', args=(self.document.pk,),
            follow=True,
        )

    def test_document_download_form_view_no_permission(self):
        response = self._request_document_download_form_view()

        self.assertNotContains(
            response, text=self.document.label, status_code=200
        )

    def test_document_download_form_view_with_access(self):
        self.grant_access(
            obj=self.document, permission=permission_document_download
        )
        response = self._request_document_download_form_view()

        self.assertContains(
            response, text=self.document.label, status_code=200
        )

    def test_document_download_view_no_permission(self):
        response = self.get(
            'documents:document_download', args=(self.document.pk,)
        )

        self.assertEqual(response.status_code, 403)

    def test_document_download_view_with_permission(self):
        # Set the expected_content_type for
        # common.tests.mixins.ContentTypeCheckMixin
        self.expected_content_type = '{}; charset=utf-8'.format(
            self.document.file_mimetype
        )

        self.grant_access(
            obj=self.document, permission=permission_document_download
        )
        response = self.get(
            'documents:document_download', args=(self.document.pk,)
        )

        self.assertEqual(response.status_code, 200)

        with self.document.open() as file_object:
            self.assert_download_response(
                response, content=file_object.read(),
                basename=TEST_SMALL_DOCUMENT_FILENAME,
                mime_type=self.document.file_mimetype
            )

    def test_document_multiple_download_view_no_permission(self):
        response = self.get(
            'documents:document_multiple_download',
            data={'id_list': self.document.pk}
        )

        self.assertEqual(response.status_code, 403)

    def test_document_multiple_download_view_with_permission(self):
        # Set the expected_content_type for
        # common.tests.mixins.ContentTypeCheckMixin
        self.expected_content_type = '{}; charset=utf-8'.format(
            self.document.file_mimetype
        )
        self.grant_access(
            obj=self.document, permission=permission_document_download
        )

        response = self.get(
            'documents:document_multiple_download',
            data={'id_list': self.document.pk}
        )

        self.assertEqual(response.status_code, 200)

        with self.document.open() as file_object:
            self.assert_download_response(
                response, content=file_object.read(),
                basename=TEST_SMALL_DOCUMENT_FILENAME,
                mime_type=self.document.file_mimetype
            )

    def _request_document_version_download(self, data=None):
        data = data or {}
        return self.get(
            'documents:document_version_download', args=(
                self.document.latest_version.pk,
            ), data=data
        )

    def test_document_version_download_view_no_permission(self):
        response = self._request_document_version_download()

        self.assertEqual(response.status_code, 403)

    def test_document_version_download_view_with_permission(self):
        # Set the expected_content_type for
        # common.tests.mixins.ContentTypeCheckMixin
        self.expected_content_type = '{}; charset=utf-8'.format(
            self.document.latest_version.mimetype
        )

        self.grant_access(
            obj=self.document, permission=permission_document_download
        )
        response = self._request_document_version_download()

        self.assertEqual(response.status_code, 200)

        with self.document.open() as file_object:
            self.assert_download_response(
                response, content=file_object.read(),
                basename=force_text(self.document.latest_version),
                mime_type='{}; charset=utf-8'.format(
                    self.document.latest_version.mimetype
                )
            )

    def test_document_version_download_preserve_extension_view_with_permission(self):
        # Set the expected_content_type for
        # common.tests.mixins.ContentTypeCheckMixin
        self.expected_content_type = '{}; charset=utf-8'.format(
            self.document.latest_version.mimetype
        )

        self.grant_access(
            obj=self.document, permission=permission_document_download
        )
        response = self._request_document_version_download(
            data={'preserve_extension': True}
        )

        self.assertEqual(response.status_code, 200)

        with self.document.open() as file_object:
            self.assert_download_response(
                response, content=file_object.read(),
                basename=self.document.latest_version.get_rendered_string(
                    preserve_extension=True
                ), mime_type='{}; charset=utf-8'.format(
                    self.document.latest_version.mimetype
                )
            )

    def test_document_update_page_count_view_no_permission(self):
        self.document.pages.all().delete()
        self.assertEqual(self.document.pages.count(), 0)

        response = self.post(
            'documents:document_update_page_count', args=(self.document.pk,)
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.document.pages.count(), 0)

    def test_document_update_page_count_view_with_permission(self):
        # TODO: Revise permission association

        page_count = self.document.pages.count()
        self.document.pages.all().delete()
        self.assertEqual(self.document.pages.count(), 0)

        self.grant_permission(permission=permission_document_tools)

        response = self.post(
            'documents:document_update_page_count',
            args=(self.document.pk,)
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.document.pages.count(), page_count)

    def test_document_multiple_update_page_count_view_no_permission(self):
        self.document.pages.all().delete()
        self.assertEqual(self.document.pages.count(), 0)

        response = self.post(
            'documents:document_multiple_update_page_count',
            data={'id_list': self.document.pk}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.document.pages.count(), 0)

    def test_document_multiple_update_page_count_view_with_permission(self):
        page_count = self.document.pages.count()
        self.document.pages.all().delete()
        self.assertEqual(self.document.pages.count(), 0)

        self.grant_permission(permission=permission_document_tools)

        response = self.post(
            'documents:document_multiple_update_page_count',
            data={'id_list': self.document.pk}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.document.pages.count(), page_count)

    def test_document_clear_transformations_view_no_permission(self):
        document_page = self.document.pages.first()
        content_type = ContentType.objects.get_for_model(document_page)
        transformation = Transformation.objects.create(
            content_type=content_type, object_id=document_page.pk,
            name=TEST_TRANSFORMATION_NAME,
            arguments=TEST_TRANSFORMATION_ARGUMENT
        )

        self.assertQuerysetEqual(
            Transformation.objects.get_for_model(document_page),
            (repr(transformation),)
        )

        self.grant_access(
            obj=self.document, permission=permission_document_view
        )

        response = self.post(
            'documents:document_clear_transformations',
            args=(self.document.pk,)
        )

        self.assertEqual(response.status_code, 302)
        self.assertQuerysetEqual(
            Transformation.objects.get_for_model(document_page),
            (repr(transformation),)
        )

    def test_document_clear_transformations_view_with_access(self):
        document_page = self.document.pages.first()
        content_type = ContentType.objects.get_for_model(document_page)
        transformation = Transformation.objects.create(
            content_type=content_type, object_id=document_page.pk,
            name=TEST_TRANSFORMATION_NAME,
            arguments=TEST_TRANSFORMATION_ARGUMENT
        )
        self.assertQuerysetEqual(
            Transformation.objects.get_for_model(document_page),
            (repr(transformation),)
        )

        self.grant_access(
            obj=self.document, permission=permission_transformation_delete
        )
        self.grant_access(
            obj=self.document, permission=permission_document_view
        )

        response = self.post(
            'documents:document_clear_transformations',
            args=(self.document.pk,)
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Transformation.objects.get_for_model(document_page).count(), 0
        )

    def test_document_multiple_clear_transformations_view_no_permission(self):
        document_page = self.document.pages.first()
        content_type = ContentType.objects.get_for_model(document_page)
        transformation = Transformation.objects.create(
            content_type=content_type, object_id=document_page.pk,
            name=TEST_TRANSFORMATION_NAME,
            arguments=TEST_TRANSFORMATION_ARGUMENT
        )

        self.assertQuerysetEqual(
            Transformation.objects.get_for_model(document_page),
            (repr(transformation),)
        )

        self.grant_permission(permission=permission_document_view)

        response = self.post(
            'documents:document_multiple_clear_transformations',
            data={'id_list': self.document.pk}
        )

        self.assertEqual(response.status_code, 302)
        self.assertQuerysetEqual(
            Transformation.objects.get_for_model(document_page),
            (repr(transformation),)
        )

    def test_document_multiple_clear_transformations_view_with_access(self):
        document_page = self.document.pages.first()
        content_type = ContentType.objects.get_for_model(document_page)
        transformation = Transformation.objects.create(
            content_type=content_type, object_id=document_page.pk,
            name=TEST_TRANSFORMATION_NAME,
            arguments=TEST_TRANSFORMATION_ARGUMENT
        )

        self.assertQuerysetEqual(
            Transformation.objects.get_for_model(document_page),
            (repr(transformation),)
        )

        self.grant_access(
            obj=self.document, permission=permission_document_view
        )
        self.grant_access(
            obj=self.document, permission=permission_transformation_delete
        )

        response = self.post(
            'documents:document_multiple_clear_transformations',
            data={'id_list': self.document.pk}, follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Transformation.objects.get_for_model(document_page).count(), 0
        )

    def _empty_trash(self):
        return self.post('documents:trash_can_empty')

    def test_trash_can_empty_view_no_permission(self):
        self.document.delete()
        self.assertEqual(DeletedDocument.objects.count(), 1)

        response = self._empty_trash()

        self.assertEqual(response.status_code, 403)

        self.assertEqual(DeletedDocument.objects.count(), 1)

    def test_trash_can_empty_view_with_permission(self):
        self.document.delete()
        self.assertEqual(DeletedDocument.objects.count(), 1)

        self.grant_permission(permission=permission_empty_trash)

        response = self._empty_trash()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(DeletedDocument.objects.count(), 0)
        self.assertEqual(Document.objects.count(), 0)

    def test_document_page_view_no_permissions(self):
        response = self.get(
            'documents:document_page_view', args=(
                self.document.pages.first().pk,
            )
        )

        self.assertEqual(response.status_code, 403)

    def test_document_page_view_with_access(self):
        self.grant_access(
            obj=self.document, permission=permission_document_view
        )
        response = self.get(
            'documents:document_page_view', args=(
                self.document.pages.first().pk,
            ),
            follow=True
        )

        self.assertContains(
            response, force_text(self.document.pages.first()), status_code=200
        )

    def _request_print_view(self):
        return self.get(
            'documents:document_print', args=(
                self.document.pk,
            ), data={
                'page_group': PAGE_RANGE_ALL
            }
        )

    def test_document_print_view_no_access(self):
        response = self ._request_print_view()
        self.assertEqual(response.status_code, 403)

    def test_document_print_view_with_access(self):
        self.grant_access(
            obj=self.document, permission=permission_document_print
        )
        response = self._request_print_view()
        self.assertEqual(response.status_code, 200)
