from __future__ import unicode_literals

import shutil

from django.test import override_settings

from common.utils import mkdtemp
from common.tests import BaseTestCase
from documents.models import Document, DocumentType
from documents.tests import (
    TEST_COMPRESSED_DOCUMENT_PATH, TEST_DOCUMENT_TYPE_LABEL,
    TEST_NON_ASCII_DOCUMENT_FILENAME, TEST_NON_ASCII_DOCUMENT_PATH,
    TEST_NON_ASCII_COMPRESSED_DOCUMENT_PATH
)

from ..literals import SOURCE_UNCOMPRESS_CHOICE_Y
from ..models import WatchFolderSource, WebFormSource, EmailBaseModel

from .literals import (
    TEST_EMAIL_ATTACHMENT_AND_INLINE, TEST_EMAIL_BASE64_FILENAME,
    TEST_EMAIL_INLINE_IMAGE, TEST_EMAIL_NO_CONTENT_TYPE,
    TEST_EMAIL_NO_CONTENT_TYPE_STRING
)


@override_settings(OCR_AUTO_OCR=False)
class CompressedUploadsTestCase(BaseTestCase):
    def setUp(self):
        super(CompressedUploadsTestCase, self).setUp()
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

    def tearDown(self):
        self.document_type.delete()
        super(CompressedUploadsTestCase, self).tearDown()

    def test_upload_compressed_file(self):
        source = WebFormSource(
            label='test source', uncompress=SOURCE_UNCOMPRESS_CHOICE_Y
        )

        with open(TEST_COMPRESSED_DOCUMENT_PATH) as file_object:
            source.handle_upload(
                document_type=self.document_type,
                file_object=file_object,
                expand=(source.uncompress == SOURCE_UNCOMPRESS_CHOICE_Y)
            )

        self.assertEqual(Document.objects.count(), 2)
        self.assertTrue(
            'first document.pdf' in Document.objects.values_list(
                'label', flat=True
            )
        )
        self.assertTrue(
            'second document.pdf' in Document.objects.values_list(
                'label', flat=True
            )
        )


@override_settings(OCR_AUTO_OCR=False)
class EmailFilenameDecodingTestCase(BaseTestCase):
    def setUp(self):
        super(EmailFilenameDecodingTestCase, self).setUp()
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

    def tearDown(self):
        self.document_type.delete()
        super(EmailFilenameDecodingTestCase, self).tearDown()

    def _create_email_source(self):
        self.source = EmailBaseModel(
            document_type=self.document_type,
            host='', username='', password='', store_body=True
        )

    def test_decode_email_base64_encoded_filename(self):
        """
        Test decoding of base64 encoded e-mail attachment filename.
        """
        self._create_email_source()
        EmailBaseModel.process_message(
            source=self.source, message_text=TEST_EMAIL_BASE64_FILENAME
        )

        self.assertEqual(
            Document.objects.first().label, 'Ampelm\xe4nnchen.txt'
        )

    def test_decode_email_no_content_type(self):
        self._create_email_source()
        EmailBaseModel.process_message(
            source=self.source, message_text=TEST_EMAIL_NO_CONTENT_TYPE
        )
        self.assertTrue(
            TEST_EMAIL_NO_CONTENT_TYPE_STRING in Document.objects.first().open().read()
        )

    def test_decode_email_with_inline_image(self):
        self._create_email_source()
        EmailBaseModel.process_message(
            source=self.source, message_text=TEST_EMAIL_INLINE_IMAGE
        )
        self.assertTrue(Document.objects.count(), 2)
        self.assertQuerysetEqual(
            ordered=False, qs=Document.objects.all(), values=(
                '<Document: test-01.png>', '<Document: email_body.html>'
            ),
        )

    def test_decode_email_with_attachment_and_inline_image(self):
        self._create_email_source()
        EmailBaseModel.process_message(
            source=self.source, message_text=TEST_EMAIL_ATTACHMENT_AND_INLINE
        )
        self.assertTrue(Document.objects.count(), 2)
        self.assertQuerysetEqual(
            ordered=False, qs=Document.objects.all(), values=(
                '<Document: test-01.png>', '<Document: email_body.html>',
                '<Document: test-02.png>'
            ),
        )


@override_settings(OCR_AUTO_OCR=False)
class UploadDocumentTestCase(BaseTestCase):
    """
    Test creating documents
    """
    def setUp(self):
        super(UploadDocumentTestCase, self).setUp()
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

    def tearDown(self):
        self.document_type.delete()
        super(UploadDocumentTestCase, self).tearDown()

    def test_issue_gh_163(self):
        """
        Non-ASCII chars in document name failing in upload via watch folder
        gh-issue #163 https://github.com/mayan-edms/mayan-edms/issues/163
        """

        temporary_directory = mkdtemp()
        shutil.copy(TEST_NON_ASCII_DOCUMENT_PATH, temporary_directory)

        watch_folder = WatchFolderSource.objects.create(
            document_type=self.document_type, folder_path=temporary_directory,
            uncompress=SOURCE_UNCOMPRESS_CHOICE_Y
        )
        watch_folder.check_source()

        self.assertEqual(Document.objects.count(), 1)

        document = Document.objects.first()

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
        document = Document.objects.all()[1]

        self.assertEqual(Document.objects.count(), 2)

        self.assertEqual(document.exists(), True)
        self.assertEqual(document.size, 17436)

        self.assertEqual(document.file_mimetype, 'image/png')
        self.assertEqual(document.file_mime_encoding, 'binary')
        self.assertEqual(document.label, TEST_NON_ASCII_DOCUMENT_FILENAME)
        self.assertEqual(document.page_count, 1)

        shutil.rmtree(temporary_directory)
