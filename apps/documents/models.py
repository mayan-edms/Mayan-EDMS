import errno
import os
import mimetypes
from datetime import datetime
import sys

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
 
from dynamic_search.api import register

from documents.conf.settings import AVAILABLE_FUNCTIONS
from documents.conf.settings import AVAILABLE_MODELS
from documents.conf.settings import CHECKSUM_FUNCTION
from documents.conf.settings import UUID_FUNCTION
from documents.conf.settings import STORAGE_BACKEND
from documents.conf.settings import STORAGE_DIRECTORY_NAME
from documents.conf.settings import FILESYSTEM_FILESERVING_ENABLE
from documents.conf.settings import FILESYSTEM_FILESERVING_PATH
from documents.conf.settings import FILESYSTEM_SLUGIFY_PATHS
from documents.conf.settings import FILESYSTEM_MAX_RENAME_COUNT


if FILESYSTEM_SLUGIFY_PATHS == False:
    #Do not slugify path or filenames and extensions
    slugify = lambda x:x


def get_filename_from_uuid(instance, filename, directory=STORAGE_DIRECTORY_NAME):
    populate_file_extension_and_mimetype(instance, filename)
    return '%s/%s' % (directory, instance.uuid)

def populate_file_extension_and_mimetype(instance, filename):
    # First populate the file extension and mimetype
    instance.file_mimetype, encoding = mimetypes.guess_type(filename)
    if not instance.file_mimetype:
         instance.file_mimetype = u'unknown'
    filename, extension = os.path.splitext(filename)
    instance.file_filename = filename
    #remove prefix '.'
    instance.file_extension = extension[1:]
    

class DocumentType(models.Model):
    name = models.CharField(max_length=32, verbose_name=_(u'name'))    
    
    def __unicode__(self):
        return self.name


