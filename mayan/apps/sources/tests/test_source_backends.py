from pathlib import Path
import shutil

import mock

from django.core import mail
from django.core.files import File

from django_celery_beat.models import PeriodicTask

from mayan.apps.common.serialization import yaml_dump
from mayan.apps.documents.models import Document
from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.documents.tests.literals import (
    TEST_COMPRESSED_DOCUMENT_PATH, TEST_NON_ASCII_DOCUMENT_FILENAME,
    TEST_NON_ASCII_COMPRESSED_DOCUMENT_PATH, TEST_SMALL_DOCUMENT_CHECKSUM,
    TEST_SMALL_DOCUMENT_PATH
)
from mayan.apps.metadata.models import MetadataType

from ..source_backends.literals import SOURCE_UNCOMPRESS_CHOICE_ALWAYS

from .literals import (
    TEST_EMAIL_ATTACHMENT_AND_INLINE, TEST_EMAIL_BASE64_FILENAME,
    TEST_EMAIL_BASE64_FILENAME_ATTACHMENT_FILENAME, TEST_EMAIL_BASE64_FILENAME_FROM,
    TEST_EMAIL_BASE64_FILENAME_SUBJECT, TEST_EMAIL_INLINE_IMAGE,
    TEST_EMAIL_NO_CONTENT_TYPE, TEST_EMAIL_NO_CONTENT_TYPE_STRING,
    TEST_EMAIL_ZERO_LENGTH_ATTACHMENT, TEST_WATCHFOLDER_SUBFOLDER
)
from .mixins import (
    EmailSourceBackendTestMixin, IMAPEmailSourceTestMixin,
    InteractiveSourceBackendTestMixin, PeriodicSourceBackendTestMixin,
    POP3EmailSourceTestMixin, StagingFolderTestMixin,
    WatchFolderTestMixin, WebFormSourceTestMixin
)
from .mocks import MockIMAPServer, MockPOP3Mailbox


