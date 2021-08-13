import imaplib
import logging
import poplib

from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from ..classes import SourceBackend
from ..exceptions import SourceException

from .literals import (
    DEFAULT_EMAIL_IMAP_MAILBOX, DEFAULT_EMAIL_IMAP_SEARCH_CRITERIA,
    DEFAULT_EMAIL_IMAP_STORE_COMMANDS, DEFAULT_EMAIL_POP3_TIMEOUT,
    SOURCE_INTERVAL_UNCOMPRESS_CHOICES
)
from .mixins import (
    SourceBackendCompressedMixin, SourceBackendEmailMixin,
    SourceBackendPeriodicMixin, SourceBaseMixin
)

__all__ = ('SourceBackendIMAPEmail', 'SourceBackendPOP3Email')
logger = logging.getLogger(name=__name__)


class SourceBackendIMAPEmail(
    SourceBackendCompressedMixin, SourceBackendEmailMixin,
    SourceBackendPeriodicMixin, SourceBaseMixin, SourceBackend
):
    field_order = (
        'mailbox', 'search_criteria', 'store_commands', 'execute_expunge',
        'mailbox_destination'
    )
    fields = {
        'mailbox': {
            'class': 'django.forms.fields.CharField',
            'default': DEFAULT_EMAIL_IMAP_MAILBOX,
            'help_text': _('IMAP Mailbox from which to check for messages.'),
            'kwargs': {
                'max_length': 64,
            },
            'label': _('Mailbox')
        },
        'search_criteria': {
            'blank': True,
            'class': 'django.forms.fields.CharField',
            'default': DEFAULT_EMAIL_IMAP_SEARCH_CRITERIA,
            'help_text': _(
                'Criteria to use when searching for messages to process. '
                'Use the format specified in '
                'https://tools.ietf.org/html/rfc2060.html#section-6.4.4'
            ),
            'label': _('Search criteria'),
            'null': True,
        },
        'store_commands': {
            'blank': True,
            'class': 'django.forms.fields.CharField',
            'default': DEFAULT_EMAIL_IMAP_STORE_COMMANDS,
            'help_text': _(
                'IMAP STORE command to execute on messages after they are '
                'processed. One command per line. Use the commands specified in '
                'https://tools.ietf.org/html/rfc2060.html#section-6.4.6 or '
                'the custom commands for your IMAP server.'
            ),
            'label': _('Store commands'),
            'null': True,
        },
        'execute_expunge': {
            'class': 'django.forms.fields.BooleanField',
            'default': True,
            'help_text': _(
                'Execute the IMAP expunge command after processing each email '
                'message.'
            ),
            'label': _('Execute expunge'),
            'required': False
        },
        'mailbox_destination': {
            'blank': True,
            'class': 'django.forms.fields.CharField',
            'help_text': _(
                'IMAP Mailbox to which processed messages will be copied.'
            ),
            'label': _('Destination mailbox'),
            'max_length': 96,
            'null': True,
            'required': False
        }
    }
    label = _('IMAP email')
    uncompress_choices = SOURCE_INTERVAL_UNCOMPRESS_CHOICES
    widgets = {
        'search_criteria': {
            'class': 'django.forms.widgets.Textarea',
        },
        'store_commands': {
            'class': 'django.forms.widgets.Textarea',
        }
    }

    def get_shared_uploaded_files(self):
        dry_run = self.process_kwargs.get('dry_run', False)

        logger.debug(msg='Starting IMAP email fetch')
        logger.debug('host: %s', self.kwargs['host'])
        logger.debug('ssl: %s', self.kwargs['ssl'])

        if self.kwargs['ssl']:
            server = imaplib.IMAP4_SSL(
                host=self.kwargs['host'], port=self.kwargs['port']
            )
        else:
            server = imaplib.IMAP4(
                host=self.kwargs['host'], port=self.kwargs['port']
            )

        server.login(
            user=self.kwargs['username'], password=self.kwargs['password']
        )
        try:
            server.select(mailbox=self.kwargs['mailbox'])
        except Exception as exception:
            raise SourceException(
                'Error selecting mailbox: {}; {}'.format(
                    self.kwargs['mailbox'], exception
                )
            )

        try:
            status, data = server.uid(
                'SEARCH', None, *self.kwargs['search_criteria'].strip().split()
            )
        except Exception as exception:
            raise SourceException(
                'Error executing search command; {}'.format(exception)
            )

        if data:
            # data is a space separated sequence of message uids.
            uids = data[0].split()
            logger.debug('messages count: %s', len(uids))
            logger.debug('message uids: %s', uids)

            for uid in uids:
                logger.debug('message uid: %s', uid)

                try:
                    status, data = server.uid('FETCH', uid, '(RFC822)')
                except Exception as exception:
                    raise SourceException(
                        'Error fetching message uid: {}; {}'.format(
                            uid, exception
                        )
                    )

                try:
                    shared_uploaded_files = self.process_message(
                        message=data[0][1]
                    )
                except Exception as exception:
                    raise SourceException(
                        'Error processing message uid: {}; {}'.format(
                            uid, exception
                        )
                    )

                if not dry_run:
                    if self.kwargs['store_commands']:
                        for command in self.kwargs['store_commands'].split('\n'):
                            try:
                                args = [uid]
                                args.extend(command.strip().split(' '))
                                server.uid('STORE', *args)
                            except Exception as exception:
                                raise SourceException(
                                    'Error executing IMAP store command "{}" '
                                    'on message uid {}; {}'.format(
                                        command, uid, exception
                                    )
                                )

                    if self.kwargs['mailbox_destination']:
                        try:
                            server.uid(
                                'COPY', uid, self.kwargs['mailbox_destination']
                            )
                        except Exception as exception:
                            raise SourceException(
                                'Error copying message uid {} to mailbox {}; '
                                '{}'.format(
                                    uid, self.kwargs['mailbox_destination'], exception
                                )
                            )

                    if self.kwargs['execute_expunge']:
                        server.expunge()

        server.close()
        server.logout()

        return shared_uploaded_files


