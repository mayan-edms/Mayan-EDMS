# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files import File
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase, override_settings
from django.utils.six import BytesIO

from common.tests.test_views import GenericViewTestCase
from permissions.classes import Permission
from permissions.models import Role
from permissions.tests.literals import TEST_ROLE_LABEL
from user_management.tests.literals import (
    TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME, TEST_ADMIN_EMAIL, TEST_GROUP,
    TEST_USER_EMAIL, TEST_USER_PASSWORD, TEST_USER_USERNAME
)

from ..literals import DEFAULT_DELETE_PERIOD, DEFAULT_DELETE_TIME_UNIT
from ..models import DeletedDocument, Document, DocumentType, HASH_FUNCTION
from ..permissions import (
    permission_document_download, permission_document_properties_edit
)

from .literals import (
    TEST_DOCUMENT_TYPE, TEST_SMALL_DOCUMENT_CHECKSUM, TEST_SMALL_DOCUMENT_PATH
)

TEST_DOCUMENT_TYPE_EDITED_LABEL = 'test document type edited label'
TEST_DOCUMENT_TYPE_2_LABEL = 'test document type 2 label'


@override_settings(OCR_AUTO_OCR=False)
class GenericDocumentViewTestCase(GenericViewTestCase):
    def setUp(self):
        super(GenericDocumentViewTestCase, self).setUp()
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=File(file_object), label='mayan_11_1.pdf'
            )

    def tearDown(self):
        super(GenericDocumentViewTestCase, self).tearDown()
        if self.document_type.pk:
            self.document_type.delete()


