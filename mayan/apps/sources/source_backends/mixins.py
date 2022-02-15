import json
import logging

from django import forms
from django.apps import apps
from django.utils.encoding import force_text
from django.utils.translation import ugettext, ugettext_lazy as _

from mayan.apps.documents.models.document_file_models import DocumentFile
from mayan.apps.documents.models.document_type_models import DocumentType
from mayan.apps.documents.tasks import task_document_file_upload

from ..classes import DocumentCreateWizardStep
from ..tasks import task_process_document_upload

from .literals import (
    DEFAULT_PERIOD_INTERVAL, SOURCE_INTERACTIVE_UNCOMPRESS_CHOICES,
    SOURCE_UNCOMPRESS_CHOICE_ALWAYS, SOURCE_UNCOMPRESS_CHOICE_ASK
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
                'user_id': user_id
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
