from __future__ import absolute_import, unicode_literals

import hashlib
import logging
import os
import uuid

from furl import furl

from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.db import models, transaction
from django.template import Template, Context
from django.urls import reverse
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext, ugettext_lazy as _

from acls.models import AccessControlList
from common.literals import TIME_DELTA_UNIT_CHOICES
from converter import (
    converter_class, BaseTransformation, TransformationResize,
    TransformationRotate, TransformationZoom
)
from converter.exceptions import InvalidOfficeFormat, PageCountError
from converter.literals import DEFAULT_ZOOM_LEVEL, DEFAULT_ROTATION
from converter.models import Transformation
from mimetype.api import get_mimetype

from .events import (
    event_document_create, event_document_new_version,
    event_document_properties_edit, event_document_type_change,
    event_document_type_created, event_document_type_edited,
    event_document_version_revert
)
from .literals import DEFAULT_DELETE_PERIOD, DEFAULT_DELETE_TIME_UNIT
from .managers import (
    DocumentManager, DocumentPageCachedImage, DocumentPageManager,
    DocumentVersionManager, DocumentTypeManager, DuplicatedDocumentManager,
    FavoriteDocumentManager, PassthroughManager, RecentDocumentManager,
    TrashCanManager
)
from .permissions import permission_document_view
from .settings import (
    setting_disable_base_image_cache, setting_disable_transformed_image_cache,
    setting_display_width, setting_display_height, setting_fix_orientation,
    setting_hash_block_size, setting_language, setting_zoom_max_level,
    setting_zoom_min_level
)
from .signals import (
    post_document_created, post_document_type_change, post_version_upload
)
from .storages import storage_documentversion, storage_documentimagecache

logger = logging.getLogger(__name__)


# document image cache name hash function
def hash_function():
    return hashlib.sha256()


def UUID_FUNCTION(*args, **kwargs):
    return force_text(uuid.uuid4())


@python_2_unicode_compatible
class DocumentType(models.Model):
    """
    Define document types or classes to which a specific set of
    properties can be attached
    """
    label = models.CharField(
        help_text=_('The name of the document type.'), max_length=96,
        unique=True, verbose_name=_('Label')
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
        blank=True, default=DEFAULT_DELETE_PERIOD, help_text=_(
            'Amount of time after which documents of this type in the trash '
            'will be deleted.'
        ), null=True, verbose_name=_('Delete time period')
    )
    delete_time_unit = models.CharField(
        blank=True, choices=TIME_DELTA_UNIT_CHOICES,
        default=DEFAULT_DELETE_TIME_UNIT, max_length=8, null=True,
        verbose_name=_('Delete time unit')
    )

    objects = DocumentTypeManager()

    class Meta:
        ordering = ('label',)
        verbose_name = _('Document type')
        verbose_name_plural = _('Documents types')

    def __str__(self):
        return self.label

    def delete(self, *args, **kwargs):
        for document in Document.passthrough.filter(document_type=self):
            document.delete(to_trash=False)

        return super(DocumentType, self).delete(*args, **kwargs)

    @property
    def deleted_documents(self):
        return DeletedDocument.objects.filter(document_type=self)

    def get_absolute_url(self):
        return reverse(
            'documents:document_type_document_list', args=(self.pk,)
        )

    def get_document_count(self, user):
        queryset = AccessControlList.objects.filter_by_access(
            permission_document_view, user, queryset=self.documents
        )

        return queryset.count()

    def natural_key(self):
        return (self.label,)

    def new_document(self, file_object, label=None, description=None, language=None, _user=None):
        try:
            with transaction.atomic():
                document = self.documents.create(
                    description=description or '',
                    label=label or file_object.name,
                    language=language or setting_language.value
                )
                document.save(_user=_user)

                document.new_version(file_object=file_object, _user=_user)
                return document
        except Exception as exception:
            logger.critical(
                'Unexpected exception while trying to create new document '
                '"%s" from document type "%s"; %s',
                label or file_object.name, self, exception
            )
            raise

    def save(self, *args, **kwargs):
        user = kwargs.pop('_user', None)
        created = not self.pk

        result = super(DocumentType, self).save(*args, **kwargs)

        if created:
            event_document_type_created.commit(
                actor=user, target=self
            )
        else:
            event_document_type_edited.commit(
                actor=user, target=self
            )

        return result


