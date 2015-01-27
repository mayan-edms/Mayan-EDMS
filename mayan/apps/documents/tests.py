from __future__ import unicode_literals

from json import loads
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import File
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from .models import Document, DocumentType

TEST_ADMIN_PASSWORD = 'test_admin_password'
TEST_ADMIN_USERNAME = 'test_admin'
TEST_ADMIN_EMAIL = 'admin@admin.com'
TEST_SMALL_DOCUMENT_FILENAME = 'title_page.png'
TEST_DOCUMENT_PATH = os.path.join(settings.BASE_DIR, 'contrib', 'sample_documents', 'mayan_11_1.pdf')
TEST_SIGNED_DOCUMENT_PATH = os.path.join(settings.BASE_DIR, 'contrib', 'sample_documents', 'mayan_11_1.pdf.gpg')
TEST_SMALL_DOCUMENT_PATH = os.path.join(settings.BASE_DIR, 'contrib', 'sample_documents', TEST_SMALL_DOCUMENT_FILENAME)
TEST_DOCUMENT_DESCRIPTION = 'test description'
TEST_DOCUMENT_TYPE = 'test_document_type'


class DocumentTestCase(TestCase):
    def setUp(self):
        self.document_type = DocumentType.objects.create(name='test doc type')

        with open(TEST_DOCUMENT_PATH) as file_object:
            self.document = Document.objects.new_document(file_object=File(file_object), label='mayan_11_1.pdf', document_type=self.document_type)[0].document

    def test_document_creation(self):
        self.failUnlessEqual(self.document_type.name, 'test doc type')

        self.failUnlessEqual(self.document.exists(), True)
        self.failUnlessEqual(self.document.size, 272213)

        self.failUnlessEqual(self.document.file_mimetype, 'application/pdf')
        self.failUnlessEqual(self.document.file_mime_encoding, 'binary')
        self.failUnlessEqual(self.document.label, 'mayan_11_1.pdf')
        self.failUnlessEqual(self.document.checksum, 'c637ffab6b8bb026ed3784afdb07663fddc60099853fae2be93890852a69ecf3')
        self.failUnlessEqual(self.document.page_count, 47)

        # self.failUnlessEqual(self.document.has_detached_signature(), False)

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            new_version_data = {
                'comment': 'test comment 1',
            }

            self.document.new_version(file_object=File(file_object))

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document.new_version(file_object=File(file_object), **new_version_data)

        self.failUnlessEqual(self.document.versions.count(), 3)

    def tearDown(self):
        self.document.delete()
        self.document_type.delete()


class DocumentAPICreateDocumentTestCase(TestCase):
    """
    Functional test to make sure all the moving parts to create a document from
    the API are working correctly
    """

    def setUp(self):
        self.admin_user = User.objects.create_superuser(username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL, password=TEST_ADMIN_PASSWORD)
        self.document_type = DocumentType.objects.create(name='test doc type')

    def test_uploading_a_document_using_token_auth(self):
        # Get the an user token
        token_client = APIClient()
        response = token_client.post(reverse('auth_token_obtain'), {'username': TEST_ADMIN_USERNAME, 'password': TEST_ADMIN_PASSWORD})

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
            document_response = document_client.post(reverse('document-list'), {'document_type': self.document_type.pk, 'file': file_descriptor})

        self.assertEqual(document_response.status_code, status.HTTP_202_ACCEPTED)

        # The document was created in the DB?
        self.assertEqual(Document.objects.count(), 1)

        new_version_url = reverse('document-new-version', args=[Document.objects.first().pk])

        with open(TEST_DOCUMENT_PATH) as file_descriptor:
            response = document_client.post(new_version_url, {'file': file_descriptor})

        # Make sure the document uploaded correctly
        document = Document.objects.first()
        self.failUnlessEqual(document.exists(), True)
        self.failUnlessEqual(document.size, 272213)

        self.failUnlessEqual(document.file_mimetype, 'application/pdf')
        self.failUnlessEqual(document.file_mime_encoding, 'binary')
        self.failUnlessEqual(document.label, TEST_SMALL_DOCUMENT_FILENAME)
        self.failUnlessEqual(document.checksum, 'c637ffab6b8bb026ed3784afdb07663fddc60099853fae2be93890852a69ecf3')
        self.failUnlessEqual(document.page_count, 47)

        # Make sure we can edit the document via the API
        document_url = reverse('document-detail', args=[Document.objects.first().pk])

        response = document_client.post(document_url, {'description': 'edited test document'})

        # self.assertTrue(document.description, 'edited test document')

        # Make sure we can delete the document via the API
        response = document_client.delete(document_url)

        # The document was deleted from the the DB?
        self.assertEqual(Document.objects.count(), 0)

    def tearDown(self):
        self.document_type.delete()


class DocumentsViewsFunctionalTestCase(TestCase):
    """
    Functional tests to make sure all the moving parts after creating a
    document from the frontend are working correctly
    """

    def setUp(self):
        from sources.models import WebFormSource
        from sources.literals import SOURCE_CHOICE_WEB_FORM

        DocumentType.objects.all().delete()  # Clean up <orphan document type>
        self.document_type = DocumentType.objects.create(name=TEST_DOCUMENT_TYPE)
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
        self.assertContains(response, 'ocuments (1)', status_code=200)

        # test document simple view
        response = self.client.get(reverse('documents:document_properties', args=[self.document.pk]))
        self.assertContains(response, 'roperties for document', status_code=200)

    def test_document_type_views(self):
        # Check that there are no document types
        response = self.client.get(reverse('documents:document_type_list'))
        self.assertContains(response, 'ocument types (1)', status_code=200)

        # Create a document type
        response = self.client.post(reverse('documents:document_type_create'), data={'name': TEST_DOCUMENT_TYPE}, follow=True)
        self.assertEqual(response.status_code, 200)
        # TODO: fix failing test
        # self.assertTrue('Document type created successfully' in response.content)

        # Check that there is one document types
        response = self.client.get(reverse('documents:document_type_list'))
        self.assertEqual(response.status_code, 200)
        # self.assertTrue('Document types (2)' in response.content)

        document_type = DocumentType.objects.first()
        self.assertEqual(document_type.name, TEST_DOCUMENT_TYPE)

        # Edit the document type
        response = self.client.post(reverse('documents:document_type_edit', args=[document_type.pk]), data={'name': TEST_DOCUMENT_TYPE + 'partial'}, follow=True)
        self.assertContains(response, 'Document type edited successfully', status_code=200)

        document_type = DocumentType.objects.first()
        self.assertEqual(document_type.name, TEST_DOCUMENT_TYPE + 'partial')

        # Delete the document type
        response = self.client.post(reverse('documents:document_type_delete', args=[document_type.pk]), follow=True)
        self.assertContains(response, 'Document type: {0} deleted successfully'.format(document_type.name), status_code=200)

        # Check that there are no document types
        response = self.client.get(reverse('documents:document_type_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ocument types (0)', status_code=200)
