from __future__ import unicode_literals

import shutil
import tempfile

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase

from documents.models import Document, DocumentType
from sources.literals import SOURCE_CHOICE_WEB_FORM
from sources.models import WebFormSource

from documents.test_models import (
    TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME, TEST_ADMIN_EMAIL,
    TEST_DOCUMENT_PATH, TEST_SMALL_DOCUMENT_PATH,
    TEST_DOCUMENT_DESCRIPTION, TEST_DOCUMENT_TYPE,
    TEST_NON_ASCII_DOCUMENT_FILENAME, TEST_NON_ASCII_DOCUMENT_PATH,
    TEST_NON_ASCII_COMPRESSED_DOCUMENT_PATH
)

from .literals import SOURCE_UNCOMPRESS_CHOICE_N, SOURCE_UNCOMPRESS_CHOICE_Y
from .models import WatchFolderSource


class UploadDocumentTestCase(TestCase):
    """
    Test creating documents
    """

    def setUp(self):
        self.document_type = DocumentType.objects.create(label=TEST_DOCUMENT_TYPE)
        ocr_settings = self.document_type.ocr_settings
        ocr_settings.auto_ocr = False
        ocr_settings.save()

        self.admin_user = User.objects.create_superuser(username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL, password=TEST_ADMIN_PASSWORD)
        self.client = Client()

    def test_issue_gh_163(self):
        """
        Non-ASCII chars in document name failing in upload via watch folder #163
        https://github.com/mayan-edms/mayan-edms/issues/163
        """

        temporary_directory = tempfile.mkdtemp()
        shutil.copy(TEST_NON_ASCII_DOCUMENT_PATH, temporary_directory)

        watch_folder = WatchFolderSource.objects.create(document_type=self.document_type, folder_path=temporary_directory, uncompress=SOURCE_UNCOMPRESS_CHOICE_Y)
        watch_folder.check_source()

        self.assertEqual(Document.objects.count(), 1)

        document = Document.objects.first()

        self.failUnlessEqual(document.exists(), True)
        self.failUnlessEqual(document.size, 17436)

        self.failUnlessEqual(document.file_mimetype, 'image/png')
        self.failUnlessEqual(document.file_mime_encoding, 'binary')
        self.failUnlessEqual(document.label, TEST_NON_ASCII_DOCUMENT_FILENAME)
        self.failUnlessEqual(document.page_count, 1)

        # Test Non-ASCII named documents inside Non-ASCII named compressed file

        shutil.copy(TEST_NON_ASCII_COMPRESSED_DOCUMENT_PATH, temporary_directory)

        watch_folder.check_source()
        document = Document.objects.all()[1]

        self.assertEqual(Document.objects.count(), 2)

        self.failUnlessEqual(document.exists(), True)
        self.failUnlessEqual(document.size, 17436)

        self.failUnlessEqual(document.file_mimetype, 'image/png')
        self.failUnlessEqual(document.file_mime_encoding, 'binary')
        self.failUnlessEqual(document.label, TEST_NON_ASCII_DOCUMENT_FILENAME)
        self.failUnlessEqual(document.page_count, 1)

        shutil.rmtree(temporary_directory)
