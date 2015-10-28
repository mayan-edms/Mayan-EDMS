from __future__ import absolute_import, unicode_literals

import base64
import hashlib
import logging
import uuid

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.files import File
from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext, ugettext_lazy as _

from acls.models import AccessControlList
from common.literals import TIME_DELTA_UNIT_CHOICES
from converter import (
    converter_class, TransformationResize, TransformationRotate,
    TransformationZoom
)
from converter.exceptions import InvalidOfficeFormat, PageCountError
from converter.literals import DEFAULT_ZOOM_LEVEL, DEFAULT_ROTATION
from converter.models import Transformation
from mimetype.api import get_mimetype
from permissions import Permission

from .events import (
    event_document_create, event_document_new_version,
    event_document_properties_edit, event_document_type_change,
    event_document_version_revert
)
from .exceptions import NewDocumentVersionNotAllowed
from .literals import DEFAULT_DELETE_PERIOD, DEFAULT_DELETE_TIME_UNIT
from .managers import (
    DocumentManager, DocumentTypeManager, NewVersionBlockManager,
    PassthroughManager, RecentDocumentManager, TrashCanManager
)
from .permissions import permission_document_view
from .runtime import cache_storage_backend, storage_backend
from .settings import (
    setting_display_size, setting_language, setting_language_choices,
    setting_zoom_max_level, setting_zoom_min_level
)
from .signals import (
    post_document_created, post_document_type_change, post_version_upload
)

# document image cache name hash function
HASH_FUNCTION = lambda x: hashlib.sha256(x).hexdigest()
logger = logging.getLogger(__name__)


def UUID_FUNCTION(*args, **kwargs):
    return unicode(uuid.uuid4())


@python_2_unicode_compatible
class DocumentType(models.Model):
    """
    Define document types or classes to which a specific set of
    properties can be attached
    """
    label = models.CharField(
        max_length=32, unique=True, verbose_name=_('Label')
    )
    trash_time_period = models.PositiveIntegerField(
        blank=True, help_text=_(
            'Amount of time after which documents of this type will be '
            'moved to the trash.'
        ), null=True, verbose_name=_('Trash time period')
    )
    trash_time_unit = models.CharField(
        blank=True, choices=TIME_DELTA_UNIT_CHOICES, null=True, max_length=8,
        verbose_name=_('Trash time unit')
    )
    delete_time_period = models.PositiveIntegerField(
        default=DEFAULT_DELETE_PERIOD, help_text=_(
            'Amount of time after which documents of this type in the trash '
            'will be deleted.'
        ), verbose_name=_('Delete time period')
    )
    delete_time_unit = models.CharField(
        choices=TIME_DELTA_UNIT_CHOICES, default=DEFAULT_DELETE_TIME_UNIT,
        max_length=8, verbose_name=_('Delete time unit')
    )

    objects = DocumentTypeManager()

    def __str__(self):
        return self.label

    def delete(self, *args, **kwargs):
        for document in Document.passthrough.filter(document_type=self):
            document.delete(to_trash=False)

        return super(DocumentType, self).delete(*args, **kwargs)

    def natural_key(self):
        return (self.label,)

    class Meta:
        ordering = ('label',)
        verbose_name = _('Document type')
        verbose_name_plural = _('Documents types')

    @property
    def deleted_documents(self):
        return DeletedDocument.objects.filter(document_type=self)

    def get_document_count(self, user):
        queryset = self.documents

        try:
            Permission.check_permissions(user, (permission_document_view,))
        except PermissionDenied:
            queryset = AccessControlList.objects.filter_by_access(
                permission_document_view, user, queryset
            )

        return queryset.count()

    def new_document(self, file_object, label=None, description=None, language=None, _user=None):
        try:
            with transaction.atomic():
                document = self.documents.create(
                    description=description or '',
                    label=label or unicode(file_object),
                    language=language or setting_language.value
                )
                document.save(_user=_user)

                document.new_version(file_object=file_object, _user=_user)
                return document
        except Exception as exception:
            logger.critical(
                'Unexpected exception while trying to create new document '
                '"%s" from document type "%s"; %s',
                label or unicode(file_object), self, exception
            )
            raise