@python_2_unicode_compatible
class Document(models.Model):
    """
    Defines a single document with it's fields and properties
    Fields:
    * uuid - UUID of a document, universally Unique ID. An unique identifier
    generated for each document. No two documents can ever have the same UUID.
    This ID is generated automatically.
    """
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, help_text=_(
            'UUID of a document, universally Unique ID. An unique identifier'
            'generated for each document.'
        ), verbose_name=_('UUID')
    )
    document_type = models.ForeignKey(
        on_delete=models.CASCADE, related_name='documents', to=DocumentType,
        verbose_name=_('Document type')
    )
    label = models.CharField(
        blank=True, db_index=True, default='', max_length=255,
        help_text=_('The name of the document.'), verbose_name=_('Label')
    )
    description = models.TextField(
        blank=True, default='', help_text=_(
            'An optional short text describing a document.'
        ), verbose_name=_('Description')
    )
    date_added = models.DateTimeField(
        auto_now_add=True, db_index=True, help_text=_(
            'The server date and time when the document was finally '
            'processed and added to the system.'
        ), verbose_name=_('Added')
    )
    language = models.CharField(
        blank=True, default=setting_language.value, help_text=_(
            'The dominant language in the document.'
        ), max_length=8, verbose_name=_('Language')
    )
    in_trash = models.BooleanField(
        db_index=True, default=False, help_text=_(
            'Whether or not this document is in the trash.'
        ), editable=False, verbose_name=_('In trash?')
    )
    # TODO: set editable to False
    deleted_date_time = models.DateTimeField(
        blank=True, editable=True, help_text=_(
            'The server date and time when the document was moved to the '
            'trash.'
        ), null=True, verbose_name=_('Date and time trashed')
    )
    is_stub = models.BooleanField(
        db_index=True, default=True, editable=False, help_text=_(
            'A document stub is a document with an entry on the database but '
            'no file uploaded. This could be an interrupted upload or a '
            'deferred upload via the API.'
        ), verbose_name=_('Is stub?')
    )

    objects = DocumentManager()
    passthrough = PassthroughManager()
    trash = TrashCanManager()

    class Meta:
        ordering = ('label',)
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')

    def __str__(self):
        return self.label or ugettext('Document stub, id: %d') % self.pk

    def add_as_recent_document_for_user(self, user):
        return RecentDocument.objects.add_document_for_user(user, self)

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

    def exists(self):
        """
        Returns a boolean value that indicates if the document's
        latest version file exists in storage
        """
        latest_version = self.latest_version
        if latest_version:
            return latest_version.exists()
        else:
            return False

    def get_absolute_url(self):
        return reverse('documents:document_preview', args=(self.pk,))

    def get_api_image_url(self, *args, **kwargs):
        latest_version = self.latest_version
        if latest_version:
            return latest_version.get_api_image_url(*args, **kwargs)
        else:
            return '#'

    def invalidate_cache(self):
        for document_version in self.versions.all():
            document_version.invalidate_cache()

    @property
    def is_in_trash(self):
        return self.in_trash

    def natural_key(self):
        return (self.uuid,)
    natural_key.dependencies = ['documents.DocumentType']

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

    def save(self, *args, **kwargs):
        user = kwargs.pop('_user', None)
        _commit_events = kwargs.pop('_commit_events', True)
        new_document = not self.pk
        super(Document, self).save(*args, **kwargs)

        if new_document:
            if user:
                self.add_as_recent_document_for_user(user)
                event_document_create.commit(
                    actor=user, target=self, action_object=self.document_type
                )
            else:
                event_document_create.commit(
                    target=self, action_object=self.document_type
                )
        else:
            if _commit_events:
                event_document_properties_edit.commit(actor=user, target=self)

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
            return DocumentPage.objects.none()


class DeletedDocument(Document):
    objects = TrashCanManager()

    class Meta:
        proxy = True