class EmailSourceBackendTestCase(
    EmailSourceBackendTestMixin, GenericDocumentTestCase
):
    auto_create_test_source = False
    auto_upload_test_document = False

    def test_decode_email_base64_encoded_filename(self):
        """
        Test decoding of base64 encoded e-mail attachment filename.
        """
        self._create_test_email_source_backend()
        source_backend_instance = self.test_source.get_backend_instance()
        source_backend_instance.content = TEST_EMAIL_BASE64_FILENAME

        source_backend_instance.process_documents()

        self.assertEqual(
            Document.objects.first().label,
            TEST_EMAIL_BASE64_FILENAME_ATTACHMENT_FILENAME
        )

    def test_decode_email_no_content_type(self):
        self._create_test_email_source_backend(extra_data={'store_body': True})
        source_backend_instance = self.test_source.get_backend_instance()

        source_backend_instance.content = TEST_EMAIL_NO_CONTENT_TYPE

        source_backend_instance.process_documents()

        self.assertTrue(
            TEST_EMAIL_NO_CONTENT_TYPE_STRING in Document.objects.first().file_latest.open().read()
        )

    def test_decode_email_zero_length_attachment(self):
        self._create_test_email_source_backend()
        source_backend_instance = self.test_source.get_backend_instance()

        source_backend_instance.content = TEST_EMAIL_ZERO_LENGTH_ATTACHMENT

        source_backend_instance.process_documents()

        self.assertEqual(Document.objects.count(), 0)

    def test_decode_email_with_inline_image(self):
        self._create_test_email_source_backend(
            extra_data={'store_body': True}
        )
        source_backend_instance = self.test_source.get_backend_instance()

        source_backend_instance.content = TEST_EMAIL_INLINE_IMAGE

        source_backend_instance.process_documents()

        # Silence expected errors in other apps.
        self._silence_logger(name='mayan.apps.converter.backends')

        self.assertTrue(Document.objects.count(), 2)
        self.assertQuerysetEqual(
            ordered=False, qs=Document.objects.all(), values=(
                '<Document: test-01.png>', '<Document: email_body.html>'
            ),
        )

    def test_decode_email_with_attachment_and_inline_image(self):
        self._create_test_email_source_backend(
            extra_data={'store_body': True}
        )
        source_backend_instance = self.test_source.get_backend_instance()

        source_backend_instance.content = TEST_EMAIL_ATTACHMENT_AND_INLINE
        source_backend_instance.process_documents()

        # Silence expected errors in other apps.
        self._silence_logger(name='mayan.apps.converter.backends')

        self.assertTrue(Document.objects.count(), 2)
        self.assertQuerysetEqual(
            ordered=False, qs=Document.objects.all(), values=(
                '<Document: test-01.png>', '<Document: email_body.html>',
            ),
        )

    def test_decode_email_and_store_from_and_subject_as_metadata(self):
        metadata_from = MetadataType.objects.create(name='from')
        metadata_subject = MetadataType.objects.create(name='subject')
        self.test_document_type.metadata.create(metadata_type=metadata_from)
        self.test_document_type.metadata.create(metadata_type=metadata_subject)

        self._create_test_email_source_backend(
            extra_data={
                'from_metadata_type_id': metadata_from.pk,
                'subject_metadata_type_id': metadata_subject.pk
            }
        )
        source_backend_instance = self.test_source.get_backend_instance()

        source_backend_instance.content = TEST_EMAIL_BASE64_FILENAME
        source_backend_instance.process_documents()

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
        self._create_test_email_source_backend()
        source_backend_instance = self.test_source.get_backend_instance()

        source_backend_instance.content = TEST_EMAIL_ATTACHMENT_AND_INLINE
        source_backend_instance.process_documents()

        # Silence expected errors in other apps.
        self._silence_logger(name='mayan.apps.converter.backends')

        # Only two attachments, no body document.
        self.assertEqual(1, Document.objects.count())

    def test_document_upload_with_body(self):
        self._create_test_email_source_backend(
            extra_data={'store_body': True}
        )
        source_backend_instance = self.test_source.get_backend_instance()

        source_backend_instance.content = TEST_EMAIL_ATTACHMENT_AND_INLINE
        source_backend_instance.process_documents()

        # Silence expected errors in other apps
        self._silence_logger(name='mayan.apps.converter.backends')

        # Only two attachments and a body document
        self.assertEqual(2, Document.objects.count())

    def test_metadata_yaml_attachment(self):
        TEST_METADATA_VALUE_1 = 'test value 1'
        TEST_METADATA_VALUE_2 = 'test value 2'

        test_metadata_type_1 = MetadataType.objects.create(
            name='test_metadata_type_1'
        )
        test_metadata_type_2 = MetadataType.objects.create(
            name='test_metadata_type_2'
        )
        self.test_document_type.metadata.create(
            metadata_type=test_metadata_type_1
        )
        self.test_document_type.metadata.create(
            metadata_type=test_metadata_type_2
        )

        test_metadata_yaml = yaml_dump(
            data={
                test_metadata_type_1.name: TEST_METADATA_VALUE_1,
                test_metadata_type_2.name: TEST_METADATA_VALUE_2,
            }
        )

        # Create email with a test attachment first, then the metadata.yaml
        # attachment.
        with mail.get_connection(
            backend='django.core.mail.backends.locmem.EmailBackend'
        ) as connection:
            email_message = mail.EmailMultiAlternatives(
                body='test email body', connection=connection,
                subject='test email subject', to=['test@example.com'],
            )

            email_message.attach(
                filename='test_attachment',
                content='test_content',
            )

            email_message.attach(
                filename='metadata.yaml',
                content=test_metadata_yaml,
            )

            email_message.send()

        self._create_test_email_source_backend(
            extra_data={'store_body': True}
        )
        source_backend_instance = self.test_source.get_backend_instance()

        source_backend_instance.content = mail.outbox[0].message()

        source_backend_instance.process_documents()

        self.assertEqual(Document.objects.count(), 2)

        for document in Document.objects.all():
            self.assertEqual(
                document.metadata.get(metadata_type=test_metadata_type_1).value,
                TEST_METADATA_VALUE_1
            )
            self.assertEqual(
                document.metadata.get(metadata_type=test_metadata_type_2).value,
                TEST_METADATA_VALUE_2
            )