class DocumentsViewsTestCase(GenericDocumentViewTestCase):
    def test_restoring_documents(self):
        # Login the admin user
        logged_in = self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.admin_user.is_authenticated())

        self.assertEqual(Document.objects.count(), 1)

        # Trash the document
        self.client.post(
            reverse('documents:document_trash', args=(self.document.pk,))
        )
        self.assertEqual(DeletedDocument.objects.count(), 1)
        self.assertEqual(Document.objects.count(), 0)

        # Restore the document
        self.client.post(
            reverse('documents:document_restore', args=(self.document.pk,))
        )
        self.assertEqual(DeletedDocument.objects.count(), 0)
        self.assertEqual(Document.objects.count(), 1)

    def test_trashing_documents(self):
        # Login the admin user
        logged_in = self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.admin_user.is_authenticated())

        self.assertEqual(Document.objects.count(), 1)

        # Trash the document
        self.client.post(
            reverse('documents:document_trash', args=(self.document.pk,))
        )
        self.assertEqual(DeletedDocument.objects.count(), 1)
        self.assertEqual(Document.objects.count(), 0)

        # Delete the document
        self.client.post(
            reverse('documents:document_delete', args=(self.document.pk,))
        )
        self.assertEqual(DeletedDocument.objects.count(), 0)
        self.assertEqual(Document.objects.count(), 0)

    def test_document_view(self):
        # Login the admin user
        logged_in = self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.admin_user.is_authenticated())

        response = self.client.get(reverse('documents:document_list'))
        self.assertContains(response, 'Total: 1', status_code=200)

        # test document simple view
        response = self.client.get(
            reverse('documents:document_properties', args=(self.document.pk,))
        )
        self.assertContains(
            response, 'roperties for document', status_code=200
        )

    def test_document_document_type_change_view(self):
        # Login the admin user
        logged_in = self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.admin_user.is_authenticated())

        self.assertEqual(Document.objects.count(), 1)
        self.assertEqual(
            Document.objects.first().document_type, self.document_type
        )

        document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2_LABEL
        )

        response = self.client.post(
            reverse(
                'documents:document_document_type_edit',
                args=(self.document.pk,)
            ), data={'document_type': document_type.pk}, follow=True
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            Document.objects.first().document_type, document_type
        )

    def test_document_multiple_document_type_change_view(self):
        # Login the admin user
        logged_in = self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.admin_user.is_authenticated())

        self.assertEqual(Document.objects.count(), 1)
        self.assertEqual(
            Document.objects.first().document_type, self.document_type
        )

        document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2_LABEL
        )

        response = self.client.post(
            reverse(
                'documents:document_multiple_document_type_edit',
            ), data={
                'id_list': self.document.pk, 'document_type': document_type.pk
            }, follow=True
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            Document.objects.first().document_type, document_type
        )

    def test_document_multiple_document_type_change_user_view(self):
        logged_in = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.user.is_authenticated())

        self.assertEqual(Document.objects.count(), 1)
        self.assertEqual(
            Document.objects.first().document_type, self.document_type
        )

        document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2_LABEL
        )

        response = self.client.post(
            reverse(
                'documents:document_multiple_document_type_edit',
            ), data={
                'id_list': self.document.pk, 'document_type': document_type.pk
            }, follow=True
        )

        self.assertEqual(response.status_code, 200)

        # Should fail to change the document type
        self.assertEqual(
            Document.objects.first().document_type, self.document_type
        )

        # Grant the permission for a positive test result

        self.role.permissions.add(
            permission_document_properties_edit.stored_permission
        )

        response = self.client.post(
            reverse(
                'documents:document_multiple_document_type_edit',
            ), data={
                'id_list': self.document.pk, 'document_type': document_type.pk
            }, follow=True
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            Document.objects.first().document_type, document_type
        )

    def test_document_download_user_view(self):
        logged_in = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.user.is_authenticated())

        self.assertEqual(Document.objects.count(), 1)

        response = self.client.post(
            reverse(
                'documents:document_download', args=(self.document.pk,)
            )
        )

        self.assertEqual(response.status_code, 302)

        self.role.permissions.add(
            permission_document_download.stored_permission
        )

        response = self.client.post(
            reverse(
                'documents:document_download', args=(self.document.pk,)
            )
        )

        self.assertEqual(response.status_code, 200)

        buf = BytesIO()
        buf.write(response.content)

        self.assertEqual(
            HASH_FUNCTION(buf.getvalue()), TEST_SMALL_DOCUMENT_CHECKSUM
        )

        del(buf)

    def test_document_multiple_download_user_view(self):
        logged_in = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.user.is_authenticated())

        self.assertEqual(Document.objects.count(), 1)

        response = self.client.post(
            reverse('documents:document_multiple_download'),
            data={'id_list': self.document.pk}
        )

        self.assertEqual(response.status_code, 302)

        self.role.permissions.add(
            permission_document_download.stored_permission
        )

        response = self.client.post(
            reverse('documents:document_multiple_download'),
            data={'id_list': self.document.pk}
        )

        self.assertEqual(response.status_code, 200)

        buf = BytesIO()
        buf.write(response.content)

        self.assertEqual(
            HASH_FUNCTION(buf.getvalue()), TEST_SMALL_DOCUMENT_CHECKSUM
        )

        del(buf)

    def test_document_version_download_user_view(self):
        logged_in = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.user.is_authenticated())

        self.assertEqual(Document.objects.count(), 1)

        response = self.client.post(
            reverse(
                'documents:document_version_download', args=(
                    self.document.latest_version.pk,
                )
            )
        )

        self.assertEqual(response.status_code, 302)

        self.role.permissions.add(
            permission_document_download.stored_permission
        )

        response = self.client.post(
            reverse(
                'documents:document_version_download', args=(
                    self.document.latest_version.pk,
                )
            )
        )

        self.assertEqual(response.status_code, 200)

        buf = BytesIO()
        buf.write(response.content)

        self.assertEqual(
            HASH_FUNCTION(buf.getvalue()), TEST_SMALL_DOCUMENT_CHECKSUM
        )

        del(buf)


class DocumentTypeViewsTestCase(GenericDocumentViewTestCase):
    def test_document_type_create_view(self):
        # Login the admin user
        logged_in = self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.admin_user.is_authenticated())

        self.document_type.delete()

        self.assertEqual(Document.objects.count(), 0)

        response = self.client.post(
            reverse('documents:document_type_create'),
            data={
                'label': TEST_DOCUMENT_TYPE,
                'delete_time_period': DEFAULT_DELETE_PERIOD,
                'delete_time_unit': DEFAULT_DELETE_TIME_UNIT
            }, follow=True
        )

        self.assertContains(response, 'successfully', status_code=200)

        self.assertEqual(DocumentType.objects.count(), 1)
        self.assertEqual(
            DocumentType.objects.first().label, TEST_DOCUMENT_TYPE
        )

    def test_document_type_delete_view(self):
        # Login the admin user
        logged_in = self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.admin_user.is_authenticated())

        response = self.client.post(
            reverse(
                'documents:document_type_delete',
                args=(self.document_type.pk,)
            ), follow=True
        )

        self.assertContains(response, 'successfully', status_code=200)
        self.assertEqual(DocumentType.objects.count(), 0)

    def test_document_type_edit_view(self):
        # Login the admin user
        logged_in = self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.admin_user.is_authenticated())

        response = self.client.post(
            reverse(
                'documents:document_type_edit',
                args=(self.document_type.pk,)
            ), data={
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
