from __future__ import absolute_import

import os
import tempfile
import hashlib
from ast import literal_eval
import base64
import datetime
import logging

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from dynamic_search.api import register
from converter.api import get_page_count
from converter.api import get_available_transformations_choices
from converter.api import convert
from converter.exceptions import UnknownFileFormat, UnkownConvertError
from mimetype.api import (get_mimetype, get_icon_file_path,
    get_error_icon_file_path)
from converter.literals import (DEFAULT_ZOOM_LEVEL, DEFAULT_ROTATION,
    DEFAULT_PAGE_NUMBER)

from .conf.settings import RECENT_COUNT
from .conf.settings import (CHECKSUM_FUNCTION, UUID_FUNCTION,
    STORAGE_BACKEND, DISPLAY_SIZE, CACHE_PATH,
    ZOOM_MAX_LEVEL, ZOOM_MIN_LEVEL)
from .managers import DocumentPageTransformationManager
from .utils import document_save_to_temp_dir
from .literals import (RELEASE_LEVEL_FINAL, RELEASE_LEVEL_CHOICES,
    VERSION_UPDATE_MAJOR, VERSION_UPDATE_MINOR, VERSION_UPDATE_MICRO)
from .exceptions import NewDocumentVersionNotAllowed

# document image cache name hash function
HASH_FUNCTION = lambda x: hashlib.sha256(x).hexdigest()

logger = logging.getLogger(__name__)


