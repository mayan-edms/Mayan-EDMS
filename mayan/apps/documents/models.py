from __future__ import unicode_literals

from ast import literal_eval
import base64
import hashlib
import logging
import os
import tempfile
import uuid

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from acls.utils import apply_default_acls
from common.settings import TEMPORARY_DIRECTORY
from converter.classes import Converter
from converter.exceptions import UnknownFileFormat
from converter.literals import (
    DEFAULT_ZOOM_LEVEL, DEFAULT_ROTATION, DEFAULT_PAGE_NUMBER
)
from mimetype.api import get_mimetype

from .events import event_document_create
from .exceptions import NewDocumentVersionNotAllowed
from .managers import (
    DocumentManager, DocumentPageTransformationManager, DocumentTypeManager,
    RecentDocumentManager
)
from .runtime import storage_backend
from .settings import (
    CACHE_PATH, DISPLAY_SIZE, LANGUAGE, LANGUAGE_CHOICES, ZOOM_MAX_LEVEL,
    ZOOM_MIN_LEVEL
)
from .signals import post_version_upload, post_document_type_change

HASH_FUNCTION = lambda x: hashlib.sha256(x).hexdigest()  # document image cache name hash function
logger = logging.getLogger(__name__)


def UUID_FUNCTION(*args, **kwargs):
    return unicode(uuid.uuid4())


@python_2_unicode_compatible
class DocumentType(models.Model):
    """
    Define document types or classes to which a specific set of
    properties can be attached
    """
    name = models.CharField(max_length=32, verbose_name=_('Name'), unique=True)

    # TODO: find a way to move this to the ocr app
    ocr = models.BooleanField(default=True, verbose_name=_('Automatically queue newly created documents for OCR.'))

    objects = DocumentTypeManager()

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)

    class Meta:
        verbose_name = _('Document type')
        verbose_name_plural = _('Documents types')
        ordering = ['name']


