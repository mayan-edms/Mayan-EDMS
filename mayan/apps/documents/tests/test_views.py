# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.test import override_settings

from django_downloadview import assert_download_response

from common.tests.test_views import GenericViewTestCase
from converter.models import Transformation
from converter.permissions import permission_transformation_delete

from ..literals import DEFAULT_DELETE_PERIOD, DEFAULT_DELETE_TIME_UNIT
from ..models import DeletedDocument, Document, DocumentType
from ..permissions import (
    permission_document_create, permission_document_delete,
    permission_document_download, permission_document_properties_edit,
    permission_document_restore, permission_document_tools,
    permission_document_trash, permission_document_type_create,
    permission_document_type_delete, permission_document_type_edit,
    permission_document_type_view, permission_document_version_revert,
    permission_document_view, permission_empty_trash
)

from .literals import (
    TEST_DOCUMENT_TYPE, TEST_DOCUMENT_TYPE_QUICK_LABEL,
    TEST_SMALL_DOCUMENT_FILENAME, TEST_SMALL_DOCUMENT_PATH
)


TEST_DOCUMENT_TYPE_EDITED_LABEL = 'test document type edited label'
TEST_DOCUMENT_TYPE_2_LABEL = 'test document type 2 label'
TEST_TRANSFORMATION_NAME = 'rotate'
TEST_TRANSFORMATION_ARGUMENT = 'degrees: 180'


