import os
import tempfile

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment

from taggit.managers import TaggableManager
from dynamic_search.api import register
from converter.api import get_page_count
from converter import TRANFORMATION_CHOICES

from documents.utils import get_document_mimetype
from documents.conf.settings import CHECKSUM_FUNCTION
from documents.conf.settings import UUID_FUNCTION
from documents.conf.settings import STORAGE_BACKEND
from documents.conf.settings import AVAILABLE_TRANSFORMATIONS
from documents.conf.settings import DEFAULT_TRANSFORMATIONS
from documents.managers import RecentDocumentManager

available_transformations = ([(name, data['label']) for name, data in AVAILABLE_TRANSFORMATIONS.items()])


def get_filename_from_uuid(instance, filename):
    """
    Store the orignal filename of the uploaded file and replace it with
    a UUID
    """
    filename, extension = os.path.splitext(filename)
    instance.file_filename = filename
    #remove prefix '.'
    instance.file_extension = extension[1:]
    uuid = UUID_FUNCTION()
    instance.uuid = uuid
    return uuid


class DocumentType(models.Model):
    """
    Define document types or classes to which a specific set of
    properties can be attached
    """
    name = models.CharField(max_length=32, verbose_name=_(u'name'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u'document type')
        verbose_name_plural = _(u'documents types')
        ordering = ['name']        


class Document(models.Model):
    """
    Defines a single document with it's fields and properties
    """
    document_type = models.ForeignKey(DocumentType, verbose_name=_(u'document type'), null=True, blank=True)
    file = models.FileField(upload_to=get_filename_from_uuid, storage=STORAGE_BACKEND(), verbose_name=_(u'file'))
    uuid = models.CharField(max_length=48, default=UUID_FUNCTION(), blank=True, editable=False)
    file_mimetype = models.CharField(max_length=64, default='', editable=False)
    file_mime_encoding = models.CharField(max_length=64, default='', editable=False)
    #FAT filename can be up to 255 using LFN
    file_filename = models.CharField(max_length=255, default=u'', editable=False, db_index=True)
    file_extension = models.CharField(max_length=16, default=u'', editable=False, db_index=True)
    date_added = models.DateTimeField(verbose_name=_(u'added'), auto_now_add=True, db_index=True)
    date_updated = models.DateTimeField(verbose_name=_(u'updated'), auto_now=True)
    checksum = models.TextField(blank=True, null=True, verbose_name=_(u'checksum'), editable=False)
    description = models.TextField(blank=True, null=True, verbose_name=_(u'description'), db_index=True)

    tags = TaggableManager()
    
    comments = generic.GenericRelation(
        Comment,
        content_type_field='content_type',
        object_id_field='object_pk'
    )

    class Meta:
        verbose_name = _(u'document')
        verbose_name_plural = _(u'documents')
        ordering = ['-date_added']

    def __unicode__(self):
        return os.extsep.join([self.file_filename, self.file_extension])

    def save(self, *args, **kwargs):
        """
        Overloaded save method that updates the document's checksum,
        mimetype, page count and transformation when originally created
        """
        new_document = not self.pk

        super(Document, self).save(*args, **kwargs)

        if new_document:
            #Only do this for new documents
            self.update_checksum(save=False)
            self.update_mimetype(save=False)
            self.save()
            self.update_page_count(save=False)
            self.apply_default_transformations()

    @models.permalink
    def get_absolute_url(self):
        return ('document_view_simple', [self.pk])

    def get_fullname(self):
        """
        Return the fullname of the document's file
        """
        return os.extsep.join([self.file_filename, self.file_extension])

    def update_mimetype(self, save=True):
        """
        Read a document's file and determine the mimetype by calling the
        get_mimetype wrapper
        """
        if self.exists():
            try:
                self.file_mimetype, self.mime_encoding = get_document_mimetype(self)
            except:
                self.file_mimetype = u''
                self.file_mime_encoding = u''
            finally:
                if save:
                    self.save()

    def open(self):
        """
        Return a file descriptor to a document's file irrespective of
        the storage backend
        """
        return self.file.storage.open(self.file.path)

    def update_checksum(self, save=True):
        """
        Open a document's file and update the checksum field using the
        user provided checksum function
        """
        if self.exists():
            source = self.open()
            self.checksum = unicode(CHECKSUM_FUNCTION(source.read()))
            source.close()
            if save:
                self.save()

    def update_page_count(self, save=True):
        handle, filepath = tempfile.mkstemp()
        self.save_to_file(filepath)
        detected_pages = get_page_count(filepath)
        os.close(handle)
        try:
            os.remove(filepath)
        except OSError:
            pass

        current_pages = DocumentPage.objects.filter(document=self).order_by('page_number',)
        if current_pages.count() > detected_pages:
            for page in current_pages[detected_pages:]:
                page.delete()

        for page_number in range(detected_pages):
            DocumentPage.objects.get_or_create(
                document=self, page_number=page_number + 1)

        if save:
            self.save()

        return detected_pages

    def save_to_file(self, filepath, buffer_size=1024 * 1024):
        """
        Save a copy of the document from the document storage backend
        to the local filesystem
        """
        input_descriptor = self.open()
        output_descriptor = open(filepath, 'wb')
        while True:
            copy_buffer = input_descriptor.read(buffer_size)
            if copy_buffer:
                output_descriptor.write(copy_buffer)
            else:
                break

        output_descriptor.close()
        input_descriptor.close()
        return filepath

    def exists(self):
        """
        Returns a boolean value that indicates if the document's file
        exists in storage
        """
        return self.file.storage.exists(self.file.path)

    def apply_default_transformations(self):
        #Only apply default transformations on new documents
        if DEFAULT_TRANSFORMATIONS and reduce(lambda x, y: x + y, [page.documentpagetransformation_set.count() for page in self.documentpage_set.all()]) == 0:
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


class DocumentTypeFilename(models.Model):
    """
    List of filenames available to a specific document type for the
    quick rename functionality
    """
    document_type = models.ForeignKey(DocumentType, verbose_name=_(u'document type'))
    filename = models.CharField(max_length=128, verbose_name=_(u'filename'), db_index=True)
    enabled = models.BooleanField(default=True, verbose_name=_(u'enabled'))

    def __unicode__(self):
        return self.filename

    class Meta:
        ordering = ['filename']
        verbose_name = _(u'document type quick rename filename')
        verbose_name_plural = _(u'document types quick rename filenames')


class DocumentPage(models.Model):
    """
    Model that describes a document page including it's content
    """
    document = models.ForeignKey(Document, verbose_name=_(u'document'))
    content = models.TextField(blank=True, null=True, verbose_name=_(u'content'), db_index=True)
    page_label = models.CharField(max_length=32, blank=True, null=True, verbose_name=_(u'page label'))
    page_number = models.PositiveIntegerField(default=1, editable=False, verbose_name=_(u'page number'), db_index=True)

    def __unicode__(self):
        return _(u'Page %(page_num)d out of %(total_pages)d of %(document)s') % {
            'document': unicode(self.document),
            'page_num': self.page_number,
            'total_pages': self.document.documentpage_set.count()
        }

    class Meta:
        ordering = ['page_number']
        verbose_name = _(u'document page')
        verbose_name_plural = _(u'document pages')

    @models.permalink
    def get_absolute_url(self):
        return ('document_page_view', [self.pk])

    def get_transformation_string(self):
        transformation_list = []
        warnings = []
        for page_transformation in self.documentpagetransformation_set.all():
            try:
                if page_transformation.transformation in TRANFORMATION_CHOICES:
                    transformation_list.append(
                        TRANFORMATION_CHOICES[page_transformation.transformation] % eval(
                            page_transformation.arguments
                        )
                    )
            except Exception, e:
                warnings.append(e)

        return u' '.join(transformation_list), warnings


class DocumentPageTransformation(models.Model):
    """
    Model that stores the transformation and transformation arguments
    for a given document page
    """
    document_page = models.ForeignKey(DocumentPage, verbose_name=_(u'document page'))
    order = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name=_(u'order'), db_index=True)
    transformation = models.CharField(choices=available_transformations, max_length=128, verbose_name=_(u'transformation'))
    arguments = models.TextField(blank=True, null=True, verbose_name=_(u'arguments'), help_text=_(u'Use dictionaries to indentify arguments, example: {\'degrees\':90}'))

    def __unicode__(self):
        return u'"%s" for %s' % (self.get_transformation_display(), unicode(self.document_page))

    class Meta:
        ordering = ('order',)
        verbose_name = _(u'document page transformation')
        verbose_name_plural = _(u'document page transformations')