@python_2_unicode_compatible
class Document(models.Model):
    """
    Defines a single document with it's fields and properties
    """

    uuid = models.CharField(default=UUID_FUNCTION(), max_length=48, editable=False)
    document_type = models.ForeignKey(DocumentType, verbose_name=_('Document type'), related_name='documents')
    label = models.CharField(max_length=255, default=_('Uninitialized document'), db_index=True, help_text=_('The name of the document'), verbose_name=_('Label'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))
    date_added = models.DateTimeField(verbose_name=_('Added'), auto_now_add=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, default=LANGUAGE, max_length=8, verbose_name=_('Language'))

    objects = DocumentManager()

    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')
        ordering = ['-date_added']

    def set_document_type(self, document_type, force=False):
        has_changed = self.document_type != document_type

        self.document_type = document_type
        self.save()
        if has_changed or force:
            post_document_type_change.send(sender=self.__class__, instance=self)

    @staticmethod
    def clear_image_cache():
        for the_file in os.listdir(CACHE_PATH):
            file_path = os.path.join(CACHE_PATH, the_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse('documents:document_preview', args=[self.pk])

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        new_document = not self.pk
        super(Document, self).save(*args, **kwargs)

        if new_document:
            apply_default_acls(self, user)

            if user:
                self.add_as_recent_document_for_user(user)
                event_document_create.commit(actor=user, target=self)
            else:
                event_document_create.commit(target=self)

    """
    def get_cached_image_name(self, page, version):
        document_version = DocumentVersion.objects.get(pk=version)
        document_page = document_version.pages.get(page_number=page)
        transformations, warnings = document_page.get_transformation_list()
        hash_value = HASH_FUNCTION(''.join([document_version.checksum, unicode(page), unicode(transformations)]))
        return os.path.join(CACHE_PATH, hash_value), transformations

    def get_image_cache_name(self, page, version):
        cache_file_path, transformations = self.get_cached_image_name(page, version)
        if os.path.exists(cache_file_path):
            return cache_file_path
        else:
            document_version = DocumentVersion.objects.get(pk=version)
            document_file = document_version.document.document_save_to_temp_dir(document_version.checksum)
            return convert(input_filepath=document_file, output_filepath=cache_file_path, page=page, transformations=transformations, mimetype=self.file_mimetype)

    def get_valid_image(self, size=DISPLAY_SIZE, page=DEFAULT_PAGE_NUMBER, zoom=DEFAULT_ZOOM_LEVEL, rotation=DEFAULT_ROTATION, version=None):
        if not version:
            version = self.latest_version.pk
        image_cache_name = self.get_image_cache_name(page=page, version=version)

        logger.debug('image_cache_name: %s', image_cache_name)

        return convert(input_filepath=image_cache_name, cleanup_files=False, size=size, zoom=zoom, rotation=rotation)

    def get_image(self, size=DISPLAY_SIZE, page=DEFAULT_PAGE_NUMBER, zoom=DEFAULT_ZOOM_LEVEL, rotation=DEFAULT_ROTATION, as_base64=False, version=None):
        if zoom < ZOOM_MIN_LEVEL:
            zoom = ZOOM_MIN_LEVEL

        if zoom > ZOOM_MAX_LEVEL:
            zoom = ZOOM_MAX_LEVEL

        rotation = rotation % 360

        file_path = self.get_valid_image(size=size, page=page, zoom=zoom, rotation=rotation, version=version)
        logger.debug('file_path: %s', file_path)

        if as_base64:
            with open(file_path, 'r') as file_object:
                mimetype = get_mimetype(file_object=file_object, mimetype_only=True)[0]
                base64_data = base64.b64encode(file_object.read())
                return 'data:%s;base64,%s' % (mimetype, base64_data)
        else:
            return file_path
    """

    def invalidate_cached_image(self, page):
        pass
        #try:
        #    os.unlink(self.get_cached_image_name(page, self.latest_version.pk)[0])
        #except OSError:
        #    pass

    def add_as_recent_document_for_user(self, user):
        RecentDocument.objects.add_document_for_user(user, self)

    def delete(self, *args, **kwargs):
        for version in self.versions.all():
            version.delete()
        return super(Document, self).delete(*args, **kwargs)

    @property
    def size(self):
        return self.latest_version.size

    def new_version(self, file_object, user=None, comment=None):
        logger.debug('creating new document version')
        # TODO: move this restriction to a signal processor of the checkouts app
        if not self.is_new_versions_allowed(user=user):
            raise NewDocumentVersionNotAllowed

        new_version = DocumentVersion.objects.create(
            document=self,
            file=file_object,
            comment=comment or '',
        )

        logger.debug('new_version saved')

        # TODO: new HISTORY for version updates

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

    # TODO: rename to file_encoding
    @property
    def file_mime_encoding(self):
        return self.latest_version.encoding

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
        try:
            return self.latest_version.pages
        except AttributeError:
            # Document has no version yet
            return 0

    @property
    def page_count(self):
        return self.latest_version.page_count

    @property
    def latest_version(self):
        return self.versions.order_by('timestamp').last()

    def document_save_to_temp_dir(self, filename, buffer_size=1024 * 1024):
        temporary_path = os.path.join(TEMPORARY_DIRECTORY, filename)
        return self.save_to_file(temporary_path, buffer_size)


@python_2_unicode_compatible
class DocumentVersion(models.Model):
    """
    Model that describes a document version and its properties
    """
    _pre_open_hooks = {}
    _post_save_hooks = {}

    @classmethod
    def register_pre_open_hook(cls, order, func):
        cls._pre_open_hooks[order] = func

    @classmethod
    def register_post_save_hook(cls, order, func):
        cls._post_save_hooks[order] = func

    document = models.ForeignKey(Document, verbose_name=_('Document'), related_name='versions')
    timestamp = models.DateTimeField(verbose_name=_('Timestamp'), auto_now_add=True)
    comment = models.TextField(blank=True, verbose_name=_('Comment'))

    # File related fields
    file = models.FileField(upload_to=UUID_FUNCTION(), storage=storage_backend, verbose_name=_('File'))
    mimetype = models.CharField(max_length=255, null=True, blank=True, editable=False)
    encoding = models.CharField(max_length=64, null=True, blank=True, editable=False)

    checksum = models.TextField(blank=True, null=True, verbose_name=_('Checksum'), editable=False)

    class Meta:
        verbose_name = _('Document version')
        verbose_name_plural = _('Document version')

    def __str__(self):
        return '{0} - {1}'.format(self.document, self.timestamp)

    def save(self, *args, **kwargs):
        """
        Overloaded save method that updates the document version's checksum,
        mimetype, page count and transformation when created
        """
        new_document_version = not self.pk

        # Only do this for new documents
        transformations = kwargs.pop('transformations', None)
        super(DocumentVersion, self).save(*args, **kwargs)

        for key in sorted(DocumentVersion._post_save_hooks):
            DocumentVersion._post_save_hooks[key](self)

        if new_document_version:
            # Only do this for new documents
            self.update_checksum(save=False)
            self.update_mimetype(save=False)
            self.save()
            self.update_page_count(save=False)

            if transformations:
                self.apply_default_transformations(transformations)

            post_version_upload.send(sender=self.__class__, instance=self)

    def update_checksum(self, save=True):
        """
        Open a document version's file and update the checksum field using the
        user provided checksum function
        """
        if self.exists():
            source = self.open()
            self.checksum = unicode(HASH_FUNCTION(source.read()))
            source.close()
            if save:
                self.save()

    def update_page_count(self, save=True):
        #handle, filepath = tempfile.mkstemp()
        # Just need the filepath, close the file description
        #os.close(handle)

        #self.save_to_file(filepath)
        try:
            with self.open() as file_object:
                converter = Converter(file_object=file_object, mimetype=self.mimetype)
                detected_pages = converter.get_page_count()
        except UnknownFileFormat:
            # If converter backend doesn't understand the format,
            # use 1 as the total page count
            detected_pages = 1
        #try:
        #    os.remove(filepath)
        #except OSError:
        #    pass

        # TODO: put inside a DB transaction
        self.pages.all().delete()

        for page_number in range(detected_pages):
            DocumentPage.objects.create(
                document_version=self, page_number=page_number + 1
            )

        # TODO: is this needed anymore
        if save:
            self.save()

        return detected_pages

    # TODO: remove from here and move to converter app
    def apply_default_transformations(self, transformations):
        # Only apply default transformations on new documents
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
                with self.open() as file_object:
                    self.mimetype, self.encoding = get_mimetype(file_object=file_object)
            except:
                self.mimetype = ''
                self.encoding = ''
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

    @property
    def page_count(self):
        return self.pages.count()


@python_2_unicode_compatible
class DocumentTypeFilename(models.Model):
    """
    List of filenames available to a specific document type for the
    quick rename functionality
    """
    document_type = models.ForeignKey(DocumentType, related_name='filenames', verbose_name=_('Document type'))
    filename = models.CharField(max_length=128, verbose_name=_('Filename'), db_index=True)
    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))

    def __str__(self):
        return self.filename

    class Meta:
        ordering = ['filename']
        unique_together = ('document_type', 'filename')
        verbose_name = _('Document type quick rename filename')
        verbose_name_plural = _('Document types quick rename filenames')


