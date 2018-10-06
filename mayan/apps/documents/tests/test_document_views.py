# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

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
from .mixins import DocumentTypeQuickLabelTestMixin


class DocumentsViewsTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(DocumentsViewsTestCase, self).setUp()
        self.login_user()

    def _request_document_properties_view(self):
        return self.get(
            viewname='documents:document_properties',
            args=(self.document.pk,)
        )

    def test_document_view_no_permissions(self):
        response = self._request_document_properties_view()
        self.assertEqual(response.status_code, 403)

    def test_document_view_with_permissions(self):
        self.grant_access(
            obj=self.document, permission=permission_document_view
        )
        response = self._request_document_properties_view()
        self.assertContains(
            response=response, text=self.document.label, status_code=200
        )

    def _request_document_list_view(self):
        return self.get(viewname='documents:document_list')

    def test_document_list_view_no_permissions(self):
        response = self._request_document_list_view()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object_list'].count(), 0)

    def test_document_list_view_with_access(self):
        self.grant_access(
            obj=self.document, permission=permission_document_view
        )
        response = self._request_document_list_view()
        self.assertContains(
            response=response, text=self.document.label, status_code=200
        )

    def _request_document_type_edit(self, document_type):
        return self.post(
            viewname='documents:document_document_type_edit',
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
            response=response, text='Select a valid choice', status_code=200
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
            viewname='documents:document_multiple_document_type_edit',
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
            response=response, text='Select a valid choice.', status_code=200
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
            viewname='documents:document_download_form',
            args=(self.document.pk,),
        )

    def test_document_download_form_view_no_permission(self):
        response = self._request_document_download_form_view()

        self.assertNotContains(
            response=response, text=self.document.label, status_code=200
        )

    def test_document_download_form_view_with_access(self):
        self.grant_access(
            obj=self.document, permission=permission_document_download
        )
        response = self._request_document_download_form_view()

        self.assertContains(
            response=response, text=self.document.label, status_code=200
        )

    def _request_document_download_view(self):
        return self.get(
            viewname='documents:document_download', args=(self.document.pk,)
        )

    def test_document_download_view_no_permission(self):
        response = self._request_document_download_view()
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
        response = self._request_document_download_view()
        self.assertEqual(response.status_code, 200)

        with self.document.open() as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
                basename=TEST_SMALL_DOCUMENT_FILENAME,
                mime_type=self.document.file_mimetype
            )

    def _request_document_multiple_download_view(self):
        return self.get(
            viewname='documents:document_multiple_download',
            data={'id_list': self.document.pk}
        )

    def test_document_multiple_download_view_no_permission(self):
        response = self._request_document_multiple_download_view()
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

        response = self._request_document_multiple_download_view()
        self.assertEqual(response.status_code, 200)

        with self.document.open() as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
                basename=TEST_SMALL_DOCUMENT_FILENAME,
                mime_type=self.document.file_mimetype
            )

    def _request_document_version_download(self, data=None):
        data = data or {}
        return self.get(
            viewname='documents:document_version_download', args=(
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
                response=response, content=file_object.read(),
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
                response=response, content=file_object.read(),
                basename=self.document.latest_version.get_rendered_string(
                    preserve_extension=True
                ), mime_type='{}; charset=utf-8'.format(
                    self.document.latest_version.mimetype
                )
            )

    def _request_document_update_page_count_view(self):
        return self.post(
            viewname='documents:document_update_page_count',
            args=(self.document.pk,)
        )

    def test_document_update_page_count_view_no_permission(self):
        self.document.pages.all().delete()
        self.assertEqual(self.document.pages.count(), 0)

        response = self._request_document_update_page_count_view()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.document.pages.count(), 0)

    def test_document_update_page_count_view_with_permission(self):
        # TODO: Revise permission association

        page_count = self.document.pages.count()
        self.document.pages.all().delete()
        self.assertEqual(self.document.pages.count(), 0)

        self.grant_permission(permission=permission_document_tools)

        response = self._request_document_update_page_count_view()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.document.pages.count(), page_count)

    def _request_document_multiple_update_page_count_view(self):
        return self.post(
            viewname='documents:document_multiple_update_page_count',
            data={'id_list': self.document.pk}
        )

    def test_document_multiple_update_page_count_view_no_permission(self):
        self.document.pages.all().delete()
        self.assertEqual(self.document.pages.count(), 0)

        response = self._request_document_multiple_update_page_count_view()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.document.pages.count(), 0)

    def test_document_multiple_update_page_count_view_with_permission(self):
        page_count = self.document.pages.count()
        self.document.pages.all().delete()
        self.assertEqual(self.document.pages.count(), 0)

        self.grant_permission(permission=permission_document_tools)

        response = self._request_document_multiple_update_page_count_view()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.document.pages.count(), page_count)

    def _request_document_clear_transformations_view(self):
        return self.post(
            viewname='documents:document_clear_transformations',
            args=(self.document.pk,)
        )

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

        response = self._request_document_clear_transformations_view()
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

        response = self._request_document_clear_transformations_view()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Transformation.objects.get_for_model(document_page).count(), 0
        )

    def _request_document_multiple_clear_transformations(self):
        return self.post(
            viewname='documents:document_multiple_clear_transformations',
            data={'id_list': self.document.pk}
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

        response = self._request_document_multiple_clear_transformations()
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

        response = self._request_document_multiple_clear_transformations()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Transformation.objects.get_for_model(document_page).count(), 0
        )

    def _request_empty_trash_view(self):
        return self.post(viewname='documents:trash_can_empty')

    def test_trash_can_empty_view_no_permission(self):
        self.document.delete()
        self.assertEqual(DeletedDocument.objects.count(), 1)

        response = self._request_empty_trash_view()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(DeletedDocument.objects.count(), 1)

    def test_trash_can_empty_view_with_permission(self):
        self.document.delete()
        self.assertEqual(DeletedDocument.objects.count(), 1)

        self.grant_permission(permission=permission_empty_trash)

        response = self._request_empty_trash_view()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DeletedDocument.objects.count(), 0)
        self.assertEqual(Document.objects.count(), 0)

    def _request_document_page_view(self, document_page):
        return self.get(
            viewname='documents:document_page_view', args=(
                document_page.pk,
            )
        )

    def test_document_page_view_no_permissions(self):
        response = self._request_document_page_view(
            document_page=self.document.pages.first()
        )
        self.assertEqual(response.status_code, 403)

    def test_document_page_view_with_access(self):
        self.grant_access(
            obj=self.document, permission=permission_document_view
        )
        response = self._request_document_page_view(
            document_page=self.document.pages.first()
        )
        self.assertContains(
            response=response, text=force_text(self.document.pages.first()),
            status_code=200
        )

    def _request_document_print_view(self):
        return self.get(
            viewname='documents:document_print', args=(
                self.document.pk,
            ), data={
                'page_group': PAGE_RANGE_ALL
            }
        )

    def test_document_print_view_no_access(self):
        response = self._request_document_print_view()
        self.assertEqual(response.status_code, 403)

    def test_document_print_view_with_access(self):
        self.grant_access(
            obj=self.document, permission=permission_document_print
        )
        response = self._request_document_print_view()
        self.assertEqual(response.status_code, 200)