def get_filename_from_uuid(instance, filename):
    """
    Store the orignal filename of the uploaded file and replace it with
    a UUID
    """
    instance.filename = filename
    return UUID_FUNCTION()


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
    uuid = models.CharField(max_length=48, blank=True, editable=False)
    document_type = models.ForeignKey(DocumentType, verbose_name=_(u'document type'), null=True, blank=True)
    description = models.TextField(blank=True, null=True, verbose_name=_(u'description'))
    date_added = models.DateTimeField(verbose_name=_(u'added'), db_index=True, editable=False)

    @staticmethod
    def clear_image_cache():
        for the_file in os.listdir(CACHE_PATH):
            file_path = os.path.join(CACHE_PATH, the_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    class Meta:
        verbose_name = _(u'document')
        verbose_name_plural = _(u'documents')
        ordering = ['-date_added']

    def __unicode__(self):
        return self.latest_version.filename

    @models.permalink
    def get_absolute_url(self):
        return ('document_view_simple', [self.pk])

    def save(self, *args, **kwargs):
        if not self.pk:
            self.uuid = UUID_FUNCTION()
            self.date_added = datetime.datetime.now()
        super(Document, self).save(*args, **kwargs)

    def get_cached_image_name(self, page, version):
        document_version = DocumentVersion.objects.get(pk=version)
        document_page = document_version.documentpage_set.get(page_number=page)
        transformations, warnings = document_page.get_transformation_list()
        hash_value = HASH_FUNCTION(u''.join([document_version.checksum, unicode(page), unicode(transformations)]))
        return os.path.join(CACHE_PATH, hash_value), transformations

    def get_image_cache_name(self, page, version):
        cache_file_path, transformations = self.get_cached_image_name(page, version)
        if os.path.exists(cache_file_path):
            return cache_file_path
        else:
            document_version = DocumentVersion.objects.get(pk=version)
            document_file = document_save_to_temp_dir(document_version, document_version.checksum)
            return convert(document_file, output_filepath=cache_file_path, page=page, transformations=transformations, mimetype=self.file_mimetype)

    def get_valid_image(self, size=DISPLAY_SIZE, page=DEFAULT_PAGE_NUMBER, zoom=DEFAULT_ZOOM_LEVEL, rotation=DEFAULT_ROTATION, version=None):
        if not version:
            version = self.latest_version.pk
        image_cache_name = self.get_image_cache_name(page=page, version=version)
        return convert(image_cache_name, cleanup_files=False, size=size, zoom=zoom, rotation=rotation)

    def get_image(self, size=DISPLAY_SIZE, page=DEFAULT_PAGE_NUMBER, zoom=DEFAULT_ZOOM_LEVEL, rotation=DEFAULT_ROTATION, as_base64=False, version=None):
        if zoom < ZOOM_MIN_LEVEL:
            zoom = ZOOM_MIN_LEVEL

        if zoom > ZOOM_MAX_LEVEL:
            zoom = ZOOM_MAX_LEVEL

        rotation = rotation % 360

        try:
            file_path = self.get_valid_image(size=size, page=page, zoom=zoom, rotation=rotation, version=version)
        except UnknownFileFormat:
            file_path = get_icon_file_path(self.file_mimetype)
        except UnkownConvertError:
            file_path = get_error_icon_file_path()
        except:
            file_path = get_error_icon_file_path()

        if as_base64:
            image = open(file_path, 'r')
            out = StringIO()
            base64.encode(image, out)
            return u'data:%s;base64,%s' % (get_mimetype(open(file_path, 'r'), file_path, mimetype_only=True)[0], out.getvalue().replace('\n', ''))
        else:
            return file_path

    def invalidate_cached_image(self, page):
        try:
            os.unlink(self.get_cached_image_name(page, self.latest_version.pk)[0])
        except OSError:
            pass

    def add_as_recent_document_for_user(self, user):
        RecentDocument.objects.add_document_for_user(user, self)

    def delete(self, *args, **kwargs):
        for version in self.versions.all():
            version.delete()
        return super(Document, self).delete(*args, **kwargs)

    @property
    def size(self):
        return self.latest_version.size

    def new_version(self, file, user=None, comment=None, version_update=None, release_level=None, serial=None):
        logger.debug('creating new document version')
        if not self.is_new_versions_allowed(user=user):
            raise NewDocumentVersionNotAllowed

        if version_update:
            new_version_dict = self.latest_version.get_new_version_dict(version_update)
            logger.debug('new_version_dict: %s' % new_version_dict)
            new_version = DocumentVersion(
                document=self,
                file=file,
                major=new_version_dict.get('major'),
                minor=new_version_dict.get('minor'),
                micro=new_version_dict.get('micro'),
                release_level=release_level,
                serial=serial,
                comment=comment,
            )
            new_version.save()
        else:
            new_version_dict = {}
            new_version = DocumentVersion(
                document=self,
                file=file,
            )
            new_version.save()

        logger.debug('new_version saved')
        return new_version

    # Proxy methods
    def open(self, *args, **kwargs):
        """
        Return a file descriptor to a document's file irrespective of
        the storage backend
        """
        return self.latest_version.open(*args, **kwargs)

    def save_to_file(self, *args, **kwargs):
        return self.latest_version.save_to_file(*args, **kwargs)

    def exists(self):
        """
        Returns a boolean value that indicates if the document's
        latest version file exists in storage
        """
        return self.latest_version.exists()

    # Compatibility methods
    @property
    def file(self):
        return self.latest_version.file

    @property
    def file_mimetype(self):
        return self.latest_version.mimetype

    @property
    def file_mime_encoding(self):
        return self.latest_version.encoding

    @property
    def file_filename(self):
        return self.latest_version.filename

    @property
    def date_updated(self):
        return self.latest_version.timestamp

    @property
    def checksum(self):
        return self.latest_version.checksum

    @property
    def signature_state(self):
        return self.latest_version.signature_state

    @property
    def pages(self):
        return self.latest_version.pages

    @property
    def page_count(self):
        return self.pages.count()

    @property
    def latest_version(self):
        return self.documentversion_set.order_by('-timestamp')[0]

    @property
    def first_version(self):
        return self.documentversion_set.order_by('timestamp')[0]

    @property
    def versions(self):
        return self.documentversion_set

    def rename(self, new_name):
        version = self.latest_version
        return version.rename(new_name)

    def _get_filename(self):
        return self.latest_version.filename

    def _set_filename(self, value):
        version = self.latest_version
        version.filename = value
        return version.save()

    filename = property(_get_filename, _set_filename)


class DocumentVersion(models.Model):
    """
    Model that describes a document version and its properties
    """
    _pre_open_hooks = {}
    _post_save_hooks = {}

    @staticmethod
    def get_version_update_choices(document_version):
        return (
            (VERSION_UPDATE_MAJOR, _(u'Major %(major)i.%(minor)i, (new release)') % document_version.get_new_version_dict(VERSION_UPDATE_MAJOR)),
            (VERSION_UPDATE_MINOR, _(u'Minor %(major)i.%(minor)i, (some updates)') % document_version.get_new_version_dict(VERSION_UPDATE_MINOR)),
            (VERSION_UPDATE_MICRO, _(u'Micro %(major)i.%(minor)i.%(micro)i, (fixes)') % document_version.get_new_version_dict(VERSION_UPDATE_MICRO))
        )

    @classmethod
    def register_pre_open_hook(cls, order, func):
        cls._pre_open_hooks[order] = func

    @classmethod
    def register_post_save_hook(cls, order, func):
        cls._post_save_hooks[order] = func

    document = models.ForeignKey(Document, verbose_name=_(u'document'), editable=False)
    major = models.PositiveIntegerField(verbose_name=_(u'mayor'), default=1, editable=False)
    minor = models.PositiveIntegerField(verbose_name=_(u'minor'), default=0, editable=False)
    micro = models.PositiveIntegerField(verbose_name=_(u'micro'), default=0, editable=False)
    release_level = models.PositiveIntegerField(choices=RELEASE_LEVEL_CHOICES, default=RELEASE_LEVEL_FINAL, verbose_name=_(u'release level'), editable=False)
    serial = models.PositiveIntegerField(verbose_name=_(u'serial'), default=0, editable=False)
    timestamp = models.DateTimeField(verbose_name=_(u'timestamp'), editable=False)
    comment = models.TextField(blank=True, verbose_name=_(u'comment'))

    # File related fields
    file = models.FileField(upload_to=get_filename_from_uuid, storage=STORAGE_BACKEND(), verbose_name=_(u'file'))
    mimetype = models.CharField(max_length=64, null=True, blank=True, editable=False)
    encoding = models.CharField(max_length=64, null=True, blank=True, editable=False)
    filename = models.CharField(max_length=255, default=u'', editable=False, db_index=True)
    checksum = models.TextField(blank=True, null=True, verbose_name=_(u'checksum'), editable=False)

    class Meta:
        unique_together = ('document', 'major', 'minor', 'micro', 'release_level', 'serial')
        verbose_name = _(u'document version')
        verbose_name_plural = _(u'document version')

    def __unicode__(self):
        return self.get_formated_version()

    def get_new_version_dict(self, version_update_type):
        logger.debug('version_update_type: %s' % version_update_type)

        if version_update_type == VERSION_UPDATE_MAJOR:
            return {
                'major': self.major + 1,
                'minor': 0,
                'micro': 0,
            }
        elif version_update_type == VERSION_UPDATE_MINOR:
            return {
                'major': self.major,
                'minor': self.minor + 1,
                'micro': 0,
            }
        elif version_update_type == VERSION_UPDATE_MICRO:
            return {
                'major': self.major,
                'minor': self.minor,
                'micro': self.micro + 1,
            }

    def get_formated_version(self):
        """
        Return the formatted version information
        """
        vers = [u'%i.%i' % (self.major, self.minor), ]

        if self.micro:
            vers.append(u'.%i' % self.micro)
        if self.release_level != RELEASE_LEVEL_FINAL:
            vers.append(u'%s%i' % (self.get_release_level_display(), self.serial))
        return u''.join(vers)

    @property
    def pages(self):
        return self.documentpage_set

    def save(self, *args, **kwargs):
        """
        Overloaded save method that updates the document version's checksum,
        mimetype, page count and transformation when created
        """
        new_document = not self.pk
        if not self.pk:
            self.timestamp = datetime.datetime.now()

        #Only do this for new documents
        transformations = kwargs.pop('transformations', None)
        super(DocumentVersion, self).save(*args, **kwargs)

        for key in sorted(DocumentVersion._post_save_hooks):
            DocumentVersion._post_save_hooks[key](self)

        if new_document:
            #Only do this for new documents
            self.update_checksum(save=False)
            self.update_mimetype(save=False)
            self.save()
            self.update_page_count(save=False)
            if transformations:
                self.apply_default_transformations(transformations)

    def update_checksum(self, save=True):
        """
        Open a document version's file and update the checksum field using the
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
        # Just need the filepath, close the file description
        os.close(handle)

        self.save_to_file(filepath)
        try:
            detected_pages = get_page_count(filepath)
        except UnknownFileFormat:
            # If converter backend doesn't understand the format,
            # use 1 as the total page count
            detected_pages = 1
            self.description = ugettext(u'This document\'s file format is not known, the page count has therefore defaulted to 1.')
            self.save()
        try:
            os.remove(filepath)
        except OSError:
            pass

        current_pages = self.documentpage_set.order_by('page_number',)
        if current_pages.count() > detected_pages:
            for page in current_pages[detected_pages:]:
                page.delete()

        for page_number in range(detected_pages):
            DocumentPage.objects.get_or_create(
                document_version=self, page_number=page_number + 1)

        if save:
            self.save()

        return detected_pages

    def apply_default_transformations(self, transformations):
        #Only apply default transformations on new documents
        if reduce(lambda x, y: x + y, [page.documentpagetransformation_set.count() for page in self.pages.all()]) == 0:
            for transformation in transformations:
                for document_page in self.pages.all():
                    page_transformation = DocumentPageTransformation(
                        document_page=document_page,
                        order=0,
                        transformation=transformation.get('transformation'),
                        arguments=transformation.get('arguments')
                    )

                    page_transformation.save()

    def revert(self):
        """
        Delete the subsequent versions after this one
        """
        for version in self.document.versions.filter(timestamp__gt=self.timestamp):
            version.delete()

    def update_mimetype(self, save=True):
        """
        Read a document verions's file and determine the mimetype by calling the
        get_mimetype wrapper
        """
        if self.exists():
            try:
                self.mimetype, self.encoding = get_mimetype(self.open(), self.filename)
            except:
                self.mimetype = u''
                self.encoding = u''
            finally:
                if save:
                    self.save()

    def delete(self, *args, **kwargs):
        self.file.storage.delete(self.file.path)
        return super(DocumentVersion, self).delete(*args, **kwargs)

    def exists(self):
        """
        Returns a boolean value that indicates if the document's file
        exists in storage
        """
        return self.file.storage.exists(self.file.path)

    def open(self, raw=False):
        """
        Return a file descriptor to a document version's file irrespective of
        the storage backend
        """
        if raw:
            return self.file.storage.open(self.file.path)
        else:
            result = self.file.storage.open(self.file.path)
            for key in sorted(DocumentVersion._pre_open_hooks):
                result = DocumentVersion._pre_open_hooks[key](result, self)

            return result

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

    @property
    def size(self):
        if self.exists():
            return self.file.storage.size(self.file.path)
        else:
            return None
            
    def rename(self, new_name):
        new_filename, new_extension = os.path.splitext(new_name)
        name, extension = os.path.splitext(self.filename)
        
        # Preserve existing extension if new name doesn't has one
        if new_extension:
            extension = new_extension

        self.filename = u''.join([new_filename, extension])
        self.save()


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
    Model that describes a document version page including it's content
    """
    document_version = models.ForeignKey(DocumentVersion, verbose_name=_(u'document version'))
    content = models.TextField(blank=True, null=True, verbose_name=_(u'content'))
    page_label = models.CharField(max_length=32, blank=True, null=True, verbose_name=_(u'page label'))
    page_number = models.PositiveIntegerField(default=1, editable=False, verbose_name=_(u'page number'), db_index=True)

    def __unicode__(self):
        return _(u'Page %(page_num)d out of %(total_pages)d of %(document)s') % {
            'document': unicode(self.document),
            'page_num': self.page_number,
            'total_pages': self.document_version.documentpage_set.count()
        }

    class Meta:
        ordering = ['page_number']
        verbose_name = _(u'document page')
        verbose_name_plural = _(u'document pages')

    def get_transformation_list(self):
        return DocumentPageTransformation.objects.get_for_document_page_as_list(self)

    @models.permalink
    def get_absolute_url(self):
        return ('document_page_view', [self.pk])

    @property
    def siblings(self):
        return DocumentPage.objects.filter(document_version=self.document_version)

    # Compatibility methods
    @property
    def document(self):
        return self.document_version.document


class ArgumentsValidator(object):
    message = _(u'Enter a valid value.')
    code = 'invalid'

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        """
        Validates that the input evaluates correctly.
        """
        value = value.strip()
        try:
            literal_eval(value)
        except (ValueError, SyntaxError):
            raise ValidationError(self.message, code=self.code)


class DocumentPageTransformation(models.Model):
    """
    Model that stores the transformation and transformation arguments
    for a given document page
    """
    document_page = models.ForeignKey(DocumentPage, verbose_name=_(u'document page'))
    order = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name=_(u'order'), db_index=True)
    transformation = models.CharField(choices=get_available_transformations_choices(), max_length=128, verbose_name=_(u'transformation'))
    arguments = models.TextField(blank=True, null=True, verbose_name=_(u'arguments'), help_text=_(u'Use dictionaries to indentify arguments, example: %s') % u'{\'degrees\':90}', validators=[ArgumentsValidator()])
    objects = DocumentPageTransformationManager()

    def __unicode__(self):
        return self.get_transformation_display()

    class Meta:
        ordering = ('order',)
        verbose_name = _(u'document page transformation')
        verbose_name_plural = _(u'document page transformations')