@override_settings(OCR_AUTO_OCR=False)
class GenericDocumentViewTestCase(GenericViewTestCase):
    def setUp(self):
        super(GenericDocumentViewTestCase, self).setUp()
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=file_object
            )

    def tearDown(self):
        super(GenericDocumentViewTestCase, self).tearDown()
        if self.document_type.pk:
            self.document_type.delete()


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
        self.grant(permission=permission_document_view)
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

    def test_document_list_view_with_permissions(self):
        self.grant(permission=permission_document_view)
        response = self.get('documents:document_list')
        self.assertContains(response, self.document.label, status_code=200)

    def _edit_document_type(self, document_type):
        return self.post(
            'documents:document_document_type_edit',
            args=(self.document.pk,),
            data={'document_type': document_type.pk}
        )

    def test_document_document_type_change_view_no_permissions(self):
        self.assertEqual(
            self.document.document_type, self.document_type
        )

        document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2_LABEL
        )

        response = self._edit_document_type(document_type=document_type)

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

        document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2_LABEL
        )

        self.grant(permission=permission_document_properties_edit)
        self.grant(permission=permission_document_create)

        response = self._edit_document_type(document_type=document_type)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Document.objects.get(pk=self.document.pk).document_type,
            document_type
        )

    def _multiple_document_type_edit(self, document_type):
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

        document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2_LABEL
        )

        response = self._multiple_document_type_edit(
            document_type=document_type
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

        document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2_LABEL
        )

        self.grant(permission=permission_document_properties_edit)
        self.grant(permission=permission_document_create)

        response = self._multiple_document_type_edit(
            document_type=document_type
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Document.objects.first().document_type, document_type
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

        self.grant(permission=permission_document_download)
        response = self.get(
            'documents:document_download', args=(self.document.pk,)
        )

        self.assertEqual(response.status_code, 200)

        with self.document.open() as file_object:
            assert_download_response(
                self, response, content=file_object.read(),
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
        self.grant(permission=permission_document_download)

        response = self.get(
            'documents:document_multiple_download',
            data={'id_list': self.document.pk}
        )

        self.assertEqual(response.status_code, 200)

        with self.document.open() as file_object:
            assert_download_response(
                self, response, content=file_object.read(),
                basename=TEST_SMALL_DOCUMENT_FILENAME,
                mime_type=self.document.file_mimetype
            )

    def test_document_version_download_view_no_permission(self):
        response = self.get(
            'documents:document_version_download', args=(
                self.document.latest_version.pk,
            )
        )

        self.assertEqual(response.status_code, 403)

    def test_document_version_download_view_with_permission(self):
        # Set the expected_content_type for
        # common.tests.mixins.ContentTypeCheckMixin
        self.expected_content_type = 'application/octet-stream; charset=utf-8'

        self.grant(permission=permission_document_download)
        response = self.get(
            'documents:document_version_download', args=(
                self.document.latest_version.pk,
            )
        )

        self.assertEqual(response.status_code, 200)

        with self.document.open() as file_object:
            assert_download_response(
                self, response, content=file_object.read(),
                basename='{} - {}'.format(
                    TEST_SMALL_DOCUMENT_FILENAME,
                    self.document.latest_version.timestamp
                ), mime_type='application/octet-stream; charset=utf-8'
            )

    def test_document_update_page_count_view_no_permission(self):
        self.document.pages.all().delete()
        self.assertEqual(self.document.pages.count(), 0)

        response = self.post(
            'documents:document_update_page_count', args=(self.document.pk,)
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.document.pages.count(), 0)

    def test_document_update_page_count_view_with_permissions(self):
        page_count = self.document.pages.count()
        self.document.pages.all().delete()
        self.assertEqual(self.document.pages.count(), 0)

        self.grant(permission=permission_document_tools)

        response = self.post(
            'documents:document_update_page_count',
            args=(self.document.pk,), follow=True
        )
        self.assertContains(response, text='queued', status_code=200)
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

    def test_document_multiple_update_page_count_view_with_permissions(self):
        page_count = self.document.pages.count()
        self.document.pages.all().delete()
        self.assertEqual(self.document.pages.count(), 0)

        self.grant(permission=permission_document_tools)

        response = self.post(
            'documents:document_multiple_update_page_count',
            data={'id_list': self.document.pk}, follow=True
        )
        self.assertContains(response, text='queued', status_code=200)
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

        self.grant(permission=permission_document_view)

        response = self.post(
            'documents:document_clear_transformations',
            args=(self.document.pk,)
        )

        self.assertEqual(response.status_code, 302)
        self.assertQuerysetEqual(
            Transformation.objects.get_for_model(document_page),
            (repr(transformation),)
        )

    def test_document_clear_transformations_view_with_permissions(self):
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

        self.grant(permission=permission_transformation_delete)
        self.grant(permission=permission_document_view)

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

        self.grant(permission=permission_document_view)

        response = self.post(
            'documents:document_multiple_clear_transformations',
            data={'id_list': self.document.pk}
        )

        self.assertEqual(response.status_code, 302)
        self.assertQuerysetEqual(
            Transformation.objects.get_for_model(document_page),
            (repr(transformation),)
        )

    def _empty_trash(self):
        return self.post('documents:trash_can_empty')

    def test_trash_can_empty_view_no_permissions(self):
        self.document.delete()
        self.assertEqual(DeletedDocument.objects.count(), 1)

        response = self._empty_trash()

        self.assertEqual(response.status_code, 403)

        self.assertEqual(DeletedDocument.objects.count(), 1)

    def test_trash_can_empty_view_with_permission(self):
        self.document.delete()
        self.assertEqual(DeletedDocument.objects.count(), 1)

        self.grant(permission=permission_empty_trash)

        response = self._empty_trash()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(DeletedDocument.objects.count(), 0)
        self.assertEqual(Document.objects.count(), 0)

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

    def test_document_version_revert_with_permission(self):
        first_version = self.document.latest_version

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document.new_version(
                file_object=file_object
            )

        self.grant(permission=permission_document_version_revert)

        response = self.post(
            'documents:document_version_revert', args=(first_version.pk,),
            follow=True
        )

        self.assertContains(response, 'reverted', status_code=200)
        self.assertEqual(self.document.versions.count(), 1)

    def test_document_page_view_no_permissions(self):
        response = self.get(
            'documents:document_page_view', args=(
                self.document.pages.first().pk,
            )
        )

        self.assertEqual(response.status_code, 403)

    def test_document_page_view_with_permissions(self):
        self.grant(permission=permission_document_view)
        response = self.get(
            'documents:document_page_view', args=(
                self.document.pages.first().pk,
            ),
            follow=True
        )

        self.assertContains(
            response, unicode(self.document.pages.first()), status_code=200
        )


class DocumentPageViewTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(DocumentPageViewTestCase, self).setUp()
        self.login_user()

    def _document_page_list_view(self):
        return self.get(
            'documents:document_pages', args=(self.document.pk,)
        )

    def test_document_page_list_view_no_permission(self):
        response = self._document_page_list_view()
        self.assertEqual(response.status_code, 403)

    def test_document_page_list_view_with_permission(self):
        self.grant(permission_document_view)
        response = self._document_page_list_view()
        self.assertContains(
            response, text=self.document.label, status_code=200
        )


class DocumentTypeViewsTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(DocumentTypeViewsTestCase, self).setUp()
        self.login_user()

    def test_document_type_create_view_no_permission(self):
        self.document_type.delete()

        self.assertEqual(Document.objects.count(), 0)

        response = self.post(
            'documents:document_type_create',
            data={
                'label': TEST_DOCUMENT_TYPE,
                'delete_time_period': DEFAULT_DELETE_PERIOD,
                'delete_time_unit': DEFAULT_DELETE_TIME_UNIT
            }
        )

        self.assertEqual(response.status_code, 403)

        self.assertEqual(DocumentType.objects.count(), 0)

    def test_document_type_create_view_with_permission(self):
        self.document_type.delete()

        self.assertEqual(Document.objects.count(), 0)

        self.grant(permission=permission_document_type_create)
        self.grant(permission=permission_document_type_view)

        response = self.post(
            'documents:document_type_create',
            data={
                'label': TEST_DOCUMENT_TYPE,
                'delete_time_period': DEFAULT_DELETE_PERIOD,
                'delete_time_unit': DEFAULT_DELETE_TIME_UNIT
            }, follow=True
        )

        self.assertContains(response, text='successfully', status_code=200)

        self.assertEqual(DocumentType.objects.count(), 1)
        self.assertEqual(
            DocumentType.objects.first().label, TEST_DOCUMENT_TYPE
        )

    def test_document_type_delete_view_no_permission(self):
        response = self.post(
            'documents:document_type_delete',
            args=(self.document_type.pk,)
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(DocumentType.objects.count(), 1)

    def test_document_type_delete_view_with_permission(self):
        self.grant(permission=permission_document_type_delete)
        self.grant(permission=permission_document_type_view)

        response = self.post(
            'documents:document_type_delete',
            args=(self.document_type.pk,), follow=True
        )

        self.assertContains(response, 'successfully', status_code=200)
        self.assertEqual(DocumentType.objects.count(), 0)

    def test_document_type_edit_view_no_permission(self):
        response = self.post(
            'documents:document_type_edit',
            args=(self.document_type.pk,),
            data={
                'label': TEST_DOCUMENT_TYPE_EDITED_LABEL,
                'delete_time_period': DEFAULT_DELETE_PERIOD,
                'delete_time_unit': DEFAULT_DELETE_TIME_UNIT
            }
        )

        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            DocumentType.objects.get(pk=self.document_type.pk).label,
            TEST_DOCUMENT_TYPE
        )

    def test_document_type_edit_view_with_permission(self):
        self.grant(permission=permission_document_type_edit)
        self.grant(permission=permission_document_type_view)

        response = self.post(
            'documents:document_type_edit',
            args=(self.document_type.pk,),
            data={
                'label': TEST_DOCUMENT_TYPE_EDITED_LABEL,
                'delete_time_period': DEFAULT_DELETE_PERIOD,
                'delete_time_unit': DEFAULT_DELETE_TIME_UNIT
            }, follow=True
        )

        self.assertContains(response, 'successfully', status_code=200)

        self.assertEqual(
            DocumentType.objects.get(pk=self.document_type.pk).label,
            TEST_DOCUMENT_TYPE_EDITED_LABEL
        )

    def test_document_type_quick_label_create_no_permission(self):
        response = self.post(
            'documents:document_type_filename_create',
            args=(self.document_type.pk,),
            data={
                'filename': TEST_DOCUMENT_TYPE_QUICK_LABEL,
            }, follow=True
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.document_type.filenames.count(), 0)

    def test_document_type_quick_label_create_with_permission(self):
        self.grant(permission=permission_document_type_edit)

        response = self.post(
            'documents:document_type_filename_create',
            args=(self.document_type.pk,),
            data={
                'filename': TEST_DOCUMENT_TYPE_QUICK_LABEL,
            }, follow=True
        )

        self.assertContains(response, 'reated', status_code=200)
        self.assertEqual(self.document_type.filenames.count(), 1)


class DeletedDocumentTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(DeletedDocumentTestCase, self).setUp()
        self.login_user()

    def test_document_restore_view_no_permission(self):
        self.document.delete()
        self.assertEqual(Document.objects.count(), 0)

        response = self.post(
            'documents:document_restore', args=(self.document.pk,)
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(DeletedDocument.objects.count(), 1)
        self.assertEqual(Document.objects.count(), 0)

    def test_document_restore_view_with_permission(self):
        self.document.delete()
        self.assertEqual(Document.objects.count(), 0)

        self.grant(permission=permission_document_restore)
        response = self.post(
            'documents:document_restore', args=(self.document.pk,),
            follow=True
        )
        self.assertContains(response, text='restored', status_code=200)
        self.assertEqual(DeletedDocument.objects.count(), 0)
        self.assertEqual(Document.objects.count(), 1)

    def test_document_trash_no_permissions(self):
        response = self.post(
            'documents:document_trash', args=(self.document.pk,)
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(DeletedDocument.objects.count(), 0)
        self.assertEqual(Document.objects.count(), 1)

    def test_document_trash_with_permissions(self):
        self.grant(permission=permission_document_trash)

        response = self.post(
            'documents:document_trash', args=(self.document.pk,),
            follow=True
        )

        self.assertContains(response, text='success', status_code=200)
        self.assertEqual(DeletedDocument.objects.count(), 1)
        self.assertEqual(Document.objects.count(), 0)

    def test_document_delete_no_permissions(self):
        self.document.delete()
        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(DeletedDocument.objects.count(), 1)

        response = self.post(
            'documents:document_delete', args=(self.document.pk,),
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(DeletedDocument.objects.count(), 1)

    def test_document_delete_with_permissions(self):
        self.document.delete()
        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(DeletedDocument.objects.count(), 1)

        self.grant(permission=permission_document_delete)

        response = self.post(
            'documents:document_delete', args=(self.document.pk,),
            follow=True
        )

        self.assertContains(response, text='success', status_code=200)
        self.assertEqual(DeletedDocument.objects.count(), 0)
        self.assertEqual(Document.objects.count(), 0)

    def test_deleted_document_list_view_no_permissions(self):
        self.document.delete()

        response = self.get('documents:document_list_deleted')

        self.assertNotContains(response, self.document.label, status_code=200)

    def test_deleted_document_list_view_with_permissions(self):
        self.document.delete()

        self.grant(permission=permission_document_view)
        response = self.get('documents:document_list_deleted')

        self.assertContains(response, self.document.label, status_code=200)
