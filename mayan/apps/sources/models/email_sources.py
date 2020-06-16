import imaplib
import logging
import poplib

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from django.utils.encoding import force_bytes, force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.serialization import yaml_load
from mayan.apps.documents.models import Document
from mayan.apps.metadata.api import set_bulk_metadata
from mayan.apps.metadata.models import MetadataType

from ..exceptions import SourceException
from ..literals import (
    DEFAULT_IMAP_MAILBOX, DEFAULT_IMAP_SEARCH_CRITERIA,
    DEFAULT_IMAP_STORE_COMMANDS, DEFAULT_METADATA_ATTACHMENT_NAME,
    DEFAULT_POP3_TIMEOUT, SOURCE_CHOICE_EMAIL_IMAP, SOURCE_CHOICE_EMAIL_POP3,
    SOURCE_UNCOMPRESS_CHOICE_N, SOURCE_UNCOMPRESS_CHOICE_Y,
)

from .base import IntervalBaseModel

__all__ = ('IMAPEmail', 'POP3Email')
logger = logging.getLogger(name=__name__)


class EmailBaseModel(IntervalBaseModel):
    """
    POP3 email and IMAP email sources are non-interactive sources that
    periodically fetch emails from an email account using either the POP3 or
    IMAP email protocol. These sources are useful when users need to scan
    documents outside their office, they can photograph a paper document with
    their phones and send the image to a designated email that is setup as a
    Mayan POP3 or IMAP source. Mayan will periodically download the emails
    and process them as Mayan documents.
    """
    host = models.CharField(max_length=128, verbose_name=_('Host'))
    ssl = models.BooleanField(default=True, verbose_name=_('SSL'))
    port = models.PositiveIntegerField(blank=True, null=True, help_text=_(
        'Typical choices are 110 for POP3, 995 for POP3 over SSL, 143 for '
        'IMAP, 993 for IMAP over SSL.'), verbose_name=_('Port')
    )
    username = models.CharField(max_length=96, verbose_name=_('Username'))
    password = models.CharField(max_length=96, verbose_name=_('Password'))
    metadata_attachment_name = models.CharField(
        default=DEFAULT_METADATA_ATTACHMENT_NAME,
        help_text=_(
            'Name of the attachment that will contains the metadata type '
            'names and value pairs to be assigned to the rest of the '
            'downloaded attachments.'
        ), max_length=128, verbose_name=_('Metadata attachment name')
    )
    subject_metadata_type = models.ForeignKey(
        blank=True, help_text=_(
            'Select a metadata type to store the email\'s subject value. '
            'Must be a valid metadata type for the document type selected '
            'previously.'
        ), on_delete=models.CASCADE, null=True, related_name='email_subject',
        to=MetadataType, verbose_name=_('Subject metadata type')
    )
    from_metadata_type = models.ForeignKey(
        blank=True, help_text=_(
            'Select a metadata type to store the email\'s "from" value. '
            'Must be a valid metadata type for the document type selected '
            'previously.'
        ), on_delete=models.CASCADE, null=True, related_name='email_from',
        to=MetadataType, verbose_name=_('From metadata type')
    )
    store_body = models.BooleanField(
        default=True, help_text=_(
            'Store the body of the email as a text document.'
        ), verbose_name=_('Store email body')
    )

    objects = models.Manager()

    class Meta:
        verbose_name = _('Email source')
        verbose_name_plural = _('Email sources')

    @staticmethod
    def process_message(source, message_text):
        from flanker import mime

        metadata_dictionary = {}

        message = mime.from_string(force_bytes(message_text))

        if source.from_metadata_type:
            metadata_dictionary[
                source.from_metadata_type.name
            ] = message.headers.get('From')

        if source.subject_metadata_type:
            metadata_dictionary[
                source.subject_metadata_type.name
            ] = message.headers.get('Subject')

        document_ids, parts_metadata_dictionary = EmailBaseModel._process_message(source=source, message=message)

        metadata_dictionary.update(parts_metadata_dictionary)

        if metadata_dictionary:
            for document in Document.objects.filter(id__in=document_ids):
                set_bulk_metadata(
                    document=document,
                    metadata_dictionary=metadata_dictionary
                )

    @staticmethod
    def _process_message(source, message):
        counter = 1
        document_ids = []
        metadata_dictionary = {}

        # Messages are tree based, do nested processing of message parts until
        # a message with no children is found, then work out way up.
        if message.parts:
            for part in message.parts:
                part_document_ids, part_metadata_dictionary = EmailBaseModel._process_message(
                    source=source, message=part,
                )

                document_ids.extend(part_document_ids)
                metadata_dictionary.update(part_metadata_dictionary)
        else:
            # Treat inlines as attachments, both are extracted and saved as
            # documents
            if message.is_attachment() or message.is_inline():
                # Reject zero length attachments
                if len(message.body) == 0:
                    return document_ids, metadata_dictionary

                label = message.detected_file_name or 'attachment-{}'.format(counter)
                counter = counter + 1

                with ContentFile(content=message.body, name=label) as file_object:
                    if label == source.metadata_attachment_name:
                        metadata_dictionary = yaml_load(
                            stream=file_object.read()
                        )
                        logger.debug(
                            'Got metadata dictionary: %s',
                            metadata_dictionary
                        )
                    else:
                        documents = source.handle_upload(
                            document_type=source.document_type,
                            file_object=file_object, expand=(
                                source.uncompress == SOURCE_UNCOMPRESS_CHOICE_Y
                            )
                        )

                        for document in documents:
                            document_ids.append(document.pk)

            else:
                # If it is not an attachment then it should be a body message part.
                # Another option is to use message.is_body()
                if message.detected_content_type == 'text/html':
                    label = 'email_body.html'
                else:
                    label = 'email_body.txt'

                if source.store_body:
                    with ContentFile(content=force_bytes(message.body), name=label) as file_object:
                        documents = source.handle_upload(
                            document_type=source.document_type,
                            expand=SOURCE_UNCOMPRESS_CHOICE_N,
                            file_object=file_object
                        )

                        for document in documents:
                            document_ids.append(document.pk)

        return document_ids, metadata_dictionary

    def clean(self):
        if self.subject_metadata_type:
            if self.subject_metadata_type.pk not in self.document_type.metadata.values_list('metadata_type', flat=True):
                raise ValidationError(
                    {
                        'subject_metadata_type': _(
                            'Subject metadata type "%(metadata_type)s" is not '
                            'valid for the document type: %(document_type)s'
                        ) % {
                            'metadata_type': self.subject_metadata_type,
                            'document_type': self.document_type
                        }
                    }
                )

        if self.from_metadata_type:
            if self.from_metadata_type.pk not in self.document_type.metadata.values_list('metadata_type', flat=True):
                raise ValidationError(
                    {
                        'from_metadata_type': _(
                            '"From" metadata type "%(metadata_type)s" is not '
                            'valid for the document type: %(document_type)s'
                        ) % {
                            'metadata_type': self.from_metadata_type,
                            'document_type': self.document_type
                        }
                    }
                )


