from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase, override_settings

from documents.models import Document, DocumentType, NewVersionBlock
from documents.tests import (
    TEST_DOCUMENT_PATH, TEST_SMALL_DOCUMENT_PATH, TEST_DOCUMENT_DESCRIPTION,
    TEST_DOCUMENT_TYPE
)
from documents.tests.test_views import GenericDocumentViewTestCase
from user_management.tests import (
    TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME,
)

from ..links import link_upload_version
from ..literals import SOURCE_CHOICE_WEB_FORM
from ..models import WebFormSource


@override_settings(OCR_AUTO_OCR=False)
class UploadDocumentTestCase(TestCase):
    """
    Test creating documents
    """

    def setUp(self):
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        self.admin_user = User.objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )
        self.client = Client()

    def tearDown(self):
        self.document_type.delete()

    def test_upload_a_document(self):
        # Login the admin user
        logged_in = self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.admin_user.is_authenticated())

        # Create new webform source
        self.client.post(
            reverse(
                'sources:setup_source_create', args=(SOURCE_CHOICE_WEB_FORM,)
            ), {'label': 'test', 'uncompress': 'n', 'enabled': True}
        )
        self.assertEqual(WebFormSource.objects.count(), 1)

        # Upload the test document
        with open(TEST_DOCUMENT_PATH) as file_descriptor:
            self.client.post(
                reverse('sources:upload_interactive'),
                {
                    'document-language': 'eng', 'source-file': file_descriptor,
                    'document_type_id': self.document_type.pk,
                    'label': 'mayan_11_1.pdf'
                }
            )
        self.assertEqual(Document.objects.count(), 1)

        self.document = Document.objects.all().first()
        self.assertEqual(self.document.exists(), True)
        self.assertEqual(self.document.size, 272213)

        self.assertEqual(self.document.file_mimetype, 'application/pdf')
        self.assertEqual(self.document.file_mime_encoding, 'binary')
        self.assertEqual(self.document.label, 'mayan_11_1.pdf')
        self.assertEqual(
            self.document.checksum,
            'c637ffab6b8bb026ed3784afdb07663fddc60099853fae2be93890852a69ecf3'
        )
        self.assertEqual(self.document.page_count, 47)

    def test_issue_25(self):
        # Login the admin user
        logged_in = self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.admin_user.is_authenticated())

        # Create new webform source
        self.client.post(
            reverse(
                'sources:setup_source_create', args=(SOURCE_CHOICE_WEB_FORM,)
            ), {'label': 'test', 'uncompress': 'n', 'enabled': True}
        )
        self.assertEqual(WebFormSource.objects.count(), 1)

        # Upload the test document
        with open(TEST_SMALL_DOCUMENT_PATH) as file_descriptor:
            self.client.post(
                reverse('sources:upload_interactive'),
                {
                    'document-language': 'eng', 'source-file': file_descriptor,
                    'document_type_id': self.document_type.pk
                }
            )
        self.assertEqual(Document.objects.count(), 1)

        document = Document.objects.first()
        # Test for issue 25 during creation
        # ** description fields was removed from upload from **
        self.assertEqual(document.description, '')

        # Reset description
        document.description = TEST_DOCUMENT_DESCRIPTION
        document.save()
        self.assertEqual(document.description, TEST_DOCUMENT_DESCRIPTION)

        # Test for issue 25 during editing
        self.client.post(
            reverse('documents:document_edit', args=(document.pk,)),
            {
                'description': TEST_DOCUMENT_DESCRIPTION,
                'language': document.language, 'label': document.label
            }
        )
        # Fetch document again and test description
        document = Document.objects.first()
        self.assertEqual(document.description, TEST_DOCUMENT_DESCRIPTION)


class NewDocumentVersionViewTestCase(GenericDocumentViewTestCase):
    def test_new_version_block(self):
        """
        Gitlab issue #231
        User shown option to upload new version of a document even though it
        is blocked by checkout - v2.0.0b2

        Expected results:
            - Link to upload version view should not resolve
            - Upload version view should reject request
        """

        self.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )

        NewVersionBlock.objects.block(self.document)

        response = self.post(
            'sources:upload_version', args=(self.document.pk,),
            follow=True
        )

        self.assertContains(
            response, text='blocked from uploading',
            status_code=200
        )

        response = self.get(
            'documents:document_version_list', args=(self.document.pk,),
            follow=True
        )

        # Needed by the url view resolver
        response.context.current_app = None
        resolved_link = link_upload_version.resolve(context=response.context)

        self.assertEqual(resolved_link, None)
