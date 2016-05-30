from __future__ import unicode_literals

import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.core.files.base import File
from django.test import TestCase, override_settings
from django.test.client import Client

from documents.models import Document, DocumentType
from documents.tests import (
    TEST_COMPRESSED_DOCUMENT_PATH, TEST_DOCUMENT_TYPE,
    TEST_NON_ASCII_DOCUMENT_FILENAME, TEST_NON_ASCII_DOCUMENT_PATH,
    TEST_NON_ASCII_COMPRESSED_DOCUMENT_PATH
)
from organizations.models import Organization
from organizations.utils import create_default_organization
from user_management.tests import (
    TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME
)

from ..literals import SOURCE_UNCOMPRESS_CHOICE_Y
from ..models import WatchFolderSource, WebFormSource


@override_settings(OCR_AUTO_OCR=False)
class UploadDocumentTestCase(TestCase):
    """
    Test creating documents
    """

    def setUp(self):
        create_default_organization()
        self.document_type = DocumentType.on_organization.create(
            label=TEST_DOCUMENT_TYPE
        )

        self.admin_user = get_user_model().objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )
        self.client = Client()

    def tearDown(self):
        self.document_type.delete()
        self.admin_user.delete()

        Organization.objects.all().delete()
        Organization.objects.clear_cache()

    def test_issue_gh_163(self):
        """
        Non-ASCII chars in document name failing in upload via watch folder
        gh-issue #163 https://github.com/mayan-edms/mayan-edms/issues/163
        """

        temporary_directory = tempfile.mkdtemp()
        shutil.copy(TEST_NON_ASCII_DOCUMENT_PATH, temporary_directory)

        watch_folder = WatchFolderSource.on_organization.create(
            document_type=self.document_type, folder_path=temporary_directory,
            uncompress=SOURCE_UNCOMPRESS_CHOICE_Y
        )
        watch_folder.check_source()

        self.assertEqual(Document.on_organization.count(), 1)

        document = Document.on_organization.first()

        self.assertEqual(document.exists(), True)
        self.assertEqual(document.size, 17436)

        self.assertEqual(document.file_mimetype, 'image/png')
        self.assertEqual(document.file_mime_encoding, 'binary')
        self.assertEqual(document.label, TEST_NON_ASCII_DOCUMENT_FILENAME)
        self.assertEqual(document.page_count, 1)

        # Test Non-ASCII named documents inside Non-ASCII named compressed file

        shutil.copy(
            TEST_NON_ASCII_COMPRESSED_DOCUMENT_PATH, temporary_directory
        )

        watch_folder.check_source()
        document = Document.on_organization.all()[1]

        self.assertEqual(Document.on_organization.count(), 2)

        self.assertEqual(document.exists(), True)
        self.assertEqual(document.size, 17436)

        self.assertEqual(document.file_mimetype, 'image/png')
        self.assertEqual(document.file_mime_encoding, 'binary')
        self.assertEqual(document.label, TEST_NON_ASCII_DOCUMENT_FILENAME)
        self.assertEqual(document.page_count, 1)

        shutil.rmtree(temporary_directory)


@override_settings(OCR_AUTO_OCR=False)
class CompressedUploadsTestCase(TestCase):
    def setUp(self):
        create_default_organization()

        self.document_type = DocumentType.on_organization.create(
            label=TEST_DOCUMENT_TYPE
        )

    def tearDown(self):
        self.document_type.delete()
        Organization.objects.all().delete()
        Organization.objects.clear_cache()

    def test_upload_compressed_file(self):
        source = WebFormSource(
            label='test source', uncompress=SOURCE_UNCOMPRESS_CHOICE_Y
        )

        with open(TEST_COMPRESSED_DOCUMENT_PATH) as file_object:
            source.handle_upload(
                document_type=self.document_type,
                file_object=File(file_object),
                expand=(source.uncompress == SOURCE_UNCOMPRESS_CHOICE_Y)
            )

        self.assertEqual(Document.on_organization.count(), 2)
        self.assertTrue(
            'first document.pdf' in Document.on_organization.values_list(
                'label', flat=True
            )
        )
        self.assertTrue(
            'second document.pdf' in Document.on_organization.values_list(
                'label', flat=True
            )
        )