class IMAPSourceBackendTestCase(
    IMAPEmailSourceTestMixin, GenericDocumentTestCase
):
    auto_upload_test_document = False

    @mock.patch('imaplib.IMAP4_SSL', autospec=True)
    def _process_test_document(self, mock_imaplib):
        mock_imaplib.return_value = MockIMAPServer()

        source_backend_instance = self.test_source.get_backend_instance()

        source_backend_instance.process_documents()

    def test_upload_simple_file(self):
        document_count = Document.objects.count()

        self._process_test_document()
        self.assertEqual(Document.objects.count(), document_count + 1)
        self.assertEqual(
            Document.objects.first().label,
            TEST_EMAIL_BASE64_FILENAME_ATTACHMENT_FILENAME
        )


class PeriodicSourceBackendTestCase(
    PeriodicSourceBackendTestMixin, GenericDocumentTestCase
):
    auto_upload_test_document = False

    def test_periodic_source_delete(self):
        periodic_task_count = PeriodicTask.objects.count()

        self.test_source.delete()

        self.assertEqual(PeriodicTask.objects.count(), periodic_task_count - 1)

    def test_periodic_source_save(self):
        periodic_task_count = PeriodicTask.objects.count()

        self.test_source.save()

        self.assertEqual(PeriodicTask.objects.count(), periodic_task_count)


class POP3SourceTestCase(
    POP3EmailSourceTestMixin, GenericDocumentTestCase
):
    auto_upload_test_document = False

    @mock.patch('poplib.POP3_SSL', autospec=True)
    def _process_test_document(self, mock_poplib):
        mock_poplib.return_value = MockPOP3Mailbox()

        source_backend_instance = self.test_source.get_backend_instance()

        source_backend_instance.process_documents()

    def test_upload_simple_file(self):
        document_count = Document.objects.count()

        self._process_test_document()
        self.assertEqual(Document.objects.count(), document_count + 1)
        self.assertEqual(
            Document.objects.first().label,
            TEST_EMAIL_BASE64_FILENAME_ATTACHMENT_FILENAME
        )


class StagingFolderSourceBackendTestCase(
    StagingFolderTestMixin, InteractiveSourceBackendTestMixin,
    GenericDocumentTestCase
):
    auto_create_test_source = False
    auto_upload_test_document = False

    def _process_test_document(self, test_file_path=TEST_SMALL_DOCUMENT_PATH):
        source_backend_instance = self.test_source.get_backend_instance()

        self.test_forms = {
            'document_form': self.test_document_form,
            'source_form': InteractiveSourceBackendTestMixin.MockSourceForm(
                staging_file_id=self.test_staging_folder_file.encoded_filename
            ),
        }

        source_backend_instance.process_documents(
            document_type=self.test_document_type, forms=self.test_forms,
            request=self.get_test_request()
        )

    def test_upload_simple_file(self):
        self._create_test_staging_folder()

        self._copy_test_staging_folder_document()

        document_count = Document.objects.count()

        self._process_test_document()

        self.assertEqual(Document.objects.count(), document_count + 1)
        self.assertEqual(
            Document.objects.first().file_latest.checksum,
            TEST_SMALL_DOCUMENT_CHECKSUM
        )

    def test_delete_after_upload(self):
        self._create_test_staging_folder(
            extra_data={'delete_after_upload': True}
        )

        self._copy_test_staging_folder_document()

        document_count = Document.objects.count()

        self._process_test_document()

        self.assertEqual(Document.objects.count(), document_count + 1)
        self.assertEqual(
            Document.objects.first().file_latest.checksum,
            TEST_SMALL_DOCUMENT_CHECKSUM
        )

        path = Path(self.test_source.get_backend_data()['folder_path'])

        self.assertEqual(sum(1 for x in path.glob('*') if x.is_file()), 0)


