import logging

from django.db import models
from django.utils.encoding import force_text
from django.utils.functional import cached_property
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.models import DocumentFile, DocumentType

from .managers import DocumentTypeSettingsManager

logger = logging.getLogger(name=__name__)


class StoredDriver(models.Model):
    driver_path = models.CharField(
        max_length=255, unique=True, verbose_name=_('Driver path')
    )
    internal_name = models.CharField(
        db_index=True, max_length=128, unique=True,
        verbose_name=_('Internal name')
    )

    class Meta:
        ordering = ('internal_name',)
        verbose_name = _('Driver')
        verbose_name_plural = _('Drivers')

    def __str__(self):
        return force_text(s=self.driver_label)

    @cached_property
    def driver_class(self):
        return import_string(dotted_path=self.driver_path)

    @cached_property
    def driver_label(self):
        return self.driver_class.label


class DocumentTypeSettings(models.Model):
    """
    Model to store the file metadata settings for a document type.
    """
    document_type = models.OneToOneField(
        on_delete=models.CASCADE, related_name='file_metadata_settings',
        to=DocumentType, unique=True, verbose_name=_('Document type')
    )
    auto_process = models.BooleanField(
        default=True, verbose_name=_(
            'Automatically queue newly created documents for processing.'
        )
    )

    objects = DocumentTypeSettingsManager()

    class Meta:
        verbose_name = _('Document type settings')
        verbose_name_plural = _('Document types settings')

    def natural_key(self):
        return self.document_type.natural_key()
    natural_key.dependencies = ['documents.DocumentType']


class DocumentFileDriverEntry(models.Model):
    driver = models.ForeignKey(
        on_delete=models.CASCADE, related_name='driver_entries',
        to=StoredDriver, verbose_name=_('Driver')
    )
    document_file = models.ForeignKey(
        on_delete=models.CASCADE, related_name='file_metadata_drivers',
        to=DocumentFile, verbose_name=_('Document file')
    )

    class Meta:
        ordering = ('document_file', 'driver')
        unique_together = ('driver', 'document_file')
        verbose_name = _('Document file driver entry')
        verbose_name_plural = _('Document file driver entries')

    def __str__(self):
        return force_text(s=self.driver)

    def get_attribute_count(self):
        return self.entries.count()
    get_attribute_count.short_description = _('Attribute count')


class FileMetadataEntry(models.Model):
    document_file_driver_entry = models.ForeignKey(
        on_delete=models.CASCADE, related_name='entries',
        to=DocumentFileDriverEntry,
        verbose_name=_('Document file driver entry')
    )

    key = models.CharField(
        db_index=True, help_text=_('Name of the file metadata entry.'),
        max_length=255, verbose_name=_('Key')
    )
    value = models.CharField(
        db_index=True, help_text=_('Value of the file metadata entry.'),
        max_length=255, verbose_name=_('Value')
    )

    class Meta:
        ordering = ('key', 'value')
        verbose_name = _('File metadata entry')
        verbose_name_plural = _('File metadata entries')

    def __str__(self):
        return '{}: {}: {}'.format(
            self.document_file_driver_entry, self.key, self.value
        )
