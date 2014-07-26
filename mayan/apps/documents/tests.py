from __future__ import absolute_import

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

from .literals import VERSION_UPDATE_MAJOR, RELEASE_LEVEL_FINAL
from .models import Document, DocumentType

TEST_ADMIN_PASSWORD = 'test_admin_password'
TEST_ADMIN_USERNAME = 'test_admin'
TEST_ADMIN_EMAIL = 'admin@admin.com'
TEST_DOCUMENT_PATH = os.path.join(settings.BASE_DIR, 'contrib', 'sample_documents', 'mayan_11_1.pdf')
TEST_SIGNED_DOCUMENT_PATH = os.path.join(settings.BASE_DIR, 'contrib', 'sample_documents', 'mayan_11_1.pdf.gpg')


class DocumentTestCase(TestCase):
    def setUp(self):
        self.document_type = DocumentType(name='test doc type')
        self.document_type.save()

        self.document = Document(
            document_type=self.document_type,
            description='description',
        )
        self.document.save()

        with open(TEST_DOCUMENT_PATH) as file_object:
            new_version = self.document.new_version(file=File(file_object, name='mayan_11_1.pdf'))

    def test_document_creation(self):
        self.failUnlessEqual(self.document_type.name, 'test doc type')

        self.failUnlessEqual(self.document.exists(), True)
        self.failUnlessEqual(self.document.size, 272213)

        self.failUnlessEqual(self.document.file_mimetype, 'application/pdf')
        self.failUnlessEqual(self.document.file_mime_encoding, 'binary')
        self.failUnlessEqual(self.document.file_filename, 'mayan_11_1.pdf')
        self.failUnlessEqual(self.document.checksum, 'c637ffab6b8bb026ed3784afdb07663fddc60099853fae2be93890852a69ecf3')
        self.failUnlessEqual(self.document.page_count, 47)

        self.failUnlessEqual(self.document.latest_version.get_formated_version(), '1.0')
        # self.failUnlessEqual(self.document.has_detached_signature(), False)

        with open(TEST_SIGNED_DOCUMENT_PATH) as file_object:
            new_version_data = {
                'comment': 'test comment 1',
                'version_update': VERSION_UPDATE_MAJOR,
                'release_level': RELEASE_LEVEL_FINAL,
                'serial': 0,
            }

            new_version = self.document.new_version(file=File(file_object, name='mayan_11_1.pdf.gpg'), **new_version_data)

        self.failUnlessEqual(self.document.latest_version.get_formated_version(), '2.0')

        new_version_data = {
            'comment': 'test comment 2',
            'version_update': VERSION_UPDATE_MAJOR,
            'release_level': RELEASE_LEVEL_FINAL,
            'serial': 0,
        }
        with open(TEST_DOCUMENT_PATH) as file_object:
            new_version = self.document.new_version(file=File(file_object), **new_version_data)

        self.failUnlessEqual(self.document.latest_version.get_formated_version(), '3.0')

    def tearDown(self):
        self.document.delete()
        self.document_type.delete()


class DocumentSearchTestCase(TestCase):
    def setUp(self):
        from ocr.parsers import parse_document_page
        self.document_type = DocumentType(name='test doc type')
        self.document_type.save()

        self.document = Document(
            document_type=self.document_type,
            description='description',
        )
        self.document.save()

        with open(TEST_DOCUMENT_PATH) as file_object:
            new_version = self.document.new_version(file=File(file_object, name='mayan_11_1.pdf'))

        # Text extraction on the first page only
        parse_document_page(self.document.latest_version.pages.all()[0])

    def test_simple_search_after_related_name_change(self):
        """
        Test that simple search works after related_name changes to
        document versions and document version pages
        """

        from . import document_search

        model_list, flat_list, shown_result_count, result_count, elapsed_time = document_search.simple_search('Mayan')
        self.assertEqual(result_count, 1)
        self.assertEqual(flat_list, [self.document])

    def test_advanced_search_after_related_name_change(self):
        from . import document_search
        # Test versions__filename
        model_list, flat_list, shown_result_count, result_count, elapsed_time = document_search.advanced_search({'versions__filename': self.document.filename})
        self.assertEqual(result_count, 1)
        self.assertEqual(flat_list, [self.document])

        # Test versions__mimetype
        model_list, flat_list, shown_result_count, result_count, elapsed_time = document_search.advanced_search({'versions__mimetype': self.document.file_mimetype})
        self.assertEqual(result_count, 1)
        self.assertEqual(flat_list, [self.document])

        # Test versions__pages__content
        # Search by the first 20 characters of the content of the first page of the uploaded document
        model_list, flat_list, shown_result_count, result_count, elapsed_time = document_search.advanced_search({'versions__pages__content': self.document.latest_version.pages.all()[0].content[0:20]})
        self.assertEqual(result_count, 1)
        self.assertEqual(flat_list, [self.document])

    def tearDown(self):
        self.document.delete()
        self.document_type.delete()