@python_2_unicode_compatible
class Document(models.Model):
    """
    Defines a single document with it's fields and properties
    """

    uuid = models.CharField(
        default=UUID_FUNCTION, editable=False, max_length=48
    )
    document_type = models.ForeignKey(
        DocumentType, related_name='documents',
        verbose_name=_('Document type')
    )
    label = models.CharField(
        blank=True, db_index=True, default='', max_length=255,
        help_text=_('The name of the document'), verbose_name=_('Label')
    )
    description = models.TextField(
        blank=True, default='', verbose_name=_('Description')
    )
    date_added = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name=_('Added')
    )
    language = models.CharField(
        blank=True, choices=setting_language_choices.value,
        default=setting_language.value, max_length=8,
        verbose_name=_('Language')
    )
    in_trash = models.BooleanField(
        default=False, editable=False, verbose_name=_('In trash?')
    )
    # TODO: set editable to False
    deleted_date_time = models.DateTimeField(
        blank=True, editable=True, null=True,
        verbose_name=_('Date and time trashed')
    )
    is_stub = models.BooleanField(
        default=True, editable=False, help_text=_(
            'A document stub is a document with an entry on the database but '
            'no file uploaded. This could be an interrupted upload or a '
            'deferred upload via the API.'), verbose_name=_('Is stub?')
    )

    objects = DocumentManager()
    passthrough = PassthroughManager()
    trash = TrashCanManager()

    def __str__(self):
        return self.label or ugettext('Document stub, id: %d') % self.pk

    def delete(self, *args, **kwargs):
        to_trash = kwargs.pop('to_trash', True)

        if not self.in_trash and to_trash:
            self.in_trash = True
            self.deleted_date_time = now()
            self.save()
        else:
            for version in self.versions.all():
                version.delete()

            return super(Document, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('documents:document_preview', args=(self.pk,))

    def natural_key(self):
        return (self.uuid,)
    natural_key.dependencies = ['documents.DocumentType']

    def save(self, *args, **kwargs):
        user = kwargs.pop('_user', None)
        new_document = not self.pk
        super(Document, self).save(*args, **kwargs)

        if new_document:
            if user:
                self.add_as_recent_document_for_user(user)
                event_document_create.commit(actor=user, target=self)
            else:
                event_document_create.commit(target=self)
        else:
            event_document_properties_edit.commit(actor=user, target=self)

    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')
        ordering = ('-date_added',)

    def add_as_recent_document_for_user(self, user):
        RecentDocument.objects.add_document_for_user(user, self)

    def exists(self):
        """
        Returns a boolean value that indicates if the document's
        latest version file exists in storage
        """
        return self.latest_version.exists()

    def invalidate_cache(self):
        for document_version in self.versions.all():
            document_version.invalidate_cache()

    def new_version(self, file_object, comment=None, _user=None):
        logger.info('Creating new document version for document: %s', self)

        document_version = DocumentVersion(
            document=self, comment=comment or '', file=File(file_object)
        )
        document_version.save(_user=_user)

        logger.info('New document version queued for document: %s', self)
        return document_version

    def open(self, *args, **kwargs):
        """
        Return a file descriptor to a document's file irrespective of
        the storage backend
        """
        return self.latest_version.open(*args, **kwargs)

    def restore(self):
        self.in_trash = False
        self.save()

    def save_to_file(self, *args, **kwargs):
        return self.latest_version.save_to_file(*args, **kwargs)

    def set_document_type(self, document_type, force=False, _user=None):
        has_changed = self.document_type != document_type

        self.document_type = document_type
        self.save()
        if has_changed or force:
            post_document_type_change.send(
                sender=self.__class__, instance=self
            )

            event_document_type_change.commit(actor=_user, target=self)
            if _user:
                self.add_as_recent_document_for_user(user=_user)

    @property
    def size(self):
        return self.latest_version.size

    # Compatibility methods

    @property
    def checksum(self):
        return self.latest_version.checksum

    @property
    def date_updated(self):
        return self.latest_version.timestamp

    # TODO: rename to file_encoding
    @property
    def file_mime_encoding(self):
        return self.latest_version.encoding

    @property
    def file_mimetype(self):
        return self.latest_version.mimetype

    @property
    def latest_version(self):
        return self.versions.order_by('timestamp').last()

    @property
    def page_count(self):
        return self.latest_version.page_count

    @property
    def pages(self):
        try:
            return self.latest_version.pages
        except AttributeError:
            # Document has no version yet
            return 0

    @property
    def signature_state(self):
        return self.latest_version.signature_state


class DeletedDocument(Document):
    objects = TrashCanManager()

    class Meta:
        proxy = True


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

    document = models.ForeignKey(
        Document, related_name='versions', verbose_name=_('Document')
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name=_('Timestamp')
    )
    comment = models.TextField(
        blank=True, default='', verbose_name=_('Comment')
    )

    # File related fields
    file = models.FileField(
        storage=storage_backend, upload_to=UUID_FUNCTION,
        verbose_name=_('File')
    )
    mimetype = models.CharField(
        blank=True, editable=False, max_length=255, null=True
    )
    encoding = models.CharField(
        blank=True, editable=False, max_length=64, null=True
    )
    checksum = models.TextField(
        blank=True, editable=False, null=True, verbose_name=_('Checksum')
    )

    def __str__(self):
        return '{0} - {1}'.format(self.document, self.timestamp)

    def delete(self, *args, **kwargs):
        for page in self.pages.all():
            page.delete()

        self.file.storage.delete(self.file.name)

        return super(DocumentVersion, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        """
        Overloaded save method that updates the document version's checksum,
        mimetype, and page count when created
        """
        user = kwargs.pop('_user', None)

        new_document_version = not self.pk

        if new_document_version:
            logger.info('Creating new version for document: %s', self.document)
            if NewVersionBlock.objects.is_blocked(self.document):
                raise NewDocumentVersionNotAllowed

        try:
            with transaction.atomic():
                super(DocumentVersion, self).save(*args, **kwargs)

                for key in sorted(DocumentVersion._post_save_hooks):
                    DocumentVersion._post_save_hooks[key](self)

                if new_document_version:
                    # Only do this for new documents
                    self.update_checksum(save=False)
                    self.update_mimetype(save=False)
                    self.save()
                    self.update_page_count(save=False)

                    logger.info(
                        'New document version "%s" created for document: %s',
                        self, self.document
                    )

                    self.document.is_stub = False
                    if not self.document.label:
                        self.document.label = unicode(self.file)

                    self.document.save()
        except Exception as exception:
            logger.error(
                'Error creating new document version for document "%s"; %s',
                self.document, exception
            )
            raise
        else:
            if new_document_version:
                event_document_new_version.commit(
                    actor=user, target=self.document
                )
                post_version_upload.send(sender=self.__class__, instance=self)

                if tuple(self.document.versions.all()) == (self,):
                    post_document_created.send(
                        sender=self.document.__class__, instance=self.document
                    )

    class Meta:
        verbose_name = _('Document version')
        verbose_name_plural = _('Document version')

    @property
    def cache_filename(self):
        return 'document-version-{}'.format(self.uuid)

    def exists(self):
        """
        Returns a boolean value that indicates if the document's file
        exists in storage
        """
        return self.file.storage.exists(self.file.name)

    def get_intermidiate_file(self):
        cache_filename = self.cache_filename
        logger.debug('Intermidiate filename: %s', cache_filename)

        if cache_storage_backend.exists(cache_filename):
            logger.debug('Intermidiate file "%s" found.', cache_filename)

            return cache_storage_backend.open(cache_filename)
        else:
            logger.debug('Intermidiate file "%s" not found.', cache_filename)

            try:
                converter = converter_class(file_object=self.open())
                pdf_file_object = converter.to_pdf()

                with cache_storage_backend.open(cache_filename, 'wb+') as file_object:
                    for chunk in pdf_file_object:
                        file_object.write(chunk)

                return cache_storage_backend.open(cache_filename)
            except InvalidOfficeFormat:
                return self.open()
            except Exception as exception:
                # Cleanup in case of error
                logger.error(
                    'Error creating intermediate file "%s"; %s.',
                    cache_filename, exception
                )
                cache_storage_backend.delete(cache_filename)
                raise

    def invalidate_cache(self):
        cache_storage_backend.delete(self.cache_filename)
        for page in self.pages.all():
            page.invalidate_cache()

    def open(self, raw=False):
        """
        Return a file descriptor to a document version's file irrespective of
        the storage backend
        """
        if raw:
            return self.file.storage.open(self.file.name)
        else:
            result = self.file.storage.open(self.file.name)
            for key in sorted(DocumentVersion._pre_open_hooks):
                result = DocumentVersion._pre_open_hooks[key](result, self)

            return result

    @property
    def page_count(self):
        return self.pages.count()

    def revert(self, _user=None):
        """
        Delete the subsequent versions after this one
        """
        logger.info(
            'Reverting to document document: %s to version: %s',
            self.document, self
        )

        event_document_version_revert.commit(actor=_user, target=self.document)
        for version in self.document.versions.filter(timestamp__gt=self.timestamp):
            version.delete()

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
            return self.file.storage.size(self.file.name)
        else:
            return None

    def update_checksum(self, save=True):
        """
        Open a document version's file and update the checksum field using
        the user provided checksum function
        """
        if self.exists():
            source = self.open()
            self.checksum = unicode(HASH_FUNCTION(source.read()))
            source.close()
            if save:
                self.save()

    def update_mimetype(self, save=True):
        """
        Read a document verions's file and determine the mimetype by calling
        the get_mimetype wrapper
        """
        if self.exists():
            try:
                with self.open() as file_object:
                    self.mimetype, self.encoding = get_mimetype(
                        file_object=file_object
                    )
            except:
                self.mimetype = ''
                self.encoding = ''
            finally:
                if save:
                    self.save()

    def update_page_count(self, save=True):
        try:
            with self.open() as file_object:
                converter = converter_class(
                    file_object=file_object, mime_type=self.mimetype
                )
                detected_pages = converter.get_page_count()
        except PageCountError:
            # If converter backend doesn't understand the format,
            # use 1 as the total page count
            pass
        else:
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

    @property
    def uuid(self):
        # Make cache UUID a mix of document UUID, version ID
        return '{}-{}'.format(self.document.uuid, self.pk)


@python_2_unicode_compatible
class DocumentTypeFilename(models.Model):
    """
    List of labels available to a specific document type for the
    quick rename functionality
    """
    document_type = models.ForeignKey(
        DocumentType, related_name='filenames',
        verbose_name=_('Document type')
    )
    filename = models.CharField(
        db_index=True, max_length=128, verbose_name=_('Label')
    )
    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))

    class Meta:
        ordering = ('filename',)
        unique_together = ('document_type', 'filename')
        verbose_name = _('Quick rename template')
        verbose_name_plural = _('Quick rename templates')

    def __str__(self):
        return self.filename