class Document(models.Model):
    """ Minimum fields for a document entry.
        Inherit this model to customise document metadata, see BasicDocument for an example.
    """
    document_type = models.ForeignKey(DocumentType, verbose_name=_(u'document type'))
    file = models.FileField(upload_to=get_filename_from_uuid, storage=STORAGE_BACKEND(), verbose_name=_(u'file'))
    uuid = models.CharField(max_length=48, default=UUID_FUNCTION(), blank=True, editable=False)
    file_mimetype = models.CharField(max_length=64, default='', editable=False)
    #FAT filename can be up to 255 using LFN
    file_filename = models.CharField(max_length=64, default='', editable=False)
    file_extension = models.CharField(max_length=16, default='', editable=False)
    date_added = models.DateTimeField(verbose_name=_(u'added'), auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name=_(u'updated'), auto_now=True)
    checksum = models.TextField(blank=True, null=True, verbose_name=_(u'checksum'), editable=False)
    description = models.TextField(blank=True, null=True, verbose_name=_(u'description'))
    
    class Meta:
        verbose_name = _(u'document')
        verbose_name_plural = _(u'documents')
        ordering = ['-date_added']
        
    def __unicode__(self):
        return '%s.%s' % (self.file_filename, self.file_extension)
      
    def get_fullname(self):
        return os.extsep.join([self.file_filename, self.file_extension])
        
    @models.permalink
    def get_absolute_url(self):
        return ('document_view', [self.id])

    def update_checksum(self, save=True):
        if self.exists():
            self.checksum = unicode(CHECKSUM_FUNCTION(self.file.read()))
            if save:
                self.save()
    
    def exists(self):
        return self.file.storage.exists(self.file.url)
        
    def save(self, *args, **kwargs):
        self.update_checksum(save=False)
        super(Document, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        #TODO: Might not execute when done in bulk from a queryset
        #topics/db/queries.html#topics-db-queries-delete
        self.delete_fs_links()
        super(Document, self).delete(*args, **kwargs)
        
    def create_fs_links(self):
        if FILESYSTEM_FILESERVING_ENABLE:
            if not self.exists():
                raise Exception(ugettext(u'Not creating metadata indexing, document not found in document storage'))
            metadata_dict = {'document':self}
            metadata_dict.update(dict([(metadata.metadata_type.name, slugify(metadata.value)) for metadata in self.documentmetadata_set.all()]))
                
            for metadata_index in self.document_type.metadataindex_set.all():
                if metadata_index.enabled:
                    try:
                        fabricated_directory = eval(metadata_index.expression, metadata_dict)
                        target_directory = os.path.join(FILESYSTEM_FILESERVING_PATH, fabricated_directory)
                        try:
                            os.makedirs(target_directory)
                        except OSError, exc:
                            if exc.errno == errno.EEXIST:
                                pass
                            else: 
                                raise OSError(ugettext(u'Unable to create metadata indexing directory: %s') % exc)
                       

                        next_available_filename(self, metadata_index, target_directory, slugify(self.file_filename), slugify(self.file_extension))
                    except NameError, exc:
                        #raise NameError(ugettext(u'Error in metadata indexing expression: %s') % exc)
                        #This should be a warning not an error
                        pass

    def delete_fs_links(self):
        if FILESYSTEM_FILESERVING_ENABLE:
            for document_metadata_index in self.documentmetadataindex_set.all():
                try:
                    os.unlink(document_metadata_index.filename)
                    document_metadata_index.delete()
                except OSError, exc:
                    if exc.errno == errno.ENOENT:
                        #No longer exits, so delete db entry anyway
                        document_metadata_index.delete()
                    else: 
                        raise OSError(ugettext(u'Unable to delete metadata indexing symbolic link: %s') % exc)
            
                path, filename = os.path.split(document_metadata_index.filename)
                
                #Cleanup directory of dead stuff
                #Delete siblings that are dead links
                try:
                    for f in os.listdir(path):
                        filepath = os.path.join(path, f)
                        if os.path.islink(filepath):
                            #Get link's source
                            source = os.readlink(filepath)
                            if os.path.isabs(source):
                                if not os.path.exists(source):
                                    #link's source is absolute and doesn't exit
                                    os.unlink(filepath)
                            else:
                                os.unlink(os.path.join(path, filepath))
                        elif os.path.isdir(filepath):
                            #is a directory, try to delete it
                            try:
                                os.removedirs(path)
                            except:
                                pass                            
                except OSError, exc:
                    pass

                #Remove the directory if it is empty
                try:
                    os.removedirs(path)
                except:
                    pass
           
def next_available_filename(document, metadata_index, path, filename, extension, suffix=0): 
    target = filename
    if suffix:
        target = '_'.join([filename, unicode(suffix)])
    filepath = os.path.join(path, os.extsep.join([target, extension]))
    matches=DocumentMetadataIndex.objects.filter(filename=filepath)
    if matches.count() == 0:
        document_metadata_index = DocumentMetadataIndex(
            document=document, metadata_index=metadata_index,
            filename=filepath)
        try:
            os.symlink(document.file.path, filepath)
            document_metadata_index.save()
        except OSError, exc:
            if exc.errno == errno.EEXIST:
                #This link should not exist, try to delete it
                try:
                    os.unlink(filepath)
                    #Try again with same suffix
                    return next_available_filename(document, metadata_index, path, filename, extension, suffix)
                except Exception, exc:
                    raise Exception(ugettext(u'Unable to create symbolic link, filename clash: %s; %s') % (filepath, exc))    
                
            else:
                raise OSError(ugettext(u'Unable to create symbolic link: %s; %s') % (filepath, exc))
        
        return filepath
    else:
        if suffix > FILESYSTEM_MAX_RENAME_COUNT:
            raise Exception(ugettext(u'Maximum rename count reached, not creating symbolic link'))
        return next_available_filename(document, metadata_index, path, filename, extension, suffix+1)
 
    
available_functions_string = (_(u' Available functions: %s') % ','.join(['%s()' % name for name, function in AVAILABLE_FUNCTIONS.items()])) if AVAILABLE_FUNCTIONS else ''
available_models_string = (_(u' Available models: %s') % ','.join([name for name, model in AVAILABLE_MODELS.items()])) if AVAILABLE_MODELS else ''

class MetadataType(models.Model):
    name = models.CharField(max_length=48, verbose_name=_(u'name'), help_text=_(u'Do not use python reserved words.'))
    title = models.CharField(max_length=48, verbose_name=_(u'title'), blank=True, null=True)
    default = models.CharField(max_length=128, blank=True, null=True,
        verbose_name=_(u'default'),
        help_text=_(u'Enter a string to be evaluated.%s') % available_functions_string)
    lookup = models.CharField(max_length=128, blank=True, null=True,
        verbose_name=_(u'lookup'),
        help_text=_(u'Enter a string to be evaluated.  Example: [user.get_full_name() for user in User.objects.all()].%s') % available_models_string)
    #TODO: datatype?
    
    def __unicode__(self):
        #return '%s - %s' % (self.name, self.title if self.title else self.name)
        return self.name
        
    class Meta:
        verbose_name = _(u'metadata type')
        verbose_name_plural = _(u'metadata types')


class DocumentTypeMetadataType(models.Model):
    document_type = models.ForeignKey(DocumentType, verbose_name=_(u'document type'))
    metadata_type = models.ForeignKey(MetadataType, verbose_name=_(u'metadata type'))
    required = models.BooleanField(default=True, verbose_name=_(u'required'))
    #TODO: override default for this document type
    
    def __unicode__(self):
        return unicode(self.metadata_type)

    class Meta:
        verbose_name = _(u'document type metadata type connector')
        verbose_name_plural = _(u'document type metadata type connectors')


class MetadataIndex(models.Model):
    document_type = models.ForeignKey(DocumentType, verbose_name=_(u'document type'))
    expression = models.CharField(max_length=128,
        verbose_name=_(u'indexing expression'),
        help_text=_(u'Enter a python string expression to be evaluated.  The slash caracter "/" acts as a directory delimiter.'))
    enabled = models.BooleanField(default=True, verbose_name=_(u'enabled'))
    
    def __unicode__(self):
        return unicode(self.expression)
        
    class Meta:
        verbose_name = _(u'metadata index')
        verbose_name_plural = _(u'metadata indexes')


class DocumentMetadataIndex(models.Model):
    document = models.ForeignKey(Document, verbose_name=_(u'document'))
    metadata_index = models.ForeignKey(MetadataIndex, verbose_name=_(u'metadata index'))
    filename = models.CharField(max_length=128, verbose_name=_(u'filename'))
    suffix = models.PositiveIntegerField(default=0, verbose_name=_(u'suffix'))

    def __unicode__(self):
        return unicode(self.filename)

    class Meta:
        verbose_name = _(u'document metadata index')
        verbose_name_plural = _(u'document metadata indexes')


class DocumentMetadata(models.Model):
    document = models.ForeignKey(Document, verbose_name=_(u'document'))
    metadata_type = models.ForeignKey(MetadataType, verbose_name=_(u'metadata type'))
    value = models.TextField(blank=True, null=True, verbose_name=_(u'metadata value'))
 
    def __unicode__(self):
        return unicode(self.metadata_type)

    class Meta:
        verbose_name = _(u'document metadata')
        verbose_name_plural = _(u'document metadata')


class DocumentTypeFilename(models.Model):
    document_type = models.ForeignKey(DocumentType, verbose_name=_(u'document type'))
    filename = models.CharField(max_length=64, verbose_name=_(u'filename'))
    enabled = models.BooleanField(default=True, verbose_name=_(u'enabled'))
    
    def __unicode__(self):
        return self.filename

    class Meta:
        ordering = ['filename']
        verbose_name = _(u'document type filename')
        verbose_name_plural = _(u'document types filenames')


class DocumentPage(models.Model):
    document = models.ForeignKey(Document, verbose_name=_(u'document'))
    content = models.TextField(blank=True, null=True, verbose_name=_(u'content'))
    page_label = models.CharField(max_length=32, blank=True, null=True, verbose_name=_(u'page label'))
    page_number = models.PositiveIntegerField(default=0, verbose_name=_(u'page number'))
        
    def __unicode__(self):
        return '%s - %s' % (self.page_number, self.page_label)

    class Meta:
        verbose_name = _(u'document page')
        verbose_name_plural = _(u'document pages')


register(Document, _(u'document'), ['document_type__name', 'file_mimetype', 'file_filename', 'file_extension', 'documentmetadata__value', 'documentpage__content'])