class DocumentUploadFunctionalTestCase(TestCase):
    """
    Functional test to make sure all the moving parts to create a document from
    the frontend are working correctly
    """

    def setUp(self):
        self.admin_user = User.objects.create_superuser(username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL, password=TEST_ADMIN_PASSWORD)
        self.client = Client()

    def test_upload_a_document(self):
        from sources.models import WebForm
        from sources.literals import SOURCE_CHOICE_WEB_FORM

        # Login the admin user
        logged_in = self.client.login(username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD)
        self.assertTrue(logged_in)
        self.assertTrue(self.admin_user.is_authenticated())

        # Create new webform source
        response = self.client.post(reverse('setup_source_create', args=[SOURCE_CHOICE_WEB_FORM]), {'title': 'test', 'uncompress': 'n', 'enabled': True})
        self.assertEqual(WebForm.objects.count(), 1)

        # Upload the test document
        with open(TEST_DOCUMENT_PATH) as file_descriptor:
            response = self.client.post(reverse('upload_interactive'), {'file': file_descriptor})
        self.assertEqual(Document.objects.count(), 1)

        self.document = Document.objects.all().first()
        self.failUnlessEqual(self.document.exists(), True)
        self.failUnlessEqual(self.document.size, 272213)

        self.failUnlessEqual(self.document.file_mimetype, 'application/pdf')
        self.failUnlessEqual(self.document.file_mime_encoding, 'binary')
        self.failUnlessEqual(self.document.file_filename, 'mayan_11_1.pdf')
        self.failUnlessEqual(self.document.checksum, 'c637ffab6b8bb026ed3784afdb07663fddc60099853fae2be93890852a69ecf3')
        self.failUnlessEqual(self.document.page_count, 47)

        # Delete the document
        response = self.client.post(reverse('document_delete', args=[self.document.pk]))
        self.assertEqual(Document.objects.count(), 0)


class DocumentAPICreateDocumentTestCase(TestCase):
    """
    Functional test to make sure all the moving parts to create a document from
    the API are working correctly
    """

    def setUp(self):
        self.admin_user = User.objects.create_superuser(username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL, password=TEST_ADMIN_PASSWORD)

    def test_uploading_a_document_using_token_auth(self):
        # Get the an user token
        token_client = APIClient()
        response = token_client.post(reverse('auth_token_obtain'), {'username': TEST_ADMIN_USERNAME, 'password': TEST_ADMIN_PASSWORD})

        # Be able to get authentication token
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Make a token was returned
        self.assertTrue(u'token' in response.content)

        token = loads(response.content)['token']

        # Create a new client to simulate a different request
        document_client = APIClient()

        # Create a blank document with no token in the header
        response = document_client.post(reverse('document-list'), {'description': 'test document'})

        # Make sure toke authentication is working, should fail
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        document_client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # Create a blank document
        document_response = document_client.post(reverse('document-list'), {'description': 'test document'})
        self.assertEqual(document_response.status_code, status.HTTP_201_CREATED)

        # The document was created in the DB?
        self.assertEqual(Document.objects.count(), 1)

        new_version_url = loads(document_response.content)['new_version']

        with open(TEST_DOCUMENT_PATH) as file_descriptor:
            response = document_client.post(new_version_url, {'file': file_descriptor})

        # Make sure the document uploaded correctly
        document = Document.objects.first()
        self.failUnlessEqual(document.exists(), True)
        self.failUnlessEqual(document.size, 272213)

        self.failUnlessEqual(document.file_mimetype, 'application/pdf')
        self.failUnlessEqual(document.file_mime_encoding, 'binary')
        self.failUnlessEqual(document.file_filename, 'mayan_11_1.pdf')
        self.failUnlessEqual(document.checksum, 'c637ffab6b8bb026ed3784afdb07663fddc60099853fae2be93890852a69ecf3')
        self.failUnlessEqual(document.page_count, 47)

        # Make sure we can edit the document via the API
        document_url = loads(document_response.content)['url']

        response = document_client.post(document_url, {'description': 'edited test document'})

        self.assertTrue(document.description, 'edited test document')

        # Make sure we can delete the document via the API
        response = document_client.delete(document_url)

        # The document was deleted from the the DB?
        self.assertEqual(Document.objects.count(), 0)