class RecentDocument(models.Model):
    """
    Keeps a list of the n most recent accessed or created document for
    a given user
    """
    user = models.ForeignKey(User, verbose_name=_(u'user'), editable=False)
    document = models.ForeignKey(Document, verbose_name=_(u'document'), editable=False)
    datetime_accessed = models.DateTimeField(verbose_name=_(u'accessed'), db_index=True)

    objects = RecentDocumentManager()

    def __unicode__(self):
        return unicode(self.document)

    class Meta:
        ordering = ('-datetime_accessed',)
        verbose_name = _(u'recent document')
        verbose_name_plural = _(u'recent documents')


# Register the fields that will be searchable
register('document', Document, _(u'document'), [
    {'name': u'document_type__name', 'title': _(u'Document type')},
    {'name': u'file_mimetype', 'title': _(u'MIME type')},
    {'name': u'file_filename', 'title': _(u'Filename')},
    {'name': u'file_extension', 'title': _(u'Filename extension')},
    {'name': u'documentmetadata__value', 'title': _(u'Metadata value')},
    {'name': u'documentpage__content', 'title': _(u'Content')},
    {'name': u'description', 'title': _(u'Description')},
    {'name': u'tags__name', 'title': _(u'Tags')},
    {'name': u'comments__comment', 'title': _(u'Comments')},
    ]
)
#register(Document, _(u'document'), ['document_type__name', 'file_mimetype', 'file_extension', 'documentmetadata__value', 'documentpage__content', 'description', {'field_name':'file_filename', 'comparison':'iexact'}])
