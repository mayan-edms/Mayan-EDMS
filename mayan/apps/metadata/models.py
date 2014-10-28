from __future__ import absolute_import

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from documents.models import Document, DocumentType

from .managers import MetadataTypeManager


class MetadataType(models.Model):
    """
    Define a type of metadata
    """
    name = models.CharField(unique=True, max_length=48, verbose_name=_(u'Name'), help_text=_(u'Do not use python reserved words, or spaces.'))
    title = models.CharField(max_length=48, verbose_name=_(u'Title'), blank=True, null=True)
    default = models.CharField(max_length=128, blank=True, null=True,
                               verbose_name=_(u'Default'),
                               help_text=_(u'Enter a string to be evaluated.'))
    # TODO: Add enable_lookup boolean to allow users to switch the lookup on and
    # off without losing the lookup expression
    lookup = models.TextField(blank=True, null=True,
                              verbose_name=_(u'Lookup'),
                              help_text=_(u'Enter a string to be evaluated that returns an iterable.'))
    # TODO: Add datatype choice: Date, Time, String, Number
    # TODO: Find a different way to let users know what models and functions are
    # available now that we removed these from the help_text
    objects = MetadataTypeManager()

    def __unicode__(self):
        return self.title if self.title else self.name

    def natural_key(self):
        return (self.name,)

    class Meta:
        ordering = ('title',)
        verbose_name = _(u'Metadata type')
        verbose_name_plural = _(u'Metadata types')


class DocumentMetadata(models.Model):
    """
    Link a document to a specific instance of a metadata type with it's
    current value
    """
    document = models.ForeignKey(Document, verbose_name=_(u'Document'), related_name='metadata')
    metadata_type = models.ForeignKey(MetadataType, verbose_name=_(u'Type'))
    value = models.CharField(max_length=255, blank=True, null=True, verbose_name=_(u'Value'), db_index=True)

    def __unicode__(self):
        return unicode(self.metadata_type)

    def save(self, *args, **kwargs):
        if self.metadata_type not in self.document.document_type.metadata.all():
            raise ValidationError(_('Metadata type is not valid for this document type.'))

        return super(DocumentMetadata, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u'Document metadata')
        verbose_name_plural = _(u'Document metadata')


class DocumentTypeDefaults(models.Model):
    """
    Default preselected metadata types per document type
    """
    document_type = models.ForeignKey(DocumentType, verbose_name=_(u'Document type'))
    default_metadata = models.ManyToManyField(MetadataType, blank=True, verbose_name=_(u'Metadata'))

    def __unicode__(self):
        return unicode(self.document_type)

    class Meta:
        verbose_name = _(u'Document type defaults')
        verbose_name_plural = _(u'Document types defaults')
