# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files import File
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase, override_settings

from authentication.tests.literals import (
    TEST_USER_EMAIL, TEST_USER_PASSWORD, TEST_USER_USERNAME
)
from permissions.classes import Permission
from permissions.models import Role
from permissions.tests.literals import (
    TEST_GROUP, TEST_ROLE_LABEL, TEST_USER_USERNAME
)

from ..literals import DEFAULT_DELETE_PERIOD, DEFAULT_DELETE_TIME_UNIT
from ..models import DeletedDocument, Document, DocumentType
from ..permissions import permission_document_properties_edit

from .literals import (
    TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME, TEST_ADMIN_EMAIL,
    TEST_SMALL_DOCUMENT_PATH, TEST_DOCUMENT_TYPE
)

TEST_DOCUMENT_TYPE_EDITED_LABEL = 'test document type edited label'
TEST_DOCUMENT_TYPE_2_LABEL = 'test document type 2 label'


@override_settings(OCR_AUTO_OCR=False)
class DocumentsViewsTestCase(TestCase):
    def setUp(self):
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        self.admin_user = get_user_model().objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )
        self.client = Client()
        # Login the admin user
        logged_in = self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.admin_user.is_authenticated())

        self.user = get_user_model().objects.create_user(
            username=TEST_USER_USERNAME, email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD
        )
        self.group = Group.objects.create(name=TEST_GROUP)
        self.role = Role.objects.create(label=TEST_ROLE_LABEL)
        Permission.invalidate_cache()
        self.group.user_set.add(self.user)
        self.role.groups.add(self.group)

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=File(file_object), label='mayan_11_1.pdf'
            )

    def tearDown(self):
        self.admin_user.delete()
        self.document_type.delete()
        self.group.delete()
        self.role.delete()
        self.user.delete()

    def test_restoring_documents(self):
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
        self.client.logout()
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

        # Fails to change the document type
        self.assertEqual(
            Document.objects.first().document_type, self.document_type
        )

        # Create ACL for a positive test result

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


@override_settings(OCR_AUTO_OCR=False)
class DocumentTypeViewsTestCase(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )
        self.client = Client()
        # Login the admin user
        logged_in = self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.admin_user.is_authenticated())

    def tearDown(self):
        self.admin_user.delete()

    def test_document_type_create_view(self):
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
        document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        response = self.client.post(
            reverse(
                'documents:document_type_delete', args=(document_type.pk,)
            ), follow=True
        )

        self.assertContains(response, 'successfully', status_code=200)
        self.assertEqual(DocumentType.objects.count(), 0)

    def test_document_type_edit_view(self):
        document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        response = self.client.post(
            reverse(
                'documents:document_type_edit', args=(document_type.pk,)
            ), data={
                'label': TEST_DOCUMENT_TYPE_EDITED_LABEL,
                'delete_time_period': DEFAULT_DELETE_PERIOD,
                'delete_time_unit': DEFAULT_DELETE_TIME_UNIT
            }, follow=True
        )

        self.assertContains(response, 'successfully', status_code=200)

        self.assertEqual(
            DocumentType.objects.first().label,
            TEST_DOCUMENT_TYPE_EDITED_LABEL
        )
