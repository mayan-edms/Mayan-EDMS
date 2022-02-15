import imaplib
import itertools
import logging
import poplib

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.utils.encoding import force_bytes, force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.serialization import yaml_load
from mayan.apps.metadata.models import MetadataType
from mayan.apps.storage.models import SharedUploadedFile

from ..classes import SourceBackend
from ..exceptions import SourceException

from .literals import (
    DEFAULT_EMAIL_IMAP_MAILBOX, DEFAULT_EMAIL_IMAP_SEARCH_CRITERIA,
    DEFAULT_EMAIL_IMAP_STORE_COMMANDS,
    DEFAULT_EMAIL_METADATA_ATTACHMENT_NAME, DEFAULT_EMAIL_POP3_TIMEOUT,
    SOURCE_INTERVAL_UNCOMPRESS_CHOICES
)
from .mixins import (
    SourceBackendCompressedMixin, SourceBackendPeriodicMixin,
    SourceBaseMixin
)

__all__ = (
    'SourceBackendEmailMixin', 'SourceBackendIMAPEmail',
    'SourceBackendPOP3Email'
)
logger = logging.getLogger(name=__name__)


class SourceBackendEmailMixin:
    @classmethod
    def get_setup_form_schema(cls):
        result = super().get_setup_form_schema()

        result['fields'].update(
            {
                'host': {
                    'class': 'django.forms.CharField',
                    'label': _('Host'),
                    'kwargs': {
                        'max_length': 128
                    },
                    'required': True
                },
                'ssl': {
                    'class': 'django.forms.BooleanField',
                    'default': True,
                    'label': _('SSL'),
                    'required': False
                },
                'port': {
                    'class': 'django.forms.IntegerField',
                    'help_text': _(
                        'Typical choices are 110 for POP3, 995 for POP3 '
                        'over SSL, 143 for IMAP, 993 for IMAP over SSL.'
                    ),
                    'kwargs': {
                        'min_value': 0
                    },
                    'label': _('Port'),
                },
                'username': {
                    'class': 'django.forms.CharField',
                    'kargs': {
                        'max_length': 128,
                    },
                    'label': _('Username'),
                },
                'password': {
                    'class': 'django.forms.CharField',
                    'kargs': {
                        'max_length': 128,
                    },
                    'label': _('Password'),
                    'required': False,
                },
                'metadata_attachment_name': {
                    'class': 'django.forms.CharField',
                    'default': DEFAULT_EMAIL_METADATA_ATTACHMENT_NAME,
                    'help_text': _(
                        'Name of the attachment that will contains the metadata type '
                        'names and value pairs to be assigned to the rest of the '
                        'downloaded attachments.'
                    ),
                    'kargs': {
                        'max_length': 128,
                    },
                    'label': _('Metadata attachment name'),
                },
                'from_metadata_type_id': {
                    'blank': True,
                    'class': 'django.forms.ChoiceField',
                    'help_text': _(
                        'Select a metadata type to store the email\'s '
                        '"from" value. Must be a valid metadata type for '
                        'the document type selected previously.'
                    ),
                    'kwargs': {
                        'choices': itertools.chain(
                            [(None, '---------')],
                            [(instance.id, instance) for instance in MetadataType.objects.all()],
                        )
                    },
                    'label': _('From metadata type'),
                    'null': True,
                    'required': False
                },
                'subject_metadata_type_id': {
                    'blank': True,
                    'class': 'django.forms.ChoiceField',
                    'help_text': _(
                        'Select a metadata type to store the email\'s '
                        'subject value. Must be a valid metadata type for '
                        'the document type selected previously.'
                    ),
                    'kwargs': {
                        'choices': itertools.chain(
                            [(None, '---------')],
                            [(instance.id, instance) for instance in MetadataType.objects.all()],
                        )
                    },
                    'label': _('Subject metadata type'),
                    'null': True,
                    'required': False
                },
                'message_id_metadata_type_id': {
                    'blank': True,
                    'class': 'django.forms.ChoiceField',
                    'help_text': _(
                        'Select a metadata type to store the email\'s '
                        'message ID value. Must be a valid metadata type '
                        'for the document type selected previously.'
                    ),
                    'kwargs': {
                        'choices': itertools.chain(
                            [(None, '---------')],
                            [(instance.id, instance) for instance in MetadataType.objects.all()],
                        )
                    },
                    'label': _('Message ID metadata type'),
                    'null': True,
                    'required': False
                },
                'store_body': {
                    'class': 'django.forms.BooleanField',
                    'default': True,
                    'help_text': _(
                        'Store the body of the email as a text document.'
                    ),
                    'label': _('Store email body'),
                    'required': False
                }
            }
        )
        result['field_order'] = (
            'host', 'ssl', 'port', 'username', 'password',
            'metadata_attachment_name', 'from_metadata_type_id',
            'subject_metadata_type_id', 'message_id_metadata_type_id',
            'store_body'
        ) + result['field_order']

        result['widgets'].update(
            {
                'password': {
                    'class': 'django.forms.widgets.PasswordInput', 'kwargs': {
                        'render_value': True
                    }
                },
                'from_metadata_type_id': {
                    'class': 'django.forms.widgets.Select', 'kwargs': {
                        'attrs': {'class': 'select2'},
                    }
                },
                'subject_metadata_type_id': {
                    'class': 'django.forms.widgets.Select', 'kwargs': {
                        'attrs': {'class': 'select2'},
                    }
                },
                'message_id_metadata_type_id': {
                    'class': 'django.forms.widgets.Select', 'kwargs': {
                        'attrs': {'class': 'select2'},
                    }
                }
            }
        )

        return result

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.document_metadata = {}

    def process_message(self, message):
        from flanker import mime

        message = mime.from_string(string=force_bytes(s=message))

        shared_uploaded_files = self._process_message(message=message)

        # Process source metadata after messages to avoid the metadata
        # attachment to be used to override the source metadata.

        from_metadata_type = self.get_from_metadata_type()
        if from_metadata_type:
            self.document_metadata[from_metadata_type.pk] = message.headers.get('From')

        subject_metadata_type = self.get_subject_metadata_type()
        if subject_metadata_type:
            self.document_metadata[subject_metadata_type.pk] = message.headers.get('Subject')

        message_id_metadata_type = self.get_message_id_metadata_type()
        if message_id_metadata_type:
            self.document_metadata[message_id_metadata_type.pk] = message.headers.get('Message-ID')

        return shared_uploaded_files

    def _process_message(self, message):
        counter = 1
        shared_uploaded_files = []

        # Messages are tree based, do nested processing of message parts until
        # a message with no children is found, then work out way up.
        if message.parts:
            for part in message.parts:
                part_shared_uploaded_files = self._process_message(
                    message=part
                )

                shared_uploaded_files.extend(part_shared_uploaded_files)
        else:
            # Treat inlines as attachments, both are extracted and saved as
            # documents.
            if message.is_attachment() or message.is_inline():
                # Reject zero length attachments.
                if len(message.body) == 0:
                    return shared_uploaded_files

                label = message.detected_file_name or 'attachment-{}'.format(counter)
                counter = counter + 1

                with ContentFile(content=message.body, name=label) as file_object:
                    if label == self.kwargs['metadata_attachment_name']:
                        metadata_dictionary = yaml_load(
                            stream=file_object.read()
                        )
                        logger.debug(
                            'Got metadata dictionary: %s',
                            metadata_dictionary
                        )
                        for metadata_name, value in metadata_dictionary.items():
                            metadata = MetadataType.objects.get(name=metadata_name)
                            self.document_metadata[metadata.pk] = value
                    else:
                        shared_uploaded_files.append(
                            SharedUploadedFile.objects.create(
                                file=file_object, filename=label
                            )
                        )
            else:
                # If it is not an attachment then it should be a body message
                # part. Another option is to use message.is_body().
                if message.detected_content_type == 'text/html':
                    label = 'email_body.html'
                else:
                    label = 'email_body.txt'

                if self.kwargs['store_body']:
                    with ContentFile(content=force_bytes(message.body), name=label) as file_object:
                        shared_uploaded_files.append(
                            SharedUploadedFile.objects.create(
                                file=file_object, filename=label
                            )
                        )

        return shared_uploaded_files

    def callback(self, document_file, **kwargs):
        for metadata_type_id, value in kwargs['document_metadata'].items():
            metadata_type = MetadataType.objects.get(pk=metadata_type_id)

            document_file.document.metadata.create(
                metadata_type=metadata_type, value=value
            )

    def clean(self):
        document_type = self.get_document_type()

        form_metadata_type = self.get_from_metadata_type()
        subject_metadata_type = self.get_subject_metadata_type()
        message_id_metadata_type = self.get_message_id_metadata_type()

        if form_metadata_type:
            if not document_type.metadata.filter(metadata_type=form_metadata_type).exists():
                raise ValidationError(
                    {
                        'from_metadata_type': _(
                            '"From" metadata type "%(metadata_type)s" is not '
                            'valid for the document type: %(document_type)s'
                        ) % {
                            'metadata_type': form_metadata_type,
                            'document_type': document_type
                        }
                    }
                )

        if subject_metadata_type:
            if not document_type.metadata.filter(metadata_type=subject_metadata_type).exists():
                raise ValidationError(
                    {
                        'subject_metadata_type': _(
                            'Subject metadata type "%(metadata_type)s" is not '
                            'valid for the document type: %(document_type)s'
                        ) % {
                            'metadata_type': subject_metadata_type,
                            'document_type': document_type
                        }
                    }
                )

        if message_id_metadata_type:
            if not document_type.metadata.filter(metadata_type=message_id_metadata_type).exists():
                raise ValidationError(
                    {
                        'message_id_metadata_type': _(
                            'Message ID metadata type "%(metadata_type)s" is not '
                            'valid for the document type: %(document_type)s'
                        ) % {
                            'metadata_type': subject_metadata_type,
                            'document_type': document_type
                        }
                    }
                )

    def get_callback_kwargs(self):
        callback_kwargs = super().get_callback_kwargs()
        callback_kwargs.update(
            {'document_metadata': self.document_metadata}
        )

        return callback_kwargs

    def get_from_metadata_type(self):
        pk = self.kwargs.get('from_metadata_type_id')

        if pk:
            return MetadataType.objects.get(pk=pk)

    def get_subject_metadata_type(self):
        pk = self.kwargs.get('subject_metadata_type_id')

        if pk:
            return MetadataType.objects.get(pk=pk)

    def get_message_id_metadata_type(self):
        pk = self.kwargs.get('message_id_metadata_type_id')

        if pk:
            return MetadataType.objects.get(pk=pk)


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
            'null': True, 'required': False
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
            imap_module_name = 'IMAP4_SSL'
        else:
            imap_module_name = 'IMAP4'

        imap_module = getattr(imaplib, imap_module_name)

        kwargs = {
            'host': self.kwargs['host'], 'port': self.kwargs['port']
        }

        with imap_module(**kwargs) as server:
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
            else:
                try:
                    status, data = server.uid(
                        'SEARCH', None, *self.kwargs['search_criteria'].strip().split()
                    )
                except Exception as exception:
                    raise SourceException(
                        'Error executing search command; {}'.format(exception)
                    )
                else:
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
                            else:
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
                                else:
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
            pop3_module_name = 'POP3_SSL'
        else:
            pop3_module_name = 'POP3'

        pop3_module = getattr(poplib, pop3_module_name)

        kwargs = {
            'host': self.kwargs['host'], 'port': self.kwargs['port'],
            'timeout': self.kwargs['timeout']
        }

        server = pop3_module(**kwargs)
        try:
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

                return shared_uploaded_files
        finally:
            server.quit()
