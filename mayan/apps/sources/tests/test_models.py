from __future__ import unicode_literals

import shutil

import mock
from pathlib2 import Path

from django.test import override_settings
from django.utils.encoding import force_text

from mayan.apps.common.tests import BaseTestCase
from mayan.apps.documents.models import Document, DocumentType
from mayan.apps.documents.tests import (
    DocumentTestMixin, TEST_COMPRESSED_DOCUMENT_PATH, TEST_DOCUMENT_TYPE_LABEL,
    TEST_NON_ASCII_DOCUMENT_FILENAME, TEST_NON_ASCII_DOCUMENT_PATH,
    TEST_NON_ASCII_COMPRESSED_DOCUMENT_PATH
)
from mayan.apps.metadata.models import MetadataType
from mayan.apps.storage.utils import mkdtemp

from ..literals import SOURCE_UNCOMPRESS_CHOICE_Y
from ..models import POP3Email, WatchFolderSource, WebFormSource
from ..models.email_sources import EmailBaseModel

from .literals import (
    TEST_EMAIL_ATTACHMENT_AND_INLINE, TEST_EMAIL_BASE64_FILENAME,
    TEST_EMAIL_BASE64_FILENAME_FROM, TEST_EMAIL_BASE64_FILENAME_SUBJECT,
    TEST_EMAIL_INLINE_IMAGE, TEST_EMAIL_NO_CONTENT_TYPE,
    TEST_EMAIL_NO_CONTENT_TYPE_STRING, TEST_EMAIL_ZERO_LENGTH_ATTACHMENT,
    TEST_WATCHFOLDER_SUBFOLDER
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

        with open(TEST_COMPRESSED_DOCUMENT_PATH, mode='rb') as file_object:
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

    def test_decode_email_zero_length_attachment(self):
        self._create_email_source()
        self.source.store_body = False
        self.source.save()

        EmailBaseModel.process_message(
            source=self.source, message_text=TEST_EMAIL_ZERO_LENGTH_ATTACHMENT
        )

        self.assertEqual(Document.objects.count(), 0)

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
            ),
        )

    def test_decode_email_and_store_from_and_subject_as_metadata(self):
        metadata_from = MetadataType.objects.create(name='from')
        metadata_subject = MetadataType.objects.create(name='subject')
        self.document_type.metadata.create(metadata_type=metadata_from)
        self.document_type.metadata.create(metadata_type=metadata_subject)

        self._create_email_source()
        self.source.from_metadata_type = metadata_from
        self.source.subject_metadata_type = metadata_subject
        self.source.save()

        EmailBaseModel.process_message(
            source=self.source, message_text=TEST_EMAIL_BASE64_FILENAME
        )

        document = Document.objects.first()

        self.assertEqual(
            document.label, 'Ampelm\xe4nnchen.txt'
        )
        self.assertEqual(
            document.metadata.get(metadata_type=metadata_from).value,
            TEST_EMAIL_BASE64_FILENAME_FROM
        )
        self.assertEqual(
            document.metadata.get(metadata_type=metadata_subject).value,
            TEST_EMAIL_BASE64_FILENAME_SUBJECT
        )

    def test_document_upload_no_body(self):
        self._create_email_source()
        self.source.store_body = False
        self.source.save()

        EmailBaseModel.process_message(
            source=self.source, message_text=TEST_EMAIL_ATTACHMENT_AND_INLINE
        )

        # Only two attachments, no body document
        self.assertEqual(1, Document.objects.count())

    def test_document_upload_with_body(self):
        self._create_email_source()

        EmailBaseModel.process_message(
            source=self.source, message_text=TEST_EMAIL_ATTACHMENT_AND_INLINE
        )

        # Only two attachments and a body document
        self.assertEqual(2, Document.objects.count())


