import logging

from django.apps import apps
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.common.literals import TIME_DELTA_UNIT_CHOICES
from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.common.serialization import yaml_load
from mayan.apps.common.validators import YAMLValidator
from mayan.apps.events.classes import (
    EventManagerMethodAfter, EventManagerSave
)
from mayan.apps.events.decorators import method_event

from ..classes import BaseDocumentFilenameGenerator
from ..events import (
    event_document_type_created, event_document_type_edited,
    event_document_type_quick_label_created,
    event_document_type_quick_label_deleted,
    event_document_type_quick_label_edited
)
from ..literals import DEFAULT_DELETE_PERIOD, DEFAULT_DELETE_TIME_UNIT
from ..managers import DocumentTypeManager
from ..permissions import permission_document_view
from ..settings import setting_language

__all__ = ('DocumentType', 'DocumentTypeFilename')
logger = logging.getLogger(name=__name__)


class DocumentType(ExtraDataModelMixin, models.Model):
    """
    Define document types or classes to which a specific set of
    properties can be attached
    """
    label = models.CharField(
        help_text=_('The name of the document type.'), max_length=96,
        unique=True, verbose_name=_('Label')
    )
    trash_time_period = models.PositiveIntegerField(
        blank=True, help_text=_(
            'Amount of time after which documents of this type will be '
            'moved to the trash.'
        ), null=True, verbose_name=_('Trash time period')
    )
    trash_time_unit = models.CharField(
        blank=True, choices=TIME_DELTA_UNIT_CHOICES, null=True, max_length=8,
        verbose_name=_('Trash time unit')
    )
    delete_time_period = models.PositiveIntegerField(
        blank=True, default=DEFAULT_DELETE_PERIOD, help_text=_(
            'Amount of time after which documents of this type in the trash '
            'will be deleted.'
        ), null=True, verbose_name=_('Delete time period')
    )
    delete_time_unit = models.CharField(
        blank=True, choices=TIME_DELTA_UNIT_CHOICES,
        default=DEFAULT_DELETE_TIME_UNIT, max_length=8, null=True,
        verbose_name=_('Delete time unit')
    )
    filename_generator_backend = models.CharField(
        default=BaseDocumentFilenameGenerator.get_default(), help_text=_(
            'The class responsible for producing the actual filename used '
            'to store the uploaded documents.'
        ), max_length=224, verbose_name=_('Filename generator backend')
    )
    filename_generator_backend_arguments = models.TextField(
        blank=True, help_text=_(
            'The arguments for the filename generator backend as a '
            'YAML dictionary.'
        ), validators=[YAMLValidator()], verbose_name=_(
            'Filename generator backend arguments'
        )
    )

    objects = DocumentTypeManager()

    class Meta:
        ordering = ('label',)
        verbose_name = _('Document type')
        verbose_name_plural = _('Documents types')

    def __str__(self):
        return self.label

    def delete(self, *args, **kwargs):
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        for document in Document.objects.filter(document_type=self):
            document.delete(to_trash=False)

        return super().delete(*args, **kwargs)

    @property
    def trashed_documents(self):
        TrashedDocument = apps.get_model(
            app_label='documents', model_name='TrashedDocument'
        )

        return TrashedDocument.objects.filter(document_type=self)

    def get_absolute_url(self):
        return reverse(
            viewname='documents:document_type_document_list', kwargs={
                'document_type_id': self.pk
            }
        )

    def get_document_count(self, user):
        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_document_view, queryset=self.documents,
            user=user
        )

        return queryset.count()

    def get_upload_filename(self, instance, filename):
        generator_klass = BaseDocumentFilenameGenerator.get(
            name=self.filename_generator_backend
        )
        generator_instance = generator_klass(
            **yaml_load(
                stream=self.filename_generator_backend_arguments or '{}'
            )
        )
        return generator_instance.upload_to(
            instance=instance, filename=filename
        )

    def natural_key(self):
        return (self.label,)

    def new_document(
        self, file_object, label=None, description=None, language=None,
        _user=None
    ):
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        try:
            document = Document(
                description=description or '', document_type=self,
                label=label or file_object.name,
                language=language or setting_language.value
            )
            document._event_keep_attributes = ('_event_actor',)
            document._event_actor = _user
            document.save()
        except Exception as exception:
            logger.critical(
                'Unexpected exception while trying to create new document '
                '"%s" from document type "%s"; %s',
                label or file_object.name, self, exception
            )
            raise
        else:
            try:
                document_file = document.file_new(
                    file_object=file_object, filename=label, _user=_user
                )
            except Exception as exception:
                logger.critical(
                    'Unexpected exception while trying to create initial '
                    'file for document %s; %s',
                    label or file_object.name, exception
                )
                raise
            else:
                return document, document_file

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_document_type_created,
            'target': 'self'
        },
        edited={
            'event': event_document_type_edited,
            'target': 'self'
        }
    )
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class DocumentTypeFilename(ExtraDataModelMixin, models.Model):
    """
    List of labels available to a specific document type for the
    quick rename functionality
    """
    document_type = models.ForeignKey(
        on_delete=models.CASCADE, related_name='filenames', to=DocumentType,
        verbose_name=_('Document type')
    )
    filename = models.CharField(
        db_index=True, max_length=128, verbose_name=_('Label')
    )
    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))

    class Meta:
        ordering = ('filename',)
        unique_together = ('document_type', 'filename')
        verbose_name = _('Quick label')
        verbose_name_plural = _('Quick labels')

    def __str__(self):
        return self.filename

    @method_event(
        event_manager_class=EventManagerMethodAfter,
        event=event_document_type_quick_label_deleted,
        target='document_type',
    )
    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_document_type_quick_label_created,
            'action_object': 'document_type',
            'target': 'self'
        },
        edited={
            'event': event_document_type_quick_label_edited,
            'action_object': 'document_type',
            'target': 'self'
        }
    )
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