@python_2_unicode_compatible
class DocumentVersion(models.Model):
    """
    Model that describes a document version and its properties
    Fields:
    * mimetype - File mimetype. MIME types are a standard way to describe the
    format of a file, in this case the file format of the document.
    Some examples: "text/plain" or "image/jpeg". Mayan uses this to determine
    how to render a document's file. More information:
    http://www.freeformatter.com/mime-types-list.html
    * encoding - File Encoding. The filesystem encoding of the document's
    file: binary 7-bit, binary 8-bit, text, base64, etc.
    * checksum - A hash/checkdigit/fingerprint generated from the document's
    binary data. Only identical documents will have the same checksum. If a
    document is modified after upload it's checksum will not match, used for
    detecting file tampering among other things.
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
        on_delete=models.CASCADE, related_name='versions', to=Document,
        verbose_name=_('Document')
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, db_index=True, help_text=_(
            'The server date and time when the document version was processed.'
        ), verbose_name=_('Timestamp')
    )
    comment = models.TextField(
        blank=True, default='', help_text=_(
            'An optional short text describing the document version.'
        ), verbose_name=_('Comment')
    )

    # File related fields
    file = models.FileField(
        storage=storage_documentversion, upload_to=UUID_FUNCTION,
        verbose_name=_('File')
    )
    mimetype = models.CharField(
        blank=True, editable=False, help_text=_(
            'The document version\'s file mimetype. MIME types are a '
            'standard way to describe the format of a file, in this case '
            'the file format of the document. Some examples: "text/plain" '
            'or "image/jpeg". '
        ), max_length=255, null=True, verbose_name=_('MIME type')
    )
    encoding = models.CharField(
        blank=True, editable=False, help_text=_(
            'The document version file encoding. binary 7-bit, binary 8-bit, '
            'text, base64, etc.'
        ), max_length=64, null=True, verbose_name=_('Encoding')
    )
    checksum = models.CharField(
        blank=True, db_index=True, editable=False, help_text=(
            'A hash/checkdigit/fingerprint generated from the document\'s '
            'binary data. Only identical documents will have the same '
            'checksum.'
        ), max_length=64, null=True, verbose_name=_('Checksum')
    )

    class Meta:
        ordering = ('timestamp',)
        verbose_name = _('Document version')
        verbose_name_plural = _('Document version')

    objects = DocumentVersionManager()

    def __str__(self):
        return self.get_rendered_string()

    @property
    def cache_filename(self):
        return 'document-version-{}'.format(self.uuid)

    def delete(self, *args, **kwargs):
        for page in self.pages.all():
            page.delete()

        self.file.storage.delete(self.file.name)

        return super(DocumentVersion, self).delete(*args, **kwargs)

    def exists(self):
        """
        Returns a boolean value that indicates if the document's file
        exists in storage. Returns True if the document's file is verified to
        be in the document storage. This is a diagnostic flag to help users
        detect if the storage has desynchronized (ie: Amazon's S3).
        """
        return self.file.storage.exists(self.file.name)

    def fix_orientation(self):
        for page in self.pages.all():
            degrees = page.detect_orientation()
            if degrees:
                Transformation.objects.add_for_model(
                    obj=page, transformation=TransformationRotate,
                    arguments='{{"degrees": {}}}'.format(360 - degrees)
                )

    def get_absolute_url(self):
        return reverse('documents:document_version_view', args=(self.pk,))

    def get_api_image_url(self, *args, **kwargs):
        first_page = self.pages.first()
        if first_page:
            return first_page.get_api_image_url(*args, **kwargs)
        else:
            return '#'

    def get_intermidiate_file(self):
        cache_filename = self.cache_filename
        logger.debug('Intermidiate filename: %s', cache_filename)

        if storage_documentimagecache.exists(cache_filename):
            logger.debug('Intermidiate file "%s" found.', cache_filename)

            return storage_documentimagecache.open(cache_filename)
        else:
            logger.debug('Intermidiate file "%s" not found.', cache_filename)

            try:
                converter = converter_class(file_object=self.open())
                pdf_file_object = converter.to_pdf()

                with storage_documentimagecache.open(cache_filename, mode='wb+') as file_object:
                    for chunk in pdf_file_object:
                        file_object.write(chunk)

                return storage_documentimagecache.open(cache_filename)
            except InvalidOfficeFormat:
                return self.open()
            except Exception as exception:
                # Cleanup in case of error
                logger.error(
                    'Error creating intermediate file "%s"; %s.',
                    cache_filename, exception
                )
                storage_documentimagecache.delete(cache_filename)
                raise

    def get_rendered_string(self, preserve_extension=False):
        if preserve_extension:
            filename, extension = os.path.splitext(self.document.label)
            return '{} ({}){}'.format(
                filename, self.get_rendered_timestamp(), extension
            )
        else:
            return Template(
                '{{ instance.document }} - {{ instance.timestamp }}'
            ).render(context=Context({'instance': self}))

    def get_rendered_timestamp(self):
        return Template('{{ instance.timestamp }}').render(
            context=Context({'instance': self})
        )

    def natural_key(self):
        return (self.checksum, self.document.natural_key())
    natural_key.dependencies = ['documents.Document']

    def invalidate_cache(self):
        storage_documentimagecache.delete(self.cache_filename)
        for page in self.pages.all():
            page.invalidate_cache()

    @property
    def is_in_trash(self):
        return self.document.is_in_trash

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
                result = DocumentVersion._pre_open_hooks[key](
                    file_object=result, document_version=self
                )

            return result

    @property
    def page_count(self):
        """
        The number of pages that the document posses.
        """
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

    def save(self, *args, **kwargs):
        """
        Overloaded save method that updates the document version's checksum,
        mimetype, and page count when created
        """
        user = kwargs.pop('_user', None)
        new_document_version = not self.pk

        if new_document_version:
            logger.info('Creating new version for document: %s', self.document)

        try:
            with transaction.atomic():
                super(DocumentVersion, self).save(*args, **kwargs)

                for key in sorted(DocumentVersion._post_save_hooks):
                    DocumentVersion._post_save_hooks[key](
                        document_version=self
                    )

                if new_document_version:
                    # Only do this for new documents
                    self.update_checksum(save=False)
                    self.update_mimetype(save=False)
                    self.save()
                    self.update_page_count(save=False)
                    if setting_fix_orientation.value:
                        self.fix_orientation()

                    logger.info(
                        'New document version "%s" created for document: %s',
                        self, self.document
                    )

                    self.document.is_stub = False
                    if not self.document.label:
                        self.document.label = force_text(self.file)

                    self.document.save(_commit_events=False)
        except Exception as exception:
            logger.error(
                'Error creating new document version for document "%s"; %s',
                self.document, exception
            )
            raise
        else:
            if new_document_version:
                event_document_new_version.commit(
                    actor=user, target=self, action_object=self.document
                )
                post_version_upload.send(sender=DocumentVersion, instance=self)

                if tuple(self.document.versions.all()) == (self,):
                    post_document_created.send(
                        sender=Document, instance=self.document
                    )

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
        block_size = setting_hash_block_size.value
        if block_size == 0:
            # If the setting value is 0 that means disable read limit. To disable
            # the read limit passing None won't work, we pass -1 instead as per
            # the Python documentation.
            # https://docs.python.org/2/tutorial/inputoutput.html#methods-of-file-objects
            block_size = -1

        if self.exists():
            hash_object = hash_function()
            with self.open() as file_object:
                while (True):
                    data = file_object.read(block_size)
                    if not data:
                        break

                    hash_object.update(data)

            self.checksum = force_text(hash_object.hexdigest())
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
            except Exception:
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
        on_delete=models.CASCADE, related_name='filenames', to=DocumentType,
        verbose_name=_('Document type')
    )
    filename = models.CharField(
        db_index=True, max_length=128, verbose_name=_('Label')
    )
    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))

    class Meta:
        ordering = ('filename',)
        unique_together = ('document_type', 'filename')
        verbose_name = _('Quick label')
        verbose_name_plural = _('Quick labels')

    def __str__(self):
        return self.filename


@python_2_unicode_compatible
class DocumentPage(models.Model):
    """
    Model that describes a document version page
    """
    document_version = models.ForeignKey(
        on_delete=models.CASCADE, related_name='pages', to=DocumentVersion,
        verbose_name=_('Document version')
    )
    page_number = models.PositiveIntegerField(
        db_index=True, default=1, editable=False,
        verbose_name=_('Page number')
    )

    objects = DocumentPageManager()

    class Meta:
        ordering = ('page_number',)
        verbose_name = _('Document page')
        verbose_name_plural = _('Document pages')

    def __str__(self):
        return _(
            'Page %(page_num)d out of %(total_pages)d of %(document)s'
        ) % {
            'document': force_text(self.document),
            'page_num': self.page_number,
            'total_pages': self.document_version.pages.count()
        }

    @property
    def cache_filename(self):
        return 'page-cache-{}'.format(self.uuid)

    def delete(self, *args, **kwargs):
        self.invalidate_cache()
        super(DocumentPage, self).delete(*args, **kwargs)

    def detect_orientation(self):
        with self.document_version.open() as file_object:
            converter = converter_class(
                file_object=file_object,
                mime_type=self.document_version.mimetype
            )
            return converter.detect_orientation(
                page_number=self.page_number
            )

    @property
    def document(self):
        return self.document_version.document

    def generate_image(self, *args, **kwargs):
        transformation_list = self.get_combined_transformation_list(*args, **kwargs)

        cache_filename = '{}-{}'.format(
            self.cache_filename, BaseTransformation.combine(transformation_list)
        )

        # Check is transformed image is available
        logger.debug('transformations cache filename: %s', cache_filename)

        if not setting_disable_transformed_image_cache.value and storage_documentimagecache.exists(cache_filename):
            logger.debug(
                'transformations cache file "%s" found', cache_filename
            )
        else:
            logger.debug(
                'transformations cache file "%s" not found', cache_filename
            )
            image = self.get_image(transformations=transformation_list)
            with storage_documentimagecache.open(cache_filename, 'wb+') as file_object:
                file_object.write(image.getvalue())

            self.cached_images.create(filename=cache_filename)

        return cache_filename

    def get_absolute_url(self):
        return reverse('documents:document_page_view', args=(self.pk,))

    def get_api_image_url(self, *args, **kwargs):
        """
        Create an unique URL combining:
        - the page's image URL
        - the interactive argument
        - a hash from the server side and interactive transformations
        The purpose of this unique URL is to allow client side caching
        if document page images.
        """
        transformations_hash = BaseTransformation.combine(
            self.get_combined_transformation_list(*args, **kwargs)
        )

        kwargs.pop('transformations', None)

        final_url = furl()
        final_url.args = kwargs
        final_url.path = reverse(
            'rest_api:documentpage-image', args=(
                self.document.pk, self.document_version.pk, self.pk
            )
        )
        final_url.args['_hash'] = transformations_hash

        return final_url.tostr()

    def get_combined_transformation_list(self, *args, **kwargs):
        """
        Return a list of transformation containing the server side
        document page transformation as well as tranformations created
        from the arguments as transient interactive transformation.
        """
        # Convert arguments into transformations
        transformations = kwargs.get('transformations', [])

        # Set sensible defaults if the argument is not specified or if the
        # argument is None
        width = kwargs.get('width', setting_display_width.value) or setting_display_width.value
        height = kwargs.get('height', setting_display_height.value) or setting_display_height.value
        rotation = kwargs.get('rotation', DEFAULT_ROTATION) or DEFAULT_ROTATION
        zoom_level = kwargs.get('zoom', DEFAULT_ZOOM_LEVEL) or DEFAULT_ZOOM_LEVEL

        if zoom_level < setting_zoom_min_level.value:
            zoom_level = setting_zoom_min_level.value

        if zoom_level > setting_zoom_max_level.value:
            zoom_level = setting_zoom_max_level.value

        # Generate transformation hash

        transformation_list = []

        # Stored transformations first
        for stored_transformation in Transformation.objects.get_for_model(self, as_classes=True):
            transformation_list.append(stored_transformation)

        # Interactive transformations second
        for transformation in transformations:
            transformation_list.append(transformation)

        if rotation:
            transformation_list.append(
                TransformationRotate(degrees=rotation)
            )

        if width:
            transformation_list.append(
                TransformationResize(width=width, height=height)
            )

        if zoom_level:
            transformation_list.append(TransformationZoom(percent=zoom_level))

        return transformation_list

    def get_image(self, transformations=None):
        cache_filename = self.cache_filename
        logger.debug('Page cache filename: %s', cache_filename)

        if not setting_disable_base_image_cache.value and storage_documentimagecache.exists(cache_filename):
            logger.debug('Page cache file "%s" found', cache_filename)
            converter = converter_class(
                file_object=storage_documentimagecache.open(cache_filename)
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

                # Since open "wb+" doesn't create files, check if the file
                # exists, if not then create it
                if not storage_documentimagecache.exists(cache_filename):
                    storage_documentimagecache.save(name=cache_filename, content=ContentFile(content=''))

                with storage_documentimagecache.open(cache_filename, 'wb+') as file_object:
                    file_object.write(page_image.getvalue())
            except Exception as exception:
                # Cleanup in case of error
                logger.error(
                    'Error creating page cache file "%s"; %s',
                    cache_filename, exception
                )
                storage_documentimagecache.delete(cache_filename)
                raise

        for transformation in transformations:
            converter.transform(transformation=transformation)

        return converter.get_page()

    def invalidate_cache(self):
        storage_documentimagecache.delete(self.cache_filename)
        for cached_image in self.cached_images.all():
            cached_image.delete()

    @property
    def is_in_trash(self):
        return self.document.is_in_trash

    def natural_key(self):
        return (self.page_number, self.document_version.natural_key())
    natural_key.dependencies = ['documents.DocumentVersion']

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


class DocumentPageCachedImage(models.Model):
    document_page = models.ForeignKey(
        on_delete=models.CASCADE, related_name='cached_images',
        to=DocumentPage, verbose_name=_('Document page')
    )
    datetime = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name=_('Date time')
    )
    filename = models.CharField(max_length=128, verbose_name=_('Filename'))
    file_size = models.PositiveIntegerField(
        db_index=True, default=0, verbose_name=_('File size')
    )

    objects = DocumentPageCachedImage()

    class Meta:
        verbose_name = _('Document page cached image')
        verbose_name_plural = _('Document page cached images')

    def delete(self, *args, **kwargs):
        storage_documentimagecache.delete(self.filename)
        return super(DocumentPageCachedImage, self).delete(*args, **kwargs)

    def natural_key(self):
        return (self.filename, self.document_page.natural_key())
    natural_key.dependencies = ['documents.DocumentPage']

    def save(self, *args, **kwargs):
        self.file_size = storage_documentimagecache.size(self.filename)
        return super(DocumentPageCachedImage, self).save(*args, **kwargs)


class DocumentPageResult(DocumentPage):
    class Meta:
        ordering = ('document_version__document', 'page_number')
        proxy = True
        verbose_name = _('Document page')
        verbose_name_plural = _('Document pages')


@python_2_unicode_compatible
class DuplicatedDocument(models.Model):
    document = models.ForeignKey(
        on_delete=models.CASCADE, related_name='duplicates', to=Document,
        verbose_name=_('Document')
    )
    documents = models.ManyToManyField(
        to=Document, verbose_name=_('Duplicated documents')
    )
    datetime_added = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name=_('Added')
    )

    objects = DuplicatedDocumentManager()

    class Meta:
        verbose_name = _('Duplicated document')
        verbose_name_plural = _('Duplicated documents')

    def __str__(self):
        return force_text(self.document)


@python_2_unicode_compatible
class FavoriteDocument(models.Model):
    """
    Keeps a list of the favorited documents of a given user
    """
    user = models.ForeignKey(
        db_index=True, editable=False, on_delete=models.CASCADE,
        to=settings.AUTH_USER_MODEL, verbose_name=_('User')
    )
    document = models.ForeignKey(
        editable=False, on_delete=models.CASCADE, related_name='favorites',
        to=Document, verbose_name=_('Document')
    )

    objects = FavoriteDocumentManager()

    class Meta:
        verbose_name = _('Favorite document')
        verbose_name_plural = _('Favorite documents')

    def __str__(self):
        return force_text(self.document)

    def natural_key(self):
        return (self.document.natural_key(), self.user.natural_key())
    natural_key.dependencies = ['documents.Document', settings.AUTH_USER_MODEL]


@python_2_unicode_compatible
class RecentDocument(models.Model):
    """
    Keeps a list of the n most recent accessed or created document for
    a given user
    """
    user = models.ForeignKey(
        db_index=True, editable=False, on_delete=models.CASCADE,
        to=settings.AUTH_USER_MODEL, verbose_name=_('User')
    )
    document = models.ForeignKey(
        editable=False, on_delete=models.CASCADE, related_name='recent',
        to=Document, verbose_name=_('Document')
    )
    datetime_accessed = models.DateTimeField(
        auto_now=True, db_index=True, verbose_name=_('Accessed')
    )

    objects = RecentDocumentManager()

    class Meta:
        ordering = ('-datetime_accessed',)
        verbose_name = _('Recent document')
        verbose_name_plural = _('Recent documents')

    def __str__(self):
        return force_text(self.document)

    def natural_key(self):
        return (self.datetime_accessed, self.document.natural_key(), self.user.natural_key())
    natural_key.dependencies = ['documents.Document', settings.AUTH_USER_MODEL]