class IMAPEmail(EmailBaseModel):
    source_type = SOURCE_CHOICE_EMAIL_IMAP

    mailbox = models.CharField(
        default=DEFAULT_IMAP_MAILBOX,
        help_text=_('IMAP Mailbox from which to check for messages.'),
        max_length=64, verbose_name=_('Mailbox')
    )
    search_criteria = models.TextField(
        blank=True, default=DEFAULT_IMAP_SEARCH_CRITERIA, help_text=_(
            'Criteria to use when searching for messages to process. '
            'Use the format specified in '
            'https://tools.ietf.org/html/rfc2060.html#section-6.4.4'
        ), null=True, verbose_name=_('Search criteria')
    )
    store_commands = models.TextField(
        blank=True, default=DEFAULT_IMAP_STORE_COMMANDS, help_text=_(
            'IMAP STORE command to execute on messages after they are '
            'processed. One command per line. Use the commands specified in '
            'https://tools.ietf.org/html/rfc2060.html#section-6.4.6 or '
            'the custom commands for your IMAP server.'
        ), null=True, verbose_name=_('Store commands')
    )
    execute_expunge = models.BooleanField(
        default=True, help_text=_(
            'Execute the IMAP expunge command after processing each email '
            'message.'
        ), verbose_name=_('Execute expunge')
    )
    mailbox_destination = models.CharField(
        blank=True, help_text=_(
            'IMAP Mailbox to which processed messages will be copied.'
        ), max_length=96, null=True, verbose_name=_('Destination mailbox')
    )

    objects = models.Manager()

    class Meta:
        verbose_name = _('IMAP email')
        verbose_name_plural = _('IMAP email')

    def _check_source(self, test=False):
        logger.debug(msg='Starting IMAP email fetch')
        logger.debug('host: %s', self.host)
        logger.debug('ssl: %s', self.ssl)

        if self.ssl:
            server = imaplib.IMAP4_SSL(host=self.host, port=self.port)
        else:
            server = imaplib.IMAP4(host=self.host, port=self.port)

        server.login(user=self.username, password=self.password)
        try:
            server.select(mailbox=self.mailbox)
        except Exception as exception:
            raise SourceException(
                'Error selecting mailbox: {}; {}'.format(
                    self.mailbox, exception
                )
            )

        try:
            status, data = server.uid(
                'SEARCH', None, *self.search_criteria.strip().split()
            )
        except Exception as exception:
            raise SourceException(
                'Error executing search command; {}'.format(exception)
            )

        if data:
            # data is a space separated sequence of message uids
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
                    EmailBaseModel.process_message(
                        source=self, message_text=data[0][1]
                    )
                except Exception as exception:
                    raise SourceException(
                        'Error processing message uid: {}; {}'.format(
                            uid, exception
                        )
                    )

                if not test:
                    if self.store_commands:
                        for command in self.store_commands.split('\n'):
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

                    if self.mailbox_destination:
                        try:
                            server.uid(
                                'COPY', uid, self.mailbox_destination
                            )
                        except Exception as exception:
                            raise SourceException(
                                'Error copying message uid {} to mailbox {}; '
                                '{}'.format(
                                    uid, self.mailbox_destination, exception
                                )
                            )

                    if self.execute_expunge:
                        server.expunge()

        server.close()
        server.logout()


class POP3Email(EmailBaseModel):
    source_type = SOURCE_CHOICE_EMAIL_POP3

    timeout = models.PositiveIntegerField(
        default=DEFAULT_POP3_TIMEOUT, verbose_name=_('Timeout')
    )

    objects = models.Manager()

    class Meta:
        verbose_name = _('POP email')
        verbose_name_plural = _('POP email')

    def _check_source(self, test=False):
        logger.debug(msg='Starting POP3 email fetch')
        logger.debug('host: %s', self.host)
        logger.debug('ssl: %s', self.ssl)

        if self.ssl:
            server = poplib.POP3_SSL(host=self.host, port=self.port)
        else:
            server = poplib.POP3(
                host=self.host, port=self.port, timeout=self.timeout
            )

        server.getwelcome()
        server.user(self.username)
        server.pass_(self.password)

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
            message_complete = force_text(b'\n'.join(message_lines))

            EmailBaseModel.process_message(
                source=self, message_text=message_complete
            )
            if not test:
                server.dele(which=message_number)

        server.quit()
