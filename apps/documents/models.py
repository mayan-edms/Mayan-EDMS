import os
from datetime import datetime
import sys
from python_magic import magic

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q


from dynamic_search.api import register

from documents.conf.settings import AVAILABLE_FUNCTIONS
from documents.conf.settings import AVAILABLE_MODELS
from documents.conf.settings import CHECKSUM_FUNCTION
from documents.conf.settings import UUID_FUNCTION
from documents.conf.settings import PAGE_COUNT_FUNCTION
from documents.conf.settings import STORAGE_BACKEND
from documents.conf.settings import STORAGE_DIRECTORY_NAME
from documents.conf.settings import AVAILABLE_TRANSFORMATIONS
from documents.conf.settings import DEFAULT_TRANSFORMATIONS



def get_filename_from_uuid(instance, filename, directory=STORAGE_DIRECTORY_NAME):
    populate_file_extension_and_mimetype(instance, filename)
    return '%s/%s' % (directory, instance.uuid)

def populate_file_extension_and_mimetype(instance, filename):
    # First populate the file extension
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
    file_mime_encoding = models.CharField(max_length=64, default='', editable=False)
    #FAT filename can be up to 255 using LFN
    file_filename = models.CharField(max_length=255, default='', editable=False)
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
    
    
    def save(self, *args, **kwargs):
        internal_save = kwargs.pop('internal_save', False)
        super(Document, self).save(*args, **kwargs)
        if not internal_save:
            self.update_checksum(save=False)
            self.update_mimetype(save=False)
            self.update_page_count(save=False)
            self.apply_default_transformations()
            self.save(internal_save=True)

      
    def get_fullname(self):
        return os.extsep.join([self.file_filename, self.file_extension])

        
    def update_mimetype(self, save=True):
        try:
            mime = magic.Magic(mime=True)
            self.file_mimetype = mime.from_buffer(self.read())
            mime_encoding = magic.Magic(mime_encoding=True)
            self.file_mime_encoding = mime_encoding.from_buffer(self.read())
        except:
            self.file_mimetype = u'unknown'
            self.file_mime_encoding = u'unknown'
        finally:
            if save:
                self.save()
      
    def read(self, count=1024):
        return self.file.storage.open(self.file.url).read(count)

        
    @models.permalink
    def get_absolute_url(self):
        return ('document_view', [self.id])


    def update_checksum(self, save=True):
        if self.exists():
            self.checksum = unicode(CHECKSUM_FUNCTION(self.file.read()))
            if save:
                self.save()

    
    def update_page_count(self, save=True):
        total_pages = PAGE_COUNT_FUNCTION(self)
        for page_number in range(total_pages):
            document_page, created = DocumentPage.objects.get_or_create(
                document=self, page_number=page_number+1)
        if save:
            self.save()

        
    def save_to_file(self, filepath, buffer_size=1024*1024):
        storage = self.file.storage.open(self.file.url)
        output_descriptor = open(filepath, 'wb')
        while 1:
            copy_buffer = storage.read()
            if copy_buffer:
                output_descriptor.write(copy_buffer)
            else:
                break
    
        #input_descriptor.close()
        output_descriptor.close()
        return filepath       
       
    
    def exists(self):
        return self.file.storage.exists(self.file.url)

        
    def delete(self, *args, **kwargs):
        #TODO: Might not execute when done in bulk from a queryset
        #topics/db/queries.html#topics-db-queries-delete
        self.delete_fs_links()
        super(Document, self).delete(*args, **kwargs)


    def get_metadata_groups(self):
        errors = []
        metadata_groups = {}
        if MetadataGroup.objects.all().count():
            metadata_dict = {}
            for document_metadata in self.documentmetadata_set.all():
                metadata_dict['metadata_%s' % document_metadata.metadata_type.name] = document_metadata.value
                
            for group in MetadataGroup.objects.filter((Q(document_type=self.document_type) | Q(document_type=None)) & Q(enabled=True)):
                total_query = Q()
                for item in group.metadatagroupitem_set.filter(enabled=True):
                    try:
                        value_query = Q(**{'value__%s' % item.operator: eval(item.expression, metadata_dict)})
                        if item.negated:
                            query = (Q(metadata_type__id=item.metadata_type.id) & ~value_query)
                        else:
                            query = (Q(metadata_type__id=item.metadata_type.id) & value_query)

                        if item.inclusion == INCLUSION_AND:
                            total_query &= query
                        elif item.inclusion == INCLUSION_OR:
                            total_query |= query
                    except Exception, e:
                        errors.append(e)
                        value_query = Q()
                        query = Q()

                if total_query:
                    document_id_list = DocumentMetadata.objects.filter(total_query).values_list('document', flat=True)
                else:
                    document_id_list = []
                metadata_groups[group] = Document.objects.filter(Q(id__in=document_id_list)) or []
        return metadata_groups, errors


    def apply_default_transformations(self):
        #Only apply default transformations on new documents
        if DEFAULT_TRANSFORMATIONS and not [page.documentpagetransformation_set.all() for page in self.documentpage_set.all()]:
            for transformation in DEFAULT_TRANSFORMATIONS:
                if 'name' in transformation:
                    for document_page in self.documentpage_set.all():
                        page_transformation = DocumentPageTransformation(
                            document_page=document_page,
                            order=0, 
                            transformation=transformation['name'])
                        if 'arguments' in transformation:
                            page_transformation.arguments = transformation['arguments']
                        
                        page_transformation.save()
 
    
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
        return self.title if self.title else self.name
        
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
    filename = models.CharField(max_length=128, verbose_name=_(u'filename'))
    enabled = models.BooleanField(default=True, verbose_name=_(u'enabled'))
    
    def __unicode__(self):
        return self.filename

    class Meta:
        ordering = ['filename']
        verbose_name = _(u'document type quick rename filename')
        verbose_name_plural = _(u'document types quick rename filenames')