class DocumentsQuickLabelViewsTestCase(DocumentTypeQuickLabelTestMixin, GenericDocumentViewTestCase):
    def setUp(self):
        super(DocumentsQuickLabelViewsTestCase, self).setUp()
        self.login_user()

    def _request_document_quick_label_edit_view(self, extra_data=None):
        data = {
            'document_type_available_filenames': self.document_type_filename.pk,
            'label': ''
            # View needs at least an empty label for quick
            # label to work. Cause is unknown.
        }
        data.update(extra_data or {})

        return self.post(
            viewname='documents:document_edit', args=(self.document.pk,),
            data=data
        )

    def test_document_quick_label_no_permission(self):
        self._create_quick_label()
        response = self._request_document_quick_label_edit_view()
        self.assertEqual(response.status_code, 403)
        self.document.refresh_from_db()

    def test_document_quick_label_with_access(self):
        self._create_quick_label()
        self.grant_access(
            permission=permission_document_properties_edit, obj=self.document
        )
        response = self._request_document_quick_label_edit_view()
        self.assertEqual(response.status_code, 302)
        self.document.refresh_from_db()
        self.assertEqual(
            self.document.label, self.document_type_filename.filename
        )

    def test_document_quick_label_preserve_extension_with_access(self):
        self._create_quick_label()
        self.grant_access(
            permission=permission_document_properties_edit, obj=self.document
        )
        filename, extension = os.path.splitext(self.document.label)
        response = self._request_document_quick_label_edit_view(
            extra_data={'preserve_extension': True}
        )
        self.assertEqual(response.status_code, 302)
        self.document.refresh_from_db()

        self.assertEqual(
            self.document.label, '{}{}'.format(
                self.document_type_filename.filename, extension
            )
        )

    def test_document_quick_label_no_preserve_extension_with_access(self):
        self._create_quick_label()
        self.grant_access(
            permission=permission_document_properties_edit, obj=self.document
        )
        filename, extension = os.path.splitext(self.document.label)
        response = self._request_document_quick_label_edit_view(
            extra_data={'preserve_extension': False}
        )
        self.assertEqual(response.status_code, 302)
        self.document.refresh_from_db()

        self.assertEqual(
            self.document.label, self.document_type_filename.filename
        )