@override_settings(OCR_AUTO_OCR=False)
class POP3SourceTestCase(BaseTestCase):
    class MockMailbox(object):
        def dele(self, which):
            return

        def getwelcome(self):
            return

        def list(self, which=None):
            return (None, ['1 test'])

        def pass_(self, password):
            return

        def quit(self):
            return

        def retr(self, which=None):
            return (
                1, [TEST_EMAIL_BASE64_FILENAME]
            )

        def user(self, username):
            return

    def setUp(self):
        super(POP3SourceTestCase, self).setUp()
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

    def tearDown(self):
        self.document_type.delete()
        super(POP3SourceTestCase, self).tearDown()

    @mock.patch('poplib.POP3_SSL')
    def test_download_document(self, mock_poplib):
        mock_poplib.return_value = POP3SourceTestCase.MockMailbox()
        self.source = POP3Email.objects.create(
            document_type=self.document_type, label='', host='', password='',
            username=''
        )

        self.source.check_source()
        self.assertEqual(
            Document.objects.first().label, 'Ampelm\xe4nnchen.txt'
        )


@override_settings(OCR_AUTO_OCR=False)
class WatchFolderTestCase(DocumentTestMixin, BaseTestCase):
    auto_upload_document = False

    def _create_watchfolder(self):
        return WatchFolderSource.objects.create(
            document_type=self.document_type,
            folder_path=self.temporary_directory,
            include_subdirectories=False,
            uncompress=SOURCE_UNCOMPRESS_CHOICE_Y
        )

    def setUp(self):
        super(WatchFolderTestCase, self).setUp()
        self.temporary_directory = mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temporary_directory)
        super(WatchFolderTestCase, self).tearDown()

    def test_subfolder_support_disabled(self):
        watch_folder = self._create_watchfolder()

        test_path = Path(self.temporary_directory)
        test_subfolder = test_path.joinpath(TEST_WATCHFOLDER_SUBFOLDER)
        test_subfolder.mkdir()

        shutil.copy(TEST_NON_ASCII_DOCUMENT_PATH, force_text(test_subfolder))
        watch_folder.check_source()
        self.assertEqual(Document.objects.count(), 0)

    def test_subfolder_support_enabled(self):
        watch_folder = self._create_watchfolder()
        watch_folder.include_subdirectories = True
        watch_folder.save()

        test_path = Path(self.temporary_directory)
        test_subfolder = test_path.joinpath(TEST_WATCHFOLDER_SUBFOLDER)
        test_subfolder.mkdir()

        shutil.copy(TEST_NON_ASCII_DOCUMENT_PATH, force_text(test_subfolder))
        watch_folder.check_source()
        self.assertEqual(Document.objects.count(), 1)

        document = Document.objects.first()

        self.assertEqual(document.exists(), True)
        self.assertEqual(document.size, 17436)

        self.assertEqual(document.file_mimetype, 'image/png')
        self.assertEqual(document.file_mime_encoding, 'binary')
        self.assertEqual(document.label, TEST_NON_ASCII_DOCUMENT_FILENAME)
        self.assertEqual(document.page_count, 1)

    def test_issue_gh_163(self):
        """
        Non-ASCII chars in document name failing in upload via watch folder
        gh-issue #163 https://github.com/mayan-edms/mayan-edms/issues/163
        """
        watch_folder = self._create_watchfolder()

        shutil.copy(TEST_NON_ASCII_DOCUMENT_PATH, self.temporary_directory)
        watch_folder.check_source()
        self.assertEqual(Document.objects.count(), 1)

        document = Document.objects.first()

        self.assertEqual(document.exists(), True)
        self.assertEqual(document.size, 17436)

        self.assertEqual(document.file_mimetype, 'image/png')
        self.assertEqual(document.file_mime_encoding, 'binary')
        self.assertEqual(document.label, TEST_NON_ASCII_DOCUMENT_FILENAME)
        self.assertEqual(document.page_count, 1)

    def test_issue_gh_163_expanded(self):
        """
        Test Non-ASCII named documents inside Non-ASCII named compressed file
        """
        watch_folder = self._create_watchfolder()

        shutil.copy(
            TEST_NON_ASCII_COMPRESSED_DOCUMENT_PATH, self.temporary_directory
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
