import mock

from django.core import mail

from mayan.apps.common.serialization import yaml_dump
from mayan.apps.documents.models import Document
from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.metadata.models import MetadataType
from mayan.apps.metadata.tests.mixins import MetadataTypeTestMixin

from .literals import (
    TEST_EMAIL_ATTACHMENT_AND_INLINE, TEST_EMAIL_BASE64_FILENAME,
    TEST_EMAIL_BASE64_FILENAME_ATTACHMENT_FILENAME,
    TEST_EMAIL_BASE64_FILENAME_FROM, TEST_EMAIL_BASE64_FILENAME_SUBJECT,
    TEST_EMAIL_BASE64_MESSAGE_ID, TEST_EMAIL_INLINE_IMAGE,
    TEST_EMAIL_NO_CONTENT_TYPE, TEST_EMAIL_NO_CONTENT_TYPE_STRING,
    TEST_EMAIL_ZERO_LENGTH_ATTACHMENT
)
from .mixins.email_source_mixins import (
    EmailSourceBackendTestMixin, IMAPEmailSourceTestMixin,
    POP3EmailSourceTestMixin
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
        self._create_test_email_source_backend(
            extra_data={'store_body': True}
        )
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

        # Silence expected errors in other apps.
        self._silence_logger(name='mayan.apps.converter.backends')

        source_backend_instance.process_documents()

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

        # Silence expected errors in other apps.
        self._silence_logger(name='mayan.apps.converter.backends')

        source_backend_instance.content = TEST_EMAIL_ATTACHMENT_AND_INLINE
        source_backend_instance.process_documents()

        self.assertTrue(Document.objects.count(), 2)
        self.assertQuerysetEqual(
            ordered=False, qs=Document.objects.all(), values=(
                '<Document: test-01.png>', '<Document: email_body.html>',
            ),
        )

    def test_document_upload_no_body(self):
        self._create_test_email_source_backend()
        source_backend_instance = self.test_source.get_backend_instance()

        # Silence expected errors in other apps.
        self._silence_logger(name='mayan.apps.converter.backends')

        source_backend_instance.content = TEST_EMAIL_ATTACHMENT_AND_INLINE
        source_backend_instance.process_documents()

        # Only two attachments, no body document.
        self.assertEqual(Document.objects.count(), 1)

    def test_document_upload_with_body(self):
        self._create_test_email_source_backend(
            extra_data={'store_body': True}
        )
        source_backend_instance = self.test_source.get_backend_instance()

        # Silence expected errors in other apps.
        self._silence_logger(name='mayan.apps.converter.backends')

        source_backend_instance.content = TEST_EMAIL_ATTACHMENT_AND_INLINE
        source_backend_instance.process_documents()

        # Only two attachments and a body document
        self.assertEqual(Document.objects.count(), 2)


class EmailSourceBackendMedatadataTestCase(
    EmailSourceBackendTestMixin, MetadataTypeTestMixin,
    GenericDocumentTestCase
):
    auto_create_test_source = False
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_metadata_type(add_test_document_type=True)

    def test_email_from_value_as_metadata(self):
        self._create_test_email_source_backend(
            extra_data={
                'from_metadata_type_id': self.test_metadata_type.pk,
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
            document.metadata.get(metadata_type=self.test_metadata_type).value,
            TEST_EMAIL_BASE64_FILENAME_FROM
        )

    def test_email_subjet_value_as_metadata(self):
        self._create_test_email_source_backend(
            extra_data={
                'subject_metadata_type_id': self.test_metadata_type.pk,
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
            document.metadata.get(metadata_type=self.test_metadata_type).value,
            TEST_EMAIL_BASE64_FILENAME_SUBJECT
        )

    def test_message_id_subjet_value_as_metadata(self):
        self._create_test_email_source_backend(
            extra_data={
                'message_id_metadata_type_id': self.test_metadata_type.pk,
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
            document.metadata.get(metadata_type=self.test_metadata_type).value,
            TEST_EMAIL_BASE64_MESSAGE_ID
        )


class EmailSourceBackendMetadataYAMLAttachmentTestCase(
    EmailSourceBackendTestMixin, GenericDocumentTestCase
):
    auto_create_test_source = False
    auto_upload_test_document = False

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

        mock_imaplib.return_value._add_test_message()
        mock_imaplib.return_value._add_test_message()

        test_imap_message_count = len(
            mock_imaplib.return_value.mailboxes['INBOX'].messages
        )

        source_backend_instance = self.test_source.get_backend_instance()

        source_backend_instance.process_documents()

        self.assertEqual(
            len(mock_imaplib.return_value.mailboxes['INBOX'].messages),
            test_imap_message_count - 1
        )

    def test_upload_simple_file(self):
        document_count = Document.objects.count()

        self._process_test_document()
        self.assertEqual(Document.objects.count(), document_count + 1)
        self.assertEqual(
            Document.objects.first().label,
            TEST_EMAIL_BASE64_FILENAME_ATTACHMENT_FILENAME
        )


class POP3SourceTestCase(
    POP3EmailSourceTestMixin, GenericDocumentTestCase
):
    auto_upload_test_document = False

    @mock.patch('poplib.POP3_SSL', autospec=True)
    def _process_test_document(self, mock_poplib):
        mock_poplib.return_value = MockPOP3Mailbox()

        mock_poplib.return_value._add_test_message()
        mock_poplib.return_value._add_test_message()

        test_imap_message_count = len(mock_poplib.return_value.messages)

        source_backend_instance = self.test_source.get_backend_instance()

        source_backend_instance.process_documents()

        self.assertEqual(
            len(mock_poplib.return_value.messages),
            test_imap_message_count - 1
        )

    def test_upload_simple_file(self):
        document_count = Document.objects.count()

        self._process_test_document()
        self.assertEqual(Document.objects.count(), document_count + 1)
        self.assertEqual(
            Document.objects.first().label,
            TEST_EMAIL_BASE64_FILENAME_ATTACHMENT_FILENAME
        )