@python_2_unicode_compatible
class DocumentPage(models.Model):
    """
    Model that describes a document version page including it's content
    """
    document_version = models.ForeignKey(DocumentVersion, verbose_name=_('Document version'), related_name='pages')
    content = models.TextField(blank=True, null=True, verbose_name=_('Content'))
    page_label = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('Page label'))
    page_number = models.PositiveIntegerField(default=1, editable=False, verbose_name=_('Page number'), db_index=True)

    def __str__(self):
        return _('Page %(page_num)d out of %(total_pages)d of %(document)s') % {
            'document': unicode(self.document),
            'page_num': self.page_number,
            'total_pages': self.document_version.pages.count()
        }

    class Meta:
        ordering = ['page_number']
        verbose_name = _('Document page')
        verbose_name_plural = _('Document pages')

    def get_absolute_url(self):
        return reverse('documents:document_page_view', args=[self.pk])

    @property
    def siblings(self):
        return DocumentPage.objects.filter(document_version=self.document_version)

    # Compatibility methods
    @property
    def document(self):
        return self.document_version.document

    def get_image(self, *args, **kargs):
        #size=DISPLAY_SIZE, page=DEFAULT_PAGE_NUMBER, zoom=DEFAULT_ZOOM_LEVEL, rotation=DEFAULT_ROTATION, as_base64=False, version=None):
        #if zoom < ZOOM_MIN_LEVEL:
        #    zoom = ZOOM_MIN_LEVEL

        #if zoom > ZOOM_MAX_LEVEL:
        #    zoom = ZOOM_MAX_LEVEL

        #rotation = rotation % 360

        #file_path = self.get_valid_image(size=size, page=page, zoom=zoom, rotation=rotation, version=version)
        #logger.debug('file_path: %s', file_path)

        converter = Converter(file_object=self.document_version.open())
        data = converter.convert(page=self.page_number)
        #print "data!!!!", data.getvalue()
        ##, *args, **kwargs):
        return 'data:%s;base64,%s' % ('PNG', base64.b64encode(data.getvalue()))

        #if as_base64:
        #    with open(file_path, 'r') as file_object:
        #        #mimetype = get_mimetype(file_object=file_object, mimetype_only=True)[0]
        #        base64_data = base64.b64encode(file_object.read())
        #        return 'data:%s;base64,%s' % (mimetype, base64_data)
        #else:
        #    return file_path