@python_2_unicode_compatible
class DocumentPage(models.Model):
    """
    Model that describes a document version page
    """
    document_version = models.ForeignKey(
        DocumentVersion, related_name='pages',
        verbose_name=_('Document version')
    )
    page_number = models.PositiveIntegerField(
        db_index=True, default=1, editable=False,
        verbose_name=_('Page number')
    )

    def __str__(self):
        return _(
            'Page %(page_num)d out of %(total_pages)d of %(document)s'
        ) % {
            'document': unicode(self.document),
            'page_num': self.page_number,
            'total_pages': self.document_version.pages.count()
        }

    def delete(self, *args, **kwargs):
        self.invalidate_cache()
        super(DocumentPage, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('documents:document_page_view', args=(self.pk,))

    class Meta:
        ordering = ('page_number',)
        verbose_name = _('Document page')
        verbose_name_plural = _('Document pages')

    @property
    def cache_filename(self):
        return 'page-cache-{}'.format(self.uuid)

    @property
    def document(self):
        return self.document_version.document

    def get_image(self, *args, **kwargs):
        as_base64 = kwargs.pop('as_base64', False)
        transformations = kwargs.pop('transformations', [])
        size = kwargs.pop('size', setting_display_size.value)
        rotation = int(
            kwargs.pop('rotation', DEFAULT_ROTATION) or DEFAULT_ROTATION
        )
        zoom_level = int(
            kwargs.pop('zoom', DEFAULT_ZOOM_LEVEL) or DEFAULT_ZOOM_LEVEL
        )

        if zoom_level < setting_zoom_min_level.value:
            zoom_level = setting_zoom_min_level.value

        if zoom_level > setting_zoom_max_level.value:
            zoom_level = setting_zoom_max_level.value

        rotation = rotation % 360

        cache_filename = self.cache_filename
        logger.debug('Page cache filename: %s', cache_filename)

        if cache_storage_backend.exists(cache_filename):
            logger.debug('Page cache file "%s" found', cache_filename)
            converter = converter_class(
                file_object=cache_storage_backend.open(cache_filename)
            )

            converter.seek(0)
        else:
            logger.debug('Page cache file "%s" not found', cache_filename)

            try:
                converter = converter_class(
                    file_object=self.document_version.get_intermidiate_file()
                )
                converter.seek(page_number=self.page_number - 1)

                page_image = converter.get_page()

                with cache_storage_backend.open(cache_filename, 'wb+') as file_object:
                    file_object.write(page_image.getvalue())
            except Exception as exception:
                # Cleanup in case of error
                logger.error(
                    'Error creating page cache file "%s"; %s',
                    cache_filename, exception
                )
                cache_storage_backend.delete(cache_filename)
                raise

        # Stored transformations
        for stored_transformation in Transformation.objects.get_for_model(self, as_classes=True):
            converter.transform(transformation=stored_transformation)

        # Interactive transformations
        for transformation in transformations:
            converter.transform(transformation=transformation)

        if rotation:
            converter.transform(transformation=TransformationRotate(
                degrees=rotation)
            )

        if size:
            converter.transform(transformation=TransformationResize(
                **dict(zip(('width', 'height'), (size.split('x')))))
            )

        if zoom_level:
            converter.transform(
                transformation=TransformationZoom(percent=zoom_level)
            )

        page_image = converter.get_page()

        if as_base64:
            # TODO: don't prepend 'data:%s;base64,%s' part
            return 'data:%s;base64,%s' % (
                'image/png', base64.b64encode(page_image.getvalue())
            )
        else:
            return page_image

    def invalidate_cache(self):
        cache_storage_backend.delete(self.cache_filename)

    @property
    def siblings(self):
        return DocumentPage.objects.filter(
            document_version=self.document_version
        )

    @property
    def uuid(self):
        """
        Make cache UUID a mix of version ID and page ID to avoid using stale
        images
        """
        return '{}-{}'.format(self.document_version.uuid, self.pk)


class NewVersionBlock(models.Model):
    document = models.ForeignKey(Document, verbose_name=_('Document'))

    objects = NewVersionBlockManager()

    class Meta:
        verbose_name = _('New version block')
        verbose_name_plural = _('New version blocks')


@python_2_unicode_compatible
class RecentDocument(models.Model):
    """
    Keeps a list of the n most recent accessed or created document for
    a given user
    """
    user = models.ForeignKey(
        User, db_index=True, editable=False, verbose_name=_('User')
    )
    document = models.ForeignKey(
        Document, editable=False, verbose_name=_('Document')
    )
    datetime_accessed = models.DateTimeField(
        auto_now=True, db_index=True, verbose_name=_('Accessed')
    )

    objects = RecentDocumentManager()

    def __str__(self):
        return unicode(self.document)

    def natural_key(self):
        return self.document.natural_key() + self.user.natural_key()
    natural_key.dependencies = ['documents.Document', 'auth.User']

    class Meta:
        ordering = ('-datetime_accessed',)
        verbose_name = _('Recent document')
        verbose_name_plural = _('Recent documents')