class WatchFolderSourceBackendTestCase(
    WatchFolderTestMixin, GenericDocumentTestCase
):
    auto_create_test_source = False
    auto_upload_test_document = False

    def test_upload_simple_file(self):
        self._create_test_watchfolder()

        document_count = Document.objects.count()

        shutil.copy(src=TEST_SMALL_DOCUMENT_PATH, dst=self.temporary_directory)

        self.test_source.get_backend_instance().process_documents()

        self.assertEqual(Document.objects.count(), document_count + 1)
        self.assertEqual(
            Document.objects.first().file_latest.checksum,
            TEST_SMALL_DOCUMENT_CHECKSUM
        )

    def test_subfolder_disabled(self):
        self._create_test_watchfolder()

        test_path = Path(self.temporary_directory)
        test_subfolder = test_path.joinpath(TEST_WATCHFOLDER_SUBFOLDER)
        test_subfolder.mkdir()

        shutil.copy(
            src=TEST_SMALL_DOCUMENT_PATH, dst=test_subfolder
        )

        document_count = Document.objects.count()

        self.test_source.get_backend_instance().process_documents()
        self.assertEqual(Document.objects.count(), document_count)

    def test_subfolder_enabled(self):
        self._create_test_watchfolder(
            extra_data={'include_subdirectories': True}
        )

        test_path = Path(self.temporary_directory)
        test_subfolder = test_path.joinpath(TEST_WATCHFOLDER_SUBFOLDER)
        test_subfolder.mkdir()

        shutil.copy(src=TEST_SMALL_DOCUMENT_PATH, dst=test_subfolder)

        document_count = Document.objects.count()

        self.test_source.get_backend_instance().process_documents()

        self.assertEqual(Document.objects.count(), document_count + 1)

        document = Document.objects.first()

        self.assertEqual(
            document.file_latest.checksum, TEST_SMALL_DOCUMENT_CHECKSUM
        )

    def test_non_ascii_file_in_non_ascii_compressed_file(self):
        """
        Test Non-ASCII named documents inside Non-ASCII named compressed
        file. GitHub issue #163.
        """
        self._create_test_watchfolder(
            extra_data={'uncompress': SOURCE_UNCOMPRESS_CHOICE_ALWAYS}
        )

        shutil.copy(
            src=TEST_NON_ASCII_COMPRESSED_DOCUMENT_PATH,
            dst=self.temporary_directory
        )

        document_count = Document.objects.count()

        self.test_source.get_backend_instance().process_documents()

        self.assertEqual(Document.objects.count(), document_count + 1)

        document = Document.objects.first()

        self.assertEqual(document.label, TEST_NON_ASCII_DOCUMENT_FILENAME)
        self.assertEqual(document.file_latest.exists(), True)
        self.assertEqual(document.file_latest.size, 17436)
        self.assertEqual(document.file_latest.mimetype, 'image/png')
        self.assertEqual(document.file_latest.encoding, 'binary')


class WebFormSourceBackendTestCase(
    InteractiveSourceBackendTestMixin, WebFormSourceTestMixin,
    GenericDocumentTestCase
):
    auto_create_test_source = False
    auto_upload_test_document = False

    def _process_test_document(self, test_file_path=TEST_SMALL_DOCUMENT_PATH):
        source_backend_instance = self.test_source.get_backend_instance()

        with open(file=test_file_path, mode='rb') as file_object:
            self.test_forms = {
                'document_form': self.test_document_form,
                'source_form': InteractiveSourceBackendTestMixin.MockSourceForm(
                    file=File(file=file_object)
                ),
            }

            source_backend_instance.process_documents(
                document_type=self.test_document_type, forms=self.test_forms,
                request=self.get_test_request()
            )

    def test_upload_simple_file(self):
        self._create_test_web_form_source()

        document_count = Document.objects.count()

        self._process_test_document()

        self.assertEqual(Document.objects.count(), document_count + 1)
        self.assertEqual(
            Document.objects.first().file_latest.checksum,
            TEST_SMALL_DOCUMENT_CHECKSUM
        )

    def test_upload_compressed_file(self):
        self._create_test_web_form_source(
            extra_data={'uncompress': SOURCE_UNCOMPRESS_CHOICE_ALWAYS}
        )

        document_count = Document.objects.count()

        self._process_test_document(
            test_file_path=TEST_COMPRESSED_DOCUMENT_PATH
        )

        self.assertEqual(Document.objects.count(), document_count + 2)

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
