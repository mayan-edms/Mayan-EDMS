from __future__ import unicode_literals

from ..literals import (
    DEFAULT_DELETE_PERIOD, DEFAULT_DELETE_TIME_UNIT
)
from ..models import DocumentType
from ..permissions import (
    permission_document_type_create, permission_document_type_delete,
    permission_document_type_edit, permission_document_type_view,
)

from .base import GenericDocumentViewTestCase
from .literals import (
    TEST_DOCUMENT_TYPE_LABEL, TEST_DOCUMENT_TYPE_LABEL_EDITED,
    TEST_DOCUMENT_TYPE_QUICK_LABEL, TEST_DOCUMENT_TYPE_QUICK_LABEL_EDITED
)
from .mixins import DocumentTypeQuickLabelTestMixin


class DocumentTypeViewsTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(DocumentTypeViewsTestCase, self).setUp()
        self.login_user()

    def _request_document_type_create(self):
        return self.post(
            viewname='documents:document_type_create',
            data={
                'label': TEST_DOCUMENT_TYPE_LABEL,
                'delete_time_period': DEFAULT_DELETE_PERIOD,
                'delete_time_unit': DEFAULT_DELETE_TIME_UNIT
            }
        )

    def test_document_type_create_view_no_permission(self):
        self.document_type.delete()
        response = self._request_document_type_create()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(DocumentType.objects.count(), 0)

    def test_document_type_create_view_with_permission(self):
        self.document_type.delete()
        self.grant_permission(permission=permission_document_type_create)
        response = self._request_document_type_create()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(DocumentType.objects.count(), 1)
        self.assertEqual(
            DocumentType.objects.first().label, TEST_DOCUMENT_TYPE_LABEL
        )

    def _request_document_type_delete(self):
        return self.post(
            viewname='documents:document_type_delete',
            args=(self.document_type.pk,)
        )

    def test_document_type_delete_view_no_permission(self):
        response = self._request_document_type_delete()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(DocumentType.objects.count(), 1)

    def test_document_type_delete_view_with_access(self):
        self.grant_access(
            obj=self.document_type, permission=permission_document_type_delete
        )
        response = self._request_document_type_delete()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DocumentType.objects.count(), 0)

    def _request_document_type_edit(self):
        return self.post(
            viewname='documents:document_type_edit',
            args=(self.document_type.pk,),
            data={
                'label': TEST_DOCUMENT_TYPE_LABEL_EDITED,
                'delete_time_period': DEFAULT_DELETE_PERIOD,
                'delete_time_unit': DEFAULT_DELETE_TIME_UNIT
            }
        )

    def test_document_type_edit_view_no_permission(self):
        response = self._request_document_type_edit()
        self.assertEqual(response.status_code, 403)
        self.document_type.refresh_from_db()
        self.assertEqual(
            self.document_type.label, TEST_DOCUMENT_TYPE_LABEL
        )

    def test_document_type_edit_view_with_access(self):
        self.grant_access(
            obj=self.document_type, permission=permission_document_type_edit
        )
        response = self._request_document_type_edit()
        self.assertEqual(response.status_code, 302)
        self.document_type.refresh_from_db()
        self.assertEqual(
            self.document_type.label, TEST_DOCUMENT_TYPE_LABEL_EDITED
        )


class DocumentTypeQuickLabelViewsTestCase(DocumentTypeQuickLabelTestMixin, GenericDocumentViewTestCase):
    def setUp(self):
        super(DocumentTypeQuickLabelViewsTestCase, self).setUp()
        self.login_user()

    def _request_quick_label_create(self):
        return self.post(
            viewname='documents:document_type_filename_create',
            args=(self.document_type.pk,),
            data={
                'filename': TEST_DOCUMENT_TYPE_QUICK_LABEL,
            }
        )

    def test_document_type_quick_label_create_no_access(self):
        self.grant_access(
            obj=self.document_type, permission=permission_document_type_view
        )
        response = self._request_quick_label_create()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.document_type.filenames.count(), 0)

    def test_document_type_quick_label_create_with_access(self):
        self.grant_access(
            obj=self.document_type, permission=permission_document_type_edit
        )
        response = self._request_quick_label_create()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.document_type.filenames.count(), 1)

    def _request_quick_label_delete(self):
        return self.post(
            viewname='documents:document_type_filename_delete',
            args=(self.document_type_filename.pk,),
        )

    def test_document_type_quick_label_delete_no_access(self):
        self._create_quick_label()
        self._request_quick_label_delete()

        self.assertEqual(
            self.document_type.filenames.count(), 1
        )

    def test_document_type_quick_label_delete_with_access(self):
        self.grant_access(
            obj=self.document_type, permission=permission_document_type_edit
        )
        self._create_quick_label()
        response = self._request_quick_label_delete()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.document_type.filenames.count(), 0
        )

    def _request_quick_label_edit(self):
        return self.post(
            viewname='documents:document_type_filename_edit',
            args=(self.document_type_filename.pk,),
            data={
                'filename': TEST_DOCUMENT_TYPE_QUICK_LABEL_EDITED,
            }
        )

    def test_document_type_quick_label_edit_no_access(self):
        self._create_quick_label()
        response = self._request_quick_label_edit()

        self.assertEqual(response.status_code, 403)
        self.document_type_filename.refresh_from_db()
        self.assertEqual(
            self.document_type_filename.filename,
            TEST_DOCUMENT_TYPE_QUICK_LABEL
        )

    def test_document_type_quick_label_edit_with_access(self):
        self.grant_access(
            obj=self.document_type, permission=permission_document_type_edit
        )
        self._create_quick_label()
        response = self._request_quick_label_edit()

        self.assertEqual(response.status_code, 302)

        self.document_type_filename.refresh_from_db()
        self.assertEqual(
            self.document_type_filename.filename,
            TEST_DOCUMENT_TYPE_QUICK_LABEL_EDITED
        )

    def _request_quick_label_list_view(self):
        return self.get(
            viewname='documents:document_type_filename_list',
            args=(self.document_type.pk,),
        )

    def test_document_type_quick_label_list_no_access(self):
        self._create_quick_label()
        response = self._request_quick_label_list_view()
        self.assertEqual(response.status_code, 403)

    def test_document_type_quick_label_list_with_access(self):
        self._create_quick_label()
        self.grant_access(
            obj=self.document_type, permission=permission_document_type_view
        )
        response = self._request_quick_label_list_view()
        self.assertContains(
            response, text=self.document_type_filename, status_code=200
        )
