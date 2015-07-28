# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from json import loads

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from .models import Document, DocumentType
from .test_models import (
    TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME, TEST_ADMIN_EMAIL,
    TEST_SMALL_DOCUMENT_FILENAME, TEST_DOCUMENT_PATH,
    TEST_SMALL_DOCUMENT_PATH,
    TEST_DOCUMENT_TYPE
)


class DocumentAPICreateDocumentTestCase(TestCase):
    """
    Functional test to make sure all the moving parts to create a document
    from the API are working correctly
    """

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        ocr_settings = self.document_type.ocr_settings
        ocr_settings.auto_ocr = False
        ocr_settings.save()

    def tearDown(self):
        self.document_type.delete()
        self.admin_user.delete()

    def test_uploading_a_document_using_token_auth(self):
        # Get the an user token
        token_client = APIClient()
        response = token_client.post(
            reverse('auth_token_obtain'), {
                'username': TEST_ADMIN_USERNAME,
                'password': TEST_ADMIN_PASSWORD
            }
        )

        # Be able to get authentication token
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Make sure a token was returned
        self.assertTrue('token' in response.content)

        token = loads(response.content)['token']

        # Create a new client to simulate a different request
        document_client = APIClient()

        # Create a blank document with no token in the header
        # TODO: Fix, must not be able to create the document with API token
        # with open(TEST_SMALL_DOCUMENT_PATH) as file_descriptor:
        #    response = document_client.post(reverse('document-list'), {'document_type': self.document_type.pk, 'file': file_descriptor})

        # Make sure toke authentication is working, should fail
        # TODO: FIX failing test: self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        document_client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # Create a blank document
        with open(TEST_SMALL_DOCUMENT_PATH) as file_descriptor:
            document_response = document_client.post(
                reverse('document-list'), {
                    'document_type': self.document_type.pk,
                    'file': file_descriptor
                }
            )

        self.assertEqual(document_response.status_code, status.HTTP_201_CREATED)

        # The document was created in the DB?
        self.assertEqual(Document.objects.count(), 1)

        new_version_url = reverse(
            'document-new-version', args=[Document.objects.first().pk]
        )

        with open(TEST_DOCUMENT_PATH) as file_descriptor:
            response = document_client.post(
                new_version_url, {'file': file_descriptor}
            )

        # Make sure the document uploaded correctly
        document = Document.objects.first()
        self.assertEqual(document.exists(), True)
        self.assertEqual(document.size, 272213)

        self.assertEqual(document.file_mimetype, 'application/pdf')
        self.assertEqual(document.file_mime_encoding, 'binary')
        self.assertEqual(document.label, TEST_SMALL_DOCUMENT_FILENAME)
        self.assertEqual(
            document.checksum,
            'c637ffab6b8bb026ed3784afdb07663fddc60099853fae2be93890852a69ecf3'
        )
        self.assertEqual(document.page_count, 47)

        # Make sure we can edit the document via the API
        document_url = reverse(
            'document-detail', args=[Document.objects.first().pk]
        )

        response = document_client.post(
            document_url, {'description': 'edited test document'}
        )

        # self.assertTrue(document.description, 'edited test document')

        # Make sure we can delete the document via the API
        response = document_client.delete(document_url)

        # The document was deleted from the the DB?
        self.assertEqual(Document.objects.count(), 0)