class DocumentPage(models.Model):
    document = models.ForeignKey(Document, verbose_name=_(u'document'))
    content = models.TextField(blank=True, null=True, verbose_name=_(u'content'))
    page_label = models.CharField(max_length=32, blank=True, null=True, verbose_name=_(u'page label'))
    page_number = models.PositiveIntegerField(default=1, editable=False, verbose_name=_(u'page number'))
        
    def __unicode__(self):
        return '%s - %d - %s' % (unicode(self.document), self.page_number, self.page_label)

    class Meta:
        verbose_name = _(u'document page')
        verbose_name_plural = _(u'document pages')


class MetadataGroup(models.Model):
    document_type = models.ManyToManyField(DocumentType, null=True, blank=True,
        verbose_name=_(u'document type'), help_text=_(u'If left blank, all document types will be matched.'))
    name = models.CharField(max_length=32, verbose_name=_(u'name'))
    label = models.CharField(max_length=32, verbose_name=_(u'label'))
    enabled = models.BooleanField(default=True, verbose_name=_(u'enabled'))
    
    def __unicode__(self):
        return self.label if self.label else self.name

    class Meta:
        verbose_name = _(u'metadata document group')
        verbose_name_plural = _(u'metadata document groups')    


INCLUSION_AND = '&'
INCLUSION_OR = '|'

INCLUSION_CHOICES = (
    (INCLUSION_AND, _(u'and')),
    (INCLUSION_OR, _(u'or')),
)

OPERATOR_CHOICES = (
    ('exact', _(u'is equal')),
    ('iexact', _(u'is equal (case insensitive)')),
    ('contains', _(u'contains')),
    ('icontains', _(u'contains (case insensitive)')),
    ('in', _(u'is in')),
    ('gt', _(u'is greater than')),
    ('gte', _(u'is greater than or equal')),
    ('lt', _(u'is less than')),
    ('lte', _(u'is less than or equal')),
    ('startswith', _(u'starts with')),
    ('istartswith', _(u'starts with (case insensitive)')),
    ('endswith', _(u'ends with')),
    ('iendswith', _(u'ends with (case insensitive)')),
    ('regex', _(u'is in regular expression')),
    ('iregex', _(u'is in regular expression (case insensitive)')),
)
    
class MetadataGroupItem(models.Model):
    metadata_group = models.ForeignKey(MetadataGroup, verbose_name=_(u'metadata group'))
    inclusion = models.CharField(default=INCLUSION_AND, max_length=16, choices=INCLUSION_CHOICES, help_text=_(u'The inclusion is ignored for the first item.'))
    metadata_type = models.ForeignKey(MetadataType, verbose_name=_(u'metadata type'), help_text=_(u'This represents the metadata of all other documents.'))
    operator = models.CharField(max_length=16, choices=OPERATOR_CHOICES)
    expression = models.CharField(max_length=128,
        verbose_name=_(u'expression'), help_text=_(u'This expression will be evaluated against the current seleted document.  The document metadata is available as variables of the same name but with the "metadata_" prefix added their name.'))
    negated = models.BooleanField(default=False, verbose_name=_(u'negated'), help_text=_(u'Inverts the logic of the operator.'))
    enabled = models.BooleanField(default=True, verbose_name=_(u'enabled'))
    
    def __unicode__(self):
        return '[%s] %s %s %s %s %s' % ('x' if self.enabled else ' ', self.get_inclusion_display(), self.metadata_type, _(u'not') if self.negated else '', self.get_operator_display(), self.expression)

    class Meta:
        verbose_name = _(u'metadata group item')
        verbose_name_plural = _(u'metadata group items')


available_transformations = ([(name, data['label']) for name, data in AVAILABLE_TRANSFORMATIONS.items()]) if AVAILABLE_MODELS else []

    
class DocumentPageTransformation(models.Model):
    document_page = models.ForeignKey(DocumentPage, verbose_name=_(u'document page'))
    order = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name=_(u'order'))
    transformation = models.CharField(choices=available_transformations, max_length=128, verbose_name=_(u'transformation'))
    arguments = models.TextField(blank=True, null=True, verbose_name=_(u'arguments'), help_text=_(u'Use dictionaries to indentify arguments, example: {\'degrees\':90}'))

    def __unicode__(self):
        return '%s - %s' % (unicode(self.document_page), self.get_transformation_display())

    class Meta:
        ordering = ('order',)
        verbose_name = _(u'document page transformation')
        verbose_name_plural = _(u'document page transformations')
    
  
register(Document, _(u'document'), ['document_type__name', 'file_mimetype', 'file_filename', 'file_extension', 'documentmetadata__value', 'documentpage__content', 'description'])
