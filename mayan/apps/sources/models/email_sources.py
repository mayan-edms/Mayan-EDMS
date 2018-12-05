from __future__ import unicode_literals

import imaplib
import logging
import poplib

import yaml

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from django.utils.encoding import force_bytes
from django.utils.translation import ugettext_lazy as _

from mayan.apps.metadata.api import set_bulk_metadata
from mayan.apps.metadata.models import MetadataType

from ..literals import (
    DEFAULT_IMAP_MAILBOX, DEFAULT_METADATA_ATTACHMENT_NAME,
    DEFAULT_POP3_TIMEOUT, SOURCE_CHOICE_EMAIL_IMAP, SOURCE_CHOICE_EMAIL_POP3,
    SOURCE_UNCOMPRESS_CHOICE_N, SOURCE_UNCOMPRESS_CHOICE_Y,
)

from .base import IntervalBaseModel

__all__ = ('IMAPEmail', 'POP3Email')
logger = logging.getLogger(__name__)


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
            'downloaded attachments. Note: This attachment has to be the '
            'first attachment.'
        ), max_length=128, verbose_name=_('Metadata attachment name')
    )
    subject_metadata_type = models.ForeignKey(
        blank=True, help_text=_(
            'Select a metadata type valid for the document type selected in '
            'which to store the email\'s subject.'
        ), on_delete=models.CASCADE, null=True, related_name='email_subject',
        to=MetadataType, verbose_name=_('Subject metadata type')
    )
    from_metadata_type = models.ForeignKey(
        blank=True, help_text=_(
            'Select a metadata type valid for the document type selected in '
            'which to store the email\'s "from" value.'
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
    def process_message(source, message_text, message_properties=None):
        from flanker import mime

        counter = 1
        message = mime.from_string(force_bytes(message_text))
        metadata_dictionary = {}

        if not message_properties:
            message_properties = {}

        message_properties['Subject'] = message_properties.get(
            'Subject', message.headers.get('Subject')
        )

        message_properties['From'] = message_properties.get(
            'From', message.headers.get('From')
        )

        if source.subject_metadata_type:
            metadata_dictionary[
                source.subject_metadata_type.name
            ] = message_properties.get('Subject')

        if source.from_metadata_type:
            metadata_dictionary[
                source.from_metadata_type.name
            ] = message_properties.get('From')

        # Messages are tree based, do nested processing of message parts until
        # a message with no children is found, then work out way up.
        if message.parts:
            for part in message.parts:
                EmailBaseModel.process_message(
                    source=source, message_text=part.to_string(),
                    message_properties=message_properties
                )
        else:
            # Treat inlines as attachments, both are extracted and saved as
            # documents
            if message.is_attachment() or message.is_inline():

                # Reject zero length attachments
                if len(message.body) == 0:
                    return

                label = message.detected_file_name or 'attachment-{}'.format(counter)
                with ContentFile(content=message.body, name=label) as file_object:
                    if label == source.metadata_attachment_name:
                        metadata_dictionary = yaml.safe_load(
                            file_object.read()
                        )
                        logger.debug(
                            'Got metadata dictionary: %s', metadata_dictionary
                        )
                    else:
                        documents = source.handle_upload(
                            document_type=source.document_type,
                            file_object=file_object, expand=(
                                source.uncompress == SOURCE_UNCOMPRESS_CHOICE_Y
                            )
                        )
                        if metadata_dictionary:
                            for document in documents:
                                set_bulk_metadata(
                                    document=document,
                                    metadata_dictionary=metadata_dictionary
                                )
            else:
                # If it is not an attachment then it should be a body message part.
                # Another option is to use message.is_body()
                if message.detected_content_type == 'text/html':
                    label = 'email_body.html'
                else:
                    label = 'email_body.txt'

                if source.store_body:
                    with ContentFile(content=message.body, name=label) as file_object:
                        documents = source.handle_upload(
                            document_type=source.document_type,
                            file_object=file_object,
                            expand=SOURCE_UNCOMPRESS_CHOICE_N
                        )
                        if metadata_dictionary:
                            for document in documents:
                                set_bulk_metadata(
                                    document=document,
                                    metadata_dictionary=metadata_dictionary
                                )

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

    objects = models.Manager()

    class Meta:
        verbose_name = _('IMAP email')
        verbose_name_plural = _('IMAP email')

    # http://www.doughellmann.com/PyMOTW/imaplib/
    def check_source(self, test=False):
        logger.debug('Starting IMAP email fetch')
        logger.debug('host: %s', self.host)
        logger.debug('ssl: %s', self.ssl)

        if self.ssl:
            mailbox = imaplib.IMAP4_SSL(self.host, self.port)
        else:
            mailbox = imaplib.IMAP4(self.host, self.port)

        mailbox.login(self.username, self.password)
        mailbox.select(self.mailbox)

        status, data = mailbox.search(None, 'NOT', 'DELETED')
        if data:
            messages_info = data[0].split()
            logger.debug('messages count: %s', len(messages_info))

            for message_number in messages_info:
                logger.debug('message_number: %s', message_number)
                status, data = mailbox.fetch(message_number, '(RFC822)')
                EmailBaseModel.process_message(
                    source=self, message_text=data[0][1]
                )
                if not test:
                    mailbox.store(message_number, '+FLAGS', '\\Deleted')

        mailbox.expunge()
        mailbox.close()
        mailbox.logout()


class POP3Email(EmailBaseModel):
    source_type = SOURCE_CHOICE_EMAIL_POP3

    timeout = models.PositiveIntegerField(
        default=DEFAULT_POP3_TIMEOUT, verbose_name=_('Timeout')
    )

    objects = models.Manager()

    class Meta:
        verbose_name = _('POP email')
        verbose_name_plural = _('POP email')

    def check_source(self, test=False):
        logger.debug('Starting POP3 email fetch')
        logger.debug('host: %s', self.host)
        logger.debug('ssl: %s', self.ssl)

        if self.ssl:
            mailbox = poplib.POP3_SSL(self.host, self.port)
        else:
            mailbox = poplib.POP3(self.host, self.port, timeout=self.timeout)

        mailbox.getwelcome()
        mailbox.user(self.username)
        mailbox.pass_(self.password)
        messages_info = mailbox.list()

        logger.debug('messages_info:')
        logger.debug(messages_info)
        logger.debug('messages count: %s', len(messages_info[1]))

        for message_info in messages_info[1]:
            message_number, message_size = message_info.split()
            logger.debug('message_number: %s', message_number)
            logger.debug('message_size: %s', message_size)

            complete_message = '\n'.join(mailbox.retr(message_number)[1])

            EmailBaseModel.process_message(
                source=self, message_text=complete_message
            )
            if not test:
                mailbox.dele(message_number)

        mailbox.quit()
