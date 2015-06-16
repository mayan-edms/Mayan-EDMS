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
from django.db import models, transaction
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from acls.utils import apply_default_acls
from common.settings import TEMPORARY_DIRECTORY
from common.utils import fs_cleanup
from converter import (
    converter_class, TransformationResize, TransformationRotate, TransformationZoom
)
from converter.exceptions import UnknownFileFormat
from converter.literals import (
    DEFAULT_ZOOM_LEVEL, DEFAULT_ROTATION, DEFAULT_PAGE_NUMBER
)
from converter.models import Transformation
from mimetype.api import get_mimetype

from .events import event_document_create
from .exceptions import NewDocumentVersionNotAllowed
from .managers import (
    DocumentManager, DocumentTypeManager, RecentDocumentManager
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
        ordering = ('name',)


@python_2_unicode_compatible
class Document(models.Model):
    """
    Defines a single document with it's fields and properties
    """

    uuid = models.CharField(default=UUID_FUNCTION, max_length=48, editable=False)
    document_type = models.ForeignKey(DocumentType, verbose_name=_('Document type'), related_name='documents')
    label = models.CharField(max_length=255, default=_('Uninitialized document'), db_index=True, help_text=_('The name of the document'), verbose_name=_('Label'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))
    date_added = models.DateTimeField(verbose_name=_('Added'), auto_now_add=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, default=LANGUAGE, max_length=8, verbose_name=_('Language'))

    objects = DocumentManager()

    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')
        ordering = ('-date_added',)

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
    file = models.FileField(upload_to=UUID_FUNCTION, storage=storage_backend, verbose_name=_('File'))
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
        mimetype, and page count when created
        """
        new_document_version = not self.pk

        # Only do this for new documents
        super(DocumentVersion, self).save(*args, **kwargs)

        for key in sorted(DocumentVersion._post_save_hooks):
            DocumentVersion._post_save_hooks[key](self)

        if new_document_version:
            # Only do this for new documents
            self.update_checksum(save=False)
            self.update_mimetype(save=False)
            self.save()
            self.update_page_count(save=False)

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
        try:
            with self.open() as file_object:
                converter = converter_class(file_object=file_object, mime_type=self.mimetype)
                detected_pages = converter.get_page_count()
        except UnknownFileFormat:
            # If converter backend doesn't understand the format,
            # use 1 as the total page count
            detected_pages = 1

        with transaction.atomic():
            self.pages.all().delete()

            for page_number in range(detected_pages):
                DocumentPage.objects.create(
                    document_version=self, page_number=page_number + 1
                )

        # TODO: is this needed anymore
        if save:
            self.save()

        return detected_pages

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
        ordering = ('filename',)
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
        ordering = ('page_number',)
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

    def get_uuid(self):
        return 'page-cache-{}'.format(self.pk)

    def get_cache_filename(self):
        return os.path.join(CACHE_PATH, self.get_uuid())

    def get_image(self, *args, **kwargs):
        transformations = kwargs.pop('transformations', [])

        size = kwargs.pop('size', DISPLAY_SIZE)
        rotation = kwargs.pop('rotation', DEFAULT_ROTATION)
        zoom_level = kwargs.pop('zoom', DEFAULT_ZOOM_LEVEL)

        if zoom_level < ZOOM_MIN_LEVEL:
            zoom_level = ZOOM_MIN_LEVEL

        if zoom_level > ZOOM_MAX_LEVEL:
            zoom_level = ZOOM_MAX_LEVEL

        rotation = rotation % 360

        as_base64 = kwargs.pop('as_base64', False)

        cache_filename = self.get_cache_filename()

        if os.path.exists(cache_filename):
            converter = converter_class(file_object=open(cache_filename))

            converter.seek(0)
        else:
            try:
                converter = converter_class(file_object=self.document_version.open())
                converter.seek(page_number=self.page_number - 1)

                page_image = converter.get_page()
                with open(cache_filename, 'wb+') as file_object:
                    file_object.write(page_image.getvalue())
            except:
                fs_cleanup(cache_filename)
                raise

        # Stored transformations
        for stored_transformation in Transformation.objects.get_for_model(self, as_classes=True):
            converter.transform(transformation=stored_transformation)

        # Interactive transformations
        for transformation in transformations:
            converter.transform(transformation=transformation)

        if rotation:
            converter.transform(transformation=TransformationRotate(degrees=rotation))

        if size:
            converter.transform(transformation=TransformationResize(**dict(zip(('width', 'height'), (size.split('x'))))))

        if zoom_level:
            converter.transform(transformation=TransformationZoom(percent=zoom_level))

        page_image = converter.get_page()

        if as_base64:
            return 'data:%s;base64,%s' % ('image/png', base64.b64encode(page_image.getvalue()))
        else:
            return page_image


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
