# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from json import loads
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from .models import Document, DocumentType
from .test_models import (
    TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME, TEST_ADMIN_EMAIL,
    TEST_SMALL_DOCUMENT_FILENAME, TEST_NON_ASCII_DOCUMENT_FILENAME,
    TEST_NON_ASCII_COMPRESSED_DOCUMENT_FILENAME, TEST_DOCUMENT_PATH,
    TEST_SIGNED_DOCUMENT_PATH, TEST_SMALL_DOCUMENT_PATH,
    TEST_NON_ASCII_DOCUMENT_PATH, TEST_NON_ASCII_COMPRESSED_DOCUMENT_PATH,
    TEST_DOCUMENT_DESCRIPTION, TEST_DOCUMENT_TYPE
)


class DocumentsViewsFunctionalTestCase(TestCase):
    """
    Functional tests to make sure all the moving parts after creating a
    document from the frontend are working correctly
    """

    def setUp(self):
        from sources.models import WebFormSource
        from sources.literals import SOURCE_CHOICE_WEB_FORM

        DocumentType.objects.all().delete()  # Clean up <orphan document type>
        self.document_type = DocumentType.objects.create(label=TEST_DOCUMENT_TYPE)
        self.admin_user = User.objects.create_superuser(username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL, password=TEST_ADMIN_PASSWORD)
        self.client = Client()
        # Login the admin user
        logged_in = self.client.login(username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD)
        self.assertTrue(logged_in)
        self.assertTrue(self.admin_user.is_authenticated())
        # Create new webform source
        self.client.post(reverse('sources:setup_source_create', args=[SOURCE_CHOICE_WEB_FORM]), {'title': 'test', 'uncompress': 'n', 'enabled': True})
        self.assertEqual(WebFormSource.objects.count(), 1)

        # Upload the test document
        with open(TEST_SMALL_DOCUMENT_PATH) as file_descriptor:
            self.client.post(reverse('sources:upload_interactive'), {'document-language': 'eng', 'source-file': file_descriptor, 'document_type_id': self.document_type.pk})
        self.assertEqual(Document.objects.count(), 1)
        self.document = Document.objects.first()

    def tearDown(self):
        self.document.delete()
        self.document_type.delete()

    def test_document_view(self):
        response = self.client.get(reverse('documents:document_list'))
        self.assertContains(response, 'Total: 1', status_code=200)

        # test document simple view
        response = self.client.get(reverse('documents:document_properties', args=[self.document.pk]))
        self.assertContains(response, 'roperties for document', status_code=200)

    def test_document_type_views(self):
        # Check that there are no document types
        response = self.client.get(reverse('documents:document_type_list'))
        self.assertContains(response, 'Total: 1', status_code=200)

        # Create a document type
        response = self.client.post(reverse('documents:document_type_create'), {'name': 'test document type 2'}, follow=True)
        #TODO: FIX self.assertContains(response, 'successfully', status_code=200)

        # Check that there are two document types
        response = self.client.get(reverse('documents:document_type_list'))
        #TODO: FIX self.assertContains(response, 'Total: 2', status_code=200)

        self.assertEqual(self.document_type.label, TEST_DOCUMENT_TYPE)

        # Edit the document type
        response = self.client.post(reverse('documents:document_type_edit', args=[self.document_type.pk]), data={'name': TEST_DOCUMENT_TYPE + 'partial'}, follow=True)
        #TODO: FIX self.assertContains(response, 'Document type edited successfully', status_code=200)

        # Reload document type model data
        self.document = DocumentType.objects.get(pk=self.document.pk)
        #TODO: FIX self.assertEqual(self.document_type.name, TEST_DOCUMENT_TYPE + 'partial')

        # Delete the document type
        response = self.client.post(reverse('documents:document_type_delete', args=[self.document_type.pk]), follow=True)
        #TODO: FIX self.assertContains(response, 'Document type: {0} deleted successfully'.format(self.document_type.name), status_code=200)

        # Check that there are no document types
        response = self.client.get(reverse('documents:document_type_list'))
        #TODO: FIX self.assertEqual(response.status_code, 200)
        #TODO: FIX self.assertContains(response, 'ocument types (0)', status_code=200)
