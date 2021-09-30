import itertools
import json
import logging

from django import forms
from django.apps import apps
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.utils.encoding import force_bytes, force_text
from django.utils.translation import ugettext, ugettext_lazy as _

from mayan.apps.common.serialization import yaml_load
from mayan.apps.documents.models.document_file_models import DocumentFile
from mayan.apps.documents.models.document_type_models import DocumentType
from mayan.apps.documents.tasks import task_document_file_upload
from mayan.apps.metadata.models import MetadataType
from mayan.apps.storage.models import SharedUploadedFile

from ..classes import DocumentCreateWizardStep
from ..tasks import task_process_document_upload

from .literals import (
    DEFAULT_EMAIL_METADATA_ATTACHMENT_NAME, DEFAULT_PERIOD_INTERVAL,
    SOURCE_INTERACTIVE_UNCOMPRESS_CHOICES, SOURCE_UNCOMPRESS_CHOICE_ALWAYS,
    SOURCE_UNCOMPRESS_CHOICE_ASK
)

logger = logging.getLogger(name=__name__)


class SourceBaseMixin:
    def callback(self, document_file, **kwargs):
        return

    def clean(self):
        return

    def get_callback_kwargs(self):
        return {}

    def get_document(self):
        raise NotImplementedError

    def get_document_description(self):
        return None

    def get_document_file_action(self):
        return None

    def get_document_file_comment(self):
        return None

    def get_document_label(self):
        return None

    def get_document_language(self):
        return None

    def get_document_type(self):
        raise NotImplementedError

    def get_task_extra_kwargs(self):
        return {}

    def get_user(self):
        return None

    def process_document_file(self, **kwargs):
        self.process_kwargs = kwargs

        document = self.get_document()
        user = self.get_user()

        if user:
            user_id = user.pk
        else:
            user_id = None

        for self.shared_uploaded_file in self.get_shared_uploaded_files() or ():
            # Call the hooks here too as in the model for early detection and
            # exception raise when using the views.
            DocumentFile.execute_pre_create_hooks(
                kwargs={
                    'document': document,
                    'file_object': self.shared_uploaded_file,
                    'user': user
                }
            )

            kwargs = {
                'action': self.get_document_file_action(),
                'comment': self.get_document_file_comment(),
                'document_id': document.pk,
                'shared_uploaded_file_id': self.shared_uploaded_file.pk,
                'user_id': user_id
            }

            kwargs.update(self.get_task_extra_kwargs())

            task_document_file_upload.apply_async(kwargs=kwargs)

    def process_documents(self, **kwargs):
        self.process_kwargs = kwargs

        document_type = self.get_document_type()
        user = self.get_user()

        if user:
            user_id = user.pk
        else:
            user_id = None

        for self.shared_uploaded_file in self.get_shared_uploaded_files() or ():
            kwargs = {
                'callback_kwargs': self.get_callback_kwargs(),
                'description': self.get_document_description(),
                'document_type_id': document_type.pk,
                'label': self.get_document_label(),
                'language': self.get_document_language(),
                'shared_uploaded_file_id': self.shared_uploaded_file.pk,
                'source_id': self.model_instance_id,
                'user_id': user_id,
            }
            kwargs.update(self.get_task_extra_kwargs())

            task_process_document_upload.apply_async(kwargs=kwargs)


class SourceBackendCompressedMixin:
    uncompress_choices = SOURCE_INTERACTIVE_UNCOMPRESS_CHOICES

    @classmethod
    def get_setup_form_schema(cls):
        result = super().get_setup_form_schema()

        result['fields'].update(
            {
                'uncompress': {
                    'label': _('Uncompress'),
                    'class': 'django.forms.ChoiceField',
                    'default': SOURCE_UNCOMPRESS_CHOICE_ASK,
                    'help_text': _(
                        'Whether to expand or not compressed archives.'
                    ), 'kwargs': {
                        'choices': cls.uncompress_choices,
                    }, 'required': True
                }
            }
        )
        result['field_order'] = ('uncompress',) + result['field_order']

        result['widgets'].update(
            {
                'uncompress': {
                    'class': 'django.forms.widgets.Select', 'kwargs': {
                        'attrs': {'class': 'select2'},
                    }
                }
            }
        )
        return result

    @classmethod
    def get_upload_form_class(cls):
        class CompressedSourceUploadForm(super().get_upload_form_class()):
            expand = forms.BooleanField(
                label=_('Expand compressed files'), required=False,
                help_text=ugettext(
                    'Upload a compressed file\'s contained files as '
                    'individual documents.'
                )
            )

            def __init__(self, *args, **kwargs):
                self.field_order = ['expand']
                super().__init__(*args, **kwargs)

        return CompressedSourceUploadForm

    def get_expand(self):
        if self.kwargs['uncompress'] == SOURCE_UNCOMPRESS_CHOICE_ASK:
            return self.process_kwargs['forms']['source_form'].cleaned_data.get('expand')
        else:
            if self.kwargs['uncompress'] == SOURCE_UNCOMPRESS_CHOICE_ALWAYS:
                return True
            else:
                return False

    def get_task_extra_kwargs(self):
        return {'expand': self.get_expand()}


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
                    'label': _('SSL')
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


