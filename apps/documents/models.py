import os
import uuid
import mimetypes
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _


def get_filename_from_uuid(instance, filename, directory='documents'):
    populate_file_extension_and_mimetype(instance, filename)
    stem, extension = os.path.splitext(filename)
    return '%s/%s%s' % (directory, instance.uuid, extension)

def populate_file_extension_and_mimetype(instance, filename):
    # First populate the file extension and mimetype
    instance.file_mimetype, encoding = mimetypes.guess_type(filename) or ""
    instance.file_filename, instance.file_extension = os.path.splitext(filename)

class DocumentType(models.Model):
    name = models.CharField(max_length=32, verbose_name=_(u'name'))    
    
    def __unicode__(self):
        return self.name
        
        
class Document(models.Model):
    """ Minimum fields for a document entry.
        Inherit this model to customise document metadata, see BasicDocument for an example.
    """
    document_type = models.ForeignKey(DocumentType, verbose_name=_(u'document type'))
    file = models.FileField(upload_to=get_filename_from_uuid)#lambda i,f: 'documents/%s' % i.uuid)
    uuid = models.CharField(max_length=36, default=lambda:unicode(uuid.uuid4()), blank=True, editable=False)
    file_mimetype = models.CharField(max_length=50, default="", editable=False)
    file_filename = models.CharField(max_length=64, default="", editable=False)
    file_extension = models.CharField(max_length=10, default="", editable=False)
    date_added   = models.DateTimeField("added", auto_now_add=True)
    date_updated = models.DateTimeField("updated", auto_now=True)
    
    class Meta:
        verbose_name = _(u'document')
        verbose_name_plural = _(u'documents')
        ordering = ['-date_updated', '-date_added']
        
    def __unicode__(self):
        return self.uuid


class MetadataType(models.Model):
    name = models.CharField(max_length=32, verbose_name=_(u'name'))
    default = models.CharField(max_length=64, blank=True, null=True, verbose_name=_(u'default'))
    lookup = models.CharField(max_length=64, blank=True, null=True, verbose_name=_(u'lookup'))
    #datatype = models.
    
    def __unicode__(self):
        return self.name
        
    class Meta:
        verbose_name = _(u'metadata type')
        verbose_name_plural = _(u'metadata types')

#    @models.permalink
#    def get_absolute_url(self):
#        return ('state_list', [])


class DocumentTypeMetadataType(models.Model):
    document_type = models.ForeignKey(DocumentType, verbose_name=_(u'document type'))
    metadata_type = models.ForeignKey(MetadataType, verbose_name=_(u'metadata type'))
    #override default
    #create index dir? -bool
    #required? -bool
    
    def __unicode__(self):
        return '%s <-> %s' %(self.document_type, self.metadata_type)

    class Meta:
        verbose_name = _(u'document type metadata type connector')
        verbose_name_plural = _(u'document type metadata type connectors')


class DocumentMetadata(models.Model):
    document = models.ForeignKey(Document, verbose_name=_(u'document'))
    metadata_type = models.ForeignKey(MetadataType, verbose_name=_(u'metadata type'))
    value = models.TextField(blank=True, null=True, verbose_name=_(u'metadata value'))
 
    def __unicode__(self):
        return '%s <-> %s' %(self.document, self.metadata_type)

    class Meta:
        verbose_name = _(u'document metadata')
        verbose_name_plural = _(u'document metadata')
