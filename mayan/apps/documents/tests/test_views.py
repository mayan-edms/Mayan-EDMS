# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.files import File
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase, override_settings

from ..literals import DEFAULT_DELETE_PERIOD, DEFAULT_DELETE_TIME_UNIT
from ..models import DeletedDocument, Document, DocumentType

from .literals import (
    TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME, TEST_ADMIN_EMAIL,
    TEST_SMALL_DOCUMENT_PATH, TEST_DOCUMENT_TYPE
)

TEST_DOCUMENT_TYPE_EDITED_LABEL = 'test document type edited label'


@override_settings(OCR_AUTO_OCR=False)
class DocumentsViewsTestCase(TestCase):
    def setUp(self):
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        self.admin_user = User.objects.create_superuser(
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

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=File(file_object), label='mayan_11_1.pdf'
            )

    def tearDown(self):
        self.document_type.delete()
        self.admin_user.delete()

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


@override_settings(OCR_AUTO_OCR=False)
class DocumentTypeViewsTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
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