class RecentDocumentManager(models.Manager):
    def add_document_for_user(self, user, document):
        if user.is_authenticated():
            self.model.objects.filter(user=user, document=document).delete()
            new_recent = self.model(user=user, document=document, datetime_accessed=datetime.datetime.now())
            new_recent.save()
            to_delete = self.model.objects.filter(user=user)[RECENT_COUNT:]
            for recent_to_delete in to_delete:
                recent_to_delete.delete()

    def get_for_user(self, user):
        if user.is_authenticated():
            return Document.objects.filter(recentdocument__user=user)
        else:
            return []


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
    {'name': u'documentversion__mimetype', 'title': _(u'MIME type')},
    {'name': u'documentversion__filename', 'title': _(u'Filename')},
    {'name': u'documentmetadata__value', 'title': _(u'Metadata value')},
    {'name': u'documentversion__documentpage__content', 'title': _(u'Content')},
    {'name': u'description', 'title': _(u'Description')},
    {'name': u'tags__name', 'title': _(u'Tags')},
    {'name': u'comments__comment', 'title': _(u'Comments')},
    ]
)
#register(Document, _(u'document'), ['document_type__name', 'file_mimetype', 'documentmetadata__value', 'documentpage__content', 'description', {'field_name':'file_filename', 'comparison':'iexact'}])