class SourceBackendInteractiveMixin:
    is_interactive = True

    def callback(self, document_file, **kwargs):
        DocumentCreateWizardStep.post_upload_process(
            document=document_file.document,
            query_string=kwargs.get('query_string', '')
        )

    def get_callback_kwargs(self):
        query_string = ''

        query_dict = self.process_kwargs['request'].GET.copy()
        query_dict.update(self.process_kwargs['request'].POST)

        # Convert into a string. Make sure it is a QueryDict object from a
        # request and not just a simple dictionary.
        if hasattr(query_dict, 'urlencode'):
            query_string = query_dict.urlencode()

        return {
            'query_string': query_string
        }

    def get_document(self):
        return self.process_kwargs['document']

    def get_document_description(self):
        return self.process_kwargs['forms']['document_form'].cleaned_data.get('description')

    def get_document_file_action(self):
        return int(self.process_kwargs['forms']['document_form'].cleaned_data.get('action'))

    def get_document_file_comment(self):
        return self.process_kwargs['forms']['document_form'].cleaned_data.get('comment')

    def get_document_label(self):
        return self.process_kwargs['forms']['document_form'].get_final_label(
            filename=force_text(self.shared_uploaded_file)
        )

    def get_document_language(self):
        return self.process_kwargs['forms']['document_form'].cleaned_data.get('language')

    def get_document_type(self):
        return self.process_kwargs['document_type']

    def get_user(self):
        if not self.process_kwargs['request'].user.is_anonymous:
            return self.process_kwargs['request'].user
        else:
            return None


class SourceBackendPeriodicMixin:
    @classmethod
    def get_setup_form_schema(cls):
        result = super().get_setup_form_schema()

        result['fields'].update(
            {
                'document_type_id': {
                    'class': 'django.forms.ChoiceField',
                    'default': '',
                    'help_text': _(
                        'Assign a document type to documents uploaded from this '
                        'source.'
                    ),
                    'kwargs': {
                        'choices': [(document_type.id, document_type) for document_type in DocumentType.objects.all()],
                    },
                    'label': _('Document type'),
                    'required': True
                },
                'interval': {
                    'class': 'django.forms.IntegerField',
                    'default': DEFAULT_PERIOD_INTERVAL,
                    'help_text': _(
                        'Interval in seconds between checks for new '
                        'documents.'
                    ),
                    'kwargs': {
                        'min_value': 0
                    },
                    'label': _('Interval'),
                    'required': True
                },
            }
        )
        result['field_order'] = ('document_type_id', 'interval',) + result['field_order']

        result['widgets'].update(
            {
                'document_type_id': {
                    'class': 'django.forms.widgets.Select', 'kwargs': {
                        'attrs': {'class': 'select2'},
                    }
                }
            }
        )

        return result

    def create(self):
        IntervalSchedule = apps.get_model(
            app_label='django_celery_beat', model_name='IntervalSchedule'
        )
        PeriodicTask = apps.get_model(
            app_label='django_celery_beat', model_name='PeriodicTask'
        )

        # Create a new interval or use an existing one
        interval_instance, created = IntervalSchedule.objects.get_or_create(
            every=self.kwargs['interval'], period='seconds'
        )

        PeriodicTask.objects.create(
            name=self.get_periodic_task_name(),
            interval=interval_instance,
            task='mayan.apps.sources.tasks.task_source_process_document',
            kwargs=json.dumps(obj={'source_id': self.model_instance_id})
        )

    def delete(self):
        self.delete_periodic_task(pk=self.model_instance_id)

    def get_document_type(self):
        return DocumentType.objects.get(pk=self.kwargs['document_type_id'])

    def delete_periodic_task(self, pk=None):
        PeriodicTask = apps.get_model(
            app_label='django_celery_beat', model_name='PeriodicTask'
        )

        try:
            periodic_task = PeriodicTask.objects.get(
                name=self.get_periodic_task_name(pk=pk)
            )

            interval_instance = periodic_task.interval

            if tuple(interval_instance.periodictask_set.values_list('id', flat=True)) == (periodic_task.pk,):
                # Only delete the interval if nobody else is using it.
                interval_instance.delete()
            else:
                periodic_task.delete()
        except PeriodicTask.DoesNotExist:
            logger.warning(
                'Tried to delete non existent periodic task "%s"',
                self.get_periodic_task_name(pk=pk)
            )

    def get_periodic_task_name(self, pk=None):
        return 'check_interval_source-{}'.format(pk or self.model_instance_id)

    def save(self):
        self.delete_periodic_task()
        self.create()
