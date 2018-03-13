# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ..literals import (
    DEFAULT_DELETE_PERIOD, DEFAULT_DELETE_TIME_UNIT
)
from ..models import Document, DocumentType
from ..permissions import (
    permission_document_type_create, permission_document_type_delete,
    permission_document_type_edit, permission_document_type_view,
)

from .base import GenericDocumentViewTestCase
from .literals import (
    TEST_DOCUMENT_TYPE_LABEL, TEST_DOCUMENT_TYPE_LABEL_EDITED,
    TEST_DOCUMENT_TYPE_QUICK_LABEL, TEST_DOCUMENT_TYPE_QUICK_LABEL_EDITED
)


class DocumentTypeViewsTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(DocumentTypeViewsTestCase, self).setUp()
        self.login_user()

    def _request_document_type_create(self):
        return self.post(
            'documents:document_type_create',
            data={
                'label': TEST_DOCUMENT_TYPE_LABEL,
                'delete_time_period': DEFAULT_DELETE_PERIOD,
                'delete_time_unit': DEFAULT_DELETE_TIME_UNIT
            }, follow=True
        )

    def test_document_type_create_view_no_permission(self):
        self.document_type.delete()

        self.assertEqual(Document.objects.count(), 0)

        # Grant the document type view permission so that the post create
        # redirect works
        self.grant_permission(permission=permission_document_type_view)
        self._request_document_type_create()

        self.assertEqual(DocumentType.objects.count(), 0)

    def test_document_type_create_view_with_permission(self):
        self.document_type.delete()

        self.assertEqual(Document.objects.count(), 0)

        self.grant_permission(permission=permission_document_type_create)
        # Grant the document type view permission so that the post create
        # redirect works
        self.grant_permission(permission=permission_document_type_view)

        response = self._request_document_type_create()

        self.assertContains(response, text='successfully', status_code=200)

        self.assertEqual(DocumentType.objects.count(), 1)
        self.assertEqual(
            DocumentType.objects.first().label, TEST_DOCUMENT_TYPE_LABEL
        )

    def _request_document_type_delete(self):
        return self.post(
            'documents:document_type_delete',
            args=(self.document_type.pk,), follow=True
        )

    def test_document_type_delete_view_no_permission(self):
        # Grant the document type view permission so that the post delete
        # redirect works
        self.grant_permission(permission=permission_document_type_view)

        self._request_document_type_delete()

        self.assertEqual(DocumentType.objects.count(), 1)

    def test_document_type_delete_view_with_access(self):
        self.grant_access(
            obj=self.document_type, permission=permission_document_type_delete
        )
        # Grant the document type view permission so that the post delete
        # redirect works
        self.grant_permission(permission=permission_document_type_view)

        response = self._request_document_type_delete()

        self.assertContains(response, 'successfully', status_code=200)
        self.assertEqual(DocumentType.objects.count(), 0)

    def _request_document_type_edit(self):
        return self.post(
            'documents:document_type_edit',
            args=(self.document_type.pk,),
            data={
                'label': TEST_DOCUMENT_TYPE_LABEL_EDITED,
                'delete_time_period': DEFAULT_DELETE_PERIOD,
                'delete_time_unit': DEFAULT_DELETE_TIME_UNIT
            }, follow=True
        )

    def test_document_type_edit_view_no_permission(self):
        self._request_document_type_edit()

        self.assertEqual(
            DocumentType.objects.get(pk=self.document_type.pk).label,
            TEST_DOCUMENT_TYPE_LABEL
        )

    def test_document_type_edit_view_with_access(self):
        self.grant_access(
            obj=self.document_type, permission=permission_document_type_edit
        )

        # Grant the document type view permission so that the post delete
        # redirect works
        self.grant_permission(permission=permission_document_type_view)

        response = self._request_document_type_edit()

        self.assertContains(response, 'successfully', status_code=200)

        self.assertEqual(
            DocumentType.objects.get(pk=self.document_type.pk).label,
            TEST_DOCUMENT_TYPE_LABEL_EDITED
        )

    def _request_quick_label_create(self):
        return self.post(
            'documents:document_type_filename_create',
            args=(self.document_type.pk,),
            data={
                'filename': TEST_DOCUMENT_TYPE_QUICK_LABEL,
            }
        )

    def test_document_type_quick_label_create_no_permission(self):
        self.grant_access(
            obj=self.document_type, permission=permission_document_type_view
        )
        response = self._request_quick_label_create()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.document_type.filenames.count(), 0)

    def test_document_type_quick_label_create_with_access(self):
        self.grant_access(
            obj=self.document_type, permission=permission_document_type_view
        )
        self.grant_access(
            obj=self.document_type, permission=permission_document_type_edit
        )

        response = self._request_quick_label_create()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.document_type.filenames.count(), 1)

    def _create_quick_label(self):
        self.document_type_filename = self.document_type.filenames.create(
            filename=TEST_DOCUMENT_TYPE_QUICK_LABEL
        )

    def _request_quick_label_edit(self):
        return self.post(
            'documents:document_type_filename_edit',
            args=(self.document_type_filename.pk,),
            data={
                'filename': TEST_DOCUMENT_TYPE_QUICK_LABEL_EDITED,
            }, follow=True
        )

    def test_document_type_quick_label_edit_no_permission(self):
        self._create_quick_label()
        self.grant_access(
            obj=self.document_type, permission=permission_document_type_view
        )
        response = self._request_quick_label_edit()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            self.document_type_filename.filename,
            TEST_DOCUMENT_TYPE_QUICK_LABEL
        )

    def test_document_type_quick_label_edit_with_access(self):
        self.grant_access(
            obj=self.document_type, permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.document_type, permission=permission_document_type_view
        )

        self._create_quick_label()
        response = self._request_quick_label_edit()
        self.assertEqual(response.status_code, 200)

        self.document_type_filename.refresh_from_db()
        self.assertEqual(
            self.document_type_filename.filename,
            TEST_DOCUMENT_TYPE_QUICK_LABEL_EDITED
        )

    def _request_quick_label_delete(self):
        return self.post(
            'documents:document_type_filename_delete',
            args=(self.document_type_filename.pk,),
            follow=True
        )

    def test_document_type_quick_label_delete_no_permission(self):
        self._create_quick_label()
        self.grant_access(
            obj=self.document_type, permission=permission_document_type_view
        )
        self._request_quick_label_delete()

        self.assertEqual(
            self.document_type.filenames.count(), 1
        )
        self.assertEqual(
            self.document_type.filenames.first().filename,
            TEST_DOCUMENT_TYPE_QUICK_LABEL
        )

    def test_document_type_quick_label_delete_with_access(self):
        self.grant_access(
            obj=self.document_type, permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.document_type, permission=permission_document_type_view
        )

        self._create_quick_label()
        response = self._request_quick_label_delete()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.document_type.filenames.count(), 0
        )