def argument_validator(value):
    """
    Validates that the input evaluates correctly.
    """
    value = value.strip()
    try:
        literal_eval(value)
    except (ValueError, SyntaxError):
        raise ValidationError(_('Enter a valid value.'), code='invalid')


@python_2_unicode_compatible
class DocumentPageTransformation(models.Model):
    """
    Model that stores the transformation and transformation arguments
    for a given document page
    """
    document_page = models.ForeignKey(DocumentPage, verbose_name=_('Document page'))
    order = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name=_('Order'), db_index=True)
    #transformation = models.CharField(choices=get_available_transformations_choices(), max_length=128, verbose_name=_('Transformation'))
    transformation = models.CharField(max_length=128, verbose_name=_('Transformation'))
    arguments = models.TextField(blank=True, null=True, verbose_name=_('Arguments'), help_text=_('Use dictionaries to indentify arguments, example: {\'degrees\':90}'), validators=[argument_validator])
    objects = DocumentPageTransformationManager()

    def __str__(self):
        return self.get_transformation_display()

    class Meta:
        ordering = ('order',)
        verbose_name = _('Document page transformation')
        verbose_name_plural = _('Document page transformations')


@python_2_unicode_compatible
class RecentDocument(models.Model):
    """
    Keeps a list of the n most recent accessed or created document for
    a given user
    """
    user = models.ForeignKey(User, verbose_name=_('User'), editable=False)
    document = models.ForeignKey(Document, verbose_name=_('Document'), editable=False)
    datetime_accessed = models.DateTimeField(verbose_name=_('Accessed'), auto_now=True, db_index=True)

    objects = RecentDocumentManager()

    def __str__(self):
        return unicode(self.document)

    class Meta:
        ordering = ('-datetime_accessed',)
        verbose_name = _('Recent document')
        verbose_name_plural = _('Recent documents')
