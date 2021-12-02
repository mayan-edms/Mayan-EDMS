from ...source_backends.email_backends import (
    SourceBackendIMAPEmail, SourceBackendPOP3Email
)
from ...source_backends.literals import (
    DEFAULT_EMAIL_IMAP_MAILBOX, DEFAULT_EMAIL_IMAP_SEARCH_CRITERIA,
    DEFAULT_EMAIL_IMAP_STORE_COMMANDS, DEFAULT_EMAIL_METADATA_ATTACHMENT_NAME,
    DEFAULT_EMAIL_POP3_TIMEOUT, DEFAULT_PERIOD_INTERVAL,
    SOURCE_UNCOMPRESS_CHOICE_NEVER
)

from ..literals import (
    TEST_EMAIL_ATTACHMENT_AND_INLINE, TEST_SOURCE_BACKEND_EMAIL_PATH
)

from .base_mixins import SourceTestMixin, SourceViewTestMixin


class EmailSourceBackendTestMixin(SourceTestMixin):
    _create_source_method = '_create_test_email_source_backend'
    _test_email_source_content = None

    def _create_test_email_source_backend(self, extra_data=None):
        backend_data = {
            'document_type_id': self.test_document_type.pk,
            'host': '',
            'interval': DEFAULT_PERIOD_INTERVAL,
            'metadata_attachment_name': DEFAULT_EMAIL_METADATA_ATTACHMENT_NAME,
            'password': '',
            'port': '',
            'ssl': True,
            'store_body': False,
            'username': '',
            '_test_content': TEST_EMAIL_ATTACHMENT_AND_INLINE
        }

        if extra_data:
            backend_data.update(extra_data)

        self._create_test_source(
            backend_path=TEST_SOURCE_BACKEND_EMAIL_PATH,
            backend_data=backend_data
        )


class IMAPEmailSourceTestMixin(SourceTestMixin):
    _create_source_method = '_create_test_imap_email_source'

    def _create_test_imap_email_source(self, extra_data=None):
        backend_data = {
            'document_type_id': self.test_document_type.pk,
            'execute_expunge': True,
            'host': '',
            'interval': DEFAULT_PERIOD_INTERVAL,
            'mailbox': DEFAULT_EMAIL_IMAP_MAILBOX,
            'mailbox_destination': '',
            'metadata_attachment_name': DEFAULT_EMAIL_METADATA_ATTACHMENT_NAME,
            'password': '',
            'port': '',
            'search_criteria': DEFAULT_EMAIL_IMAP_SEARCH_CRITERIA,
            'ssl': True,
            'store_body': False,
            'store_commands': DEFAULT_EMAIL_IMAP_STORE_COMMANDS,
            'uncompress': SOURCE_UNCOMPRESS_CHOICE_NEVER,
            'username': ''
        }

        if extra_data:
            backend_data.update(extra_data)

        self._create_test_source(
            backend_path=SourceBackendIMAPEmail.get_class_path(),
            backend_data=backend_data
        )


class POP3EmailSourceTestMixin(SourceTestMixin):
    _create_source_method = '_create_test_pop3_email_source'

    def _create_test_pop3_email_source(self, extra_data=None):
        backend_data = {
            'document_type_id': self.test_document_type.pk,
            'host': '',
            'interval': DEFAULT_PERIOD_INTERVAL,
            'metadata_attachment_name': DEFAULT_EMAIL_METADATA_ATTACHMENT_NAME,
            'password': '',
            'port': '',
            'ssl': True,
            'store_body': False,
            'timeout': DEFAULT_EMAIL_POP3_TIMEOUT,
            'uncompress': SOURCE_UNCOMPRESS_CHOICE_NEVER,
            'username': ''
        }

        if extra_data:
            backend_data.update(extra_data)

        self._create_test_source(
            backend_path=SourceBackendPOP3Email.get_class_path(),
            backend_data=backend_data
        )


class EmailSourceBackendViewTestMixin(SourceViewTestMixin):
    def _request_test_email_source_create_view(self, extra_data=None):
        data = {
            'document_type_id': self.test_document_type.pk,
            'host': '127.0.0.1',
            'interval': DEFAULT_PERIOD_INTERVAL,
            'metadata_attachment_name': DEFAULT_EMAIL_METADATA_ATTACHMENT_NAME,
            'port': '0',
            'ssl': True,
            'store_body': False,
            'username': 'username'
        }

        if extra_data:
            data.update(extra_data)

        return self._request_test_source_create_view(
            backend_path=TEST_SOURCE_BACKEND_EMAIL_PATH, extra_data=data
        )
