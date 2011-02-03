import os
import uuid
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _


def get_filename_from_uuid(instance, filename, directory='documents'):
    populate_file_extension_and_mimetype(instance, filename)
    stem, extension = os.path.splitext(filename)
    return '%s/%s%s' % (directory, instance.uuid, extension)

def populate_file_extension_and_mimetype(instance, filename):
    # First populate the file extension and mimetype
    instance.file_mimetype, encoding = guess_type(filename) or ""
    slug, instance.file_extension = os.path.splitext(filename)
    #instance.slug, instance.extension = os.path.splitext(filename)

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
    #file = models.FileField(upload_to=get_filename_from_uuid)#lambda i,f: 'documents/%s' % i.uuid)
    #file_mimetype = models.CharField(max_length=50, default="", editable=False)
    #file_extension = models.CharField(max_length=10, default="", editable=False)

    date_added   = models.DateTimeField("added", auto_now_add=True)
    date_updated = models.DateTimeField("updated", auto_now=True)
    
    
    #def save_file(self, contents, save=False):
    #    " Save a file, creating a new document_version if necessary. "
    #    self.file.save(contents.name, contents, save=save)
    #    # This is now done elsewhere
    #    #self.file_mimetype = guess_type(contents.name) or ""
    #    #try:
    #        #self.file_extension = contents[contents.rindex(".")+1:] or ""
    #    #except ValueError:
    #        #pass
    #    #self.save()

    class Meta:
        verbose_name = _(u'document')
        verbose_name_plural = _(u"documents")
        
    def __unicode__(self):
        return self.uuid

    #@property
    #def friendly_filename(self):
    #    """ A friendly filename (ie not the UUID) for the user to see when they download.
    #        Overload this with eg a slug field. 
    #    """
    #    return 'untitled.%s' % self.file_extension


    #def already(self, mode, request):
    #    """ Tests if a user has already viewed, downloaded or sent this document. 
    #        Assumes this model has a log of document interactions.
    #    """
    #    mode = getattr(DocumentInteractionBase.MODES, mode.upper())
    #
    #    if request.user.is_anonymous():
    #        return bool(self.interactions.filter(mode=mode, session_key=request.session.session_key))
    #    else:
    #        return bool(self.interactions.filter(mode=mode, user=request.user))

    #@property               
    #def file_thumbnail_small(self):
    #    # TODO: subclass DjangoThumbnail to remove UUID from URL
    #    if DjangoThumbnail:
    #        return DjangoThumbnail(self.file.name, (200,200))

    #@property               
    #def file_thumbnail_medium(self):
    #    # TODO: subclass DjangoThumbnail to remove UUID from URL
    #    if DjangoThumbnail:
    #        return DjangoThumbnail(self.file.name, (600,600))


class MetadataType(models.Model):
    name = models.CharField(max_length=32, verbose_name=_(u'name'))
    default = models.CharField(max_length=64, blank=True, null=True, verbose_name=_(u'default'))
    lookup = models.CharField(max_length=64, blank=True, null=True, verbose_name=_(u'lookup'))
    #datatype = models.
    
    def __unicode__(self):
        return self.name
        
    class Meta:
        verbose_name = _(u'metadata type')
        verbose_name_plural = _(u"metadata types")

#    @models.permalink
#    def get_absolute_url(self):
#        return ('state_list', [])


class DocumentTypeMetadataTypeConnector(models.Model):
    document_type = models.ForeignKey(DocumentType, verbose_name=_(u'document type'))
    metadata_type = models.ForeignKey(MetadataType, verbose_name=_(u'metadata type'))
    #override default
    #create index dir
    
    def __unicode__(self):
        return '%s <-> %s' %(self.document_type, self.metadata_type)

    class Meta:
        verbose_name = _(u"document type metadata type connector")
        verbose_name_plural = _(u"document type metadata type connectors")