class SourceBackendPOP3Email(
    SourceBackendCompressedMixin, SourceBackendEmailMixin,
    SourceBackendPeriodicMixin, SourceBaseMixin, SourceBackend
):
    field_order = ('timeout', 'uncompress',)
    fields = {
        'timeout': {
            'class': 'django.forms.fields.IntegerField',
            'default': DEFAULT_EMAIL_POP3_TIMEOUT,
            'kwargs': {
                'min_value': 0
            },
            'label': _('Timeout')
        }
    }
    label = _('POP3 email')

    def get_shared_uploaded_files(self):
        dry_run = self.process_kwargs.get('dry_run', False)

        logger.debug(msg='Starting POP3 email fetch')
        logger.debug('host: %s', self.kwargs['host'])
        logger.debug('ssl: %s', self.kwargs['ssl'])

        if self.kwargs['ssl']:
            server = poplib.POP3_SSL(host=self.kwargs['host'], port=self.kwargs['port'])
        else:
            server = poplib.POP3(
                host=self.kwargs['host'], port=self.kwargs['port'], timeout=self.kwargs['timeout']
            )

        server.getwelcome()
        server.user(self.kwargs['username'])
        server.pass_(self.kwargs['password'])

        messages_info = server.list()

        logger.debug(msg='messages_info:')
        logger.debug(msg=messages_info)
        logger.debug('messages count: %s', len(messages_info[1]))

        for message_info in messages_info[1]:
            message_number, message_size = message_info.split()
            message_number = int(message_number)

            logger.debug('message_number: %s', message_number)
            logger.debug('message_size: %s', message_size)

            message_lines = server.retr(which=message_number)[1]
            message_complete = force_text(s=b'\n'.join(message_lines))

            shared_uploaded_files = self.process_message(
                message=message_complete
            )
            if not dry_run:
                server.dele(which=message_number)

        server.quit()

        return shared_uploaded_files
