import hashlib
import logging
import shutil

from django.apps import apps
from django.db import models, transaction
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.classes import ModelQueryFields
from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.common.signals import signal_mayan_pre_save
from mayan.apps.converter.classes import ConverterBase
from mayan.apps.converter.exceptions import (
    InvalidOfficeFormat, PageCountError
)
from mayan.apps.events.classes import EventManagerMethodAfter
from mayan.apps.events.decorators import method_event
from mayan.apps.file_caching.models import CachePartitionFile
from mayan.apps.mimetype.api import get_mimetype
from mayan.apps.storage.classes import DefinedStorageLazy

from ..events import (
    event_document_file_created, event_document_file_deleted,
    event_document_file_downloaded, event_document_file_edited
)
from ..literals import (
    STORAGE_NAME_DOCUMENT_FILE_PAGE_IMAGE_CACHE, STORAGE_NAME_DOCUMENT_FILES
)
from ..managers import DocumentFileManager, ValidDocumentFileManager
from ..settings import setting_hash_block_size
from ..signals import (
    signal_post_document_created, signal_post_document_file_upload
)

from .document_models import Document
from .mixins import HooksModelMixin

__all__ = ('DocumentFile', 'DocumentFileSearchResult')
logger = logging.getLogger(name=__name__)


def upload_to(instance, filename):
    return instance.document.document_type.get_upload_filename(
        instance=instance, filename=filename
    )


class DocumentFile(
    ExtraDataModelMixin, HooksModelMixin, models.Model
):
    """
    Model that describes a document file and its properties
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
    _hooks_pre_create = []
    _pre_open_hooks = []
    _pre_save_hooks = []
    _post_save_hooks = []

    document = models.ForeignKey(
        on_delete=models.CASCADE, related_name='files', to=Document,
        verbose_name=_('Document')
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, db_index=True, help_text=_(
            'The server date and time when the document file was processed.'
        ), verbose_name=_('Timestamp')
    )
    comment = models.TextField(
        blank=True, default='', help_text=_(
            'An optional short text describing the document file.'
        ), verbose_name=_('Comment')
    )
    # File related fields.
    file = models.FileField(
        storage=DefinedStorageLazy(name=STORAGE_NAME_DOCUMENT_FILES),
        upload_to=upload_to, verbose_name=_('File')
    )
    filename = models.CharField(
        blank=True, max_length=255, verbose_name=_('Filename')
    )
    mimetype = models.CharField(
        blank=True, editable=False, help_text=_(
            'The document file\'s file mimetype. MIME types are a '
            'standard way to describe the format of a file, in this case '
            'the file format of the document. Some examples: "text/plain" '
            'or "image/jpeg". '
        ), max_length=255, null=True, verbose_name=_('MIME type')
    )
    encoding = models.CharField(
        blank=True, editable=False, help_text=_(
            'The document file file encoding. binary 7-bit, binary 8-bit, '
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
        verbose_name = _('Document file')
        verbose_name_plural = _('Document files')

    objects = DocumentFileManager()
    valid = ValidDocumentFileManager()

    @staticmethod
    def hash_function():
        return hashlib.sha256()

    @classmethod
    def execute_pre_create_hooks(cls, kwargs=None):
        """
        Helper method to allow checking if it is possible to create
        a new document file.
        """
        cls._execute_hooks(
            hook_list=cls._hooks_pre_create, instance=None, kwargs=kwargs
        )

    @classmethod
    def register_post_save_hook(cls, func, order=None):
        cls._insert_hook_entry(
            hook_list=cls._post_save_hooks, func=func, order=order
        )

    @classmethod
    def register_pre_create_hook(cls, func, order=None):
        cls._insert_hook_entry(
            hook_list=cls._hooks_pre_create, func=func, order=order
        )

    @classmethod
    def register_pre_open_hook(cls, func, order=None):
        cls._insert_hook_entry(
            hook_list=cls._pre_open_hooks, func=func, order=order
        )

    @classmethod
    def register_pre_save_hook(cls, func, order=None):
        cls._insert_hook_entry(
            hook_list=cls._pre_save_hooks, func=func, order=order
        )

    def __str__(self):
        return self.get_label()

    @cached_property
    def cache(self):
        Cache = apps.get_model(app_label='file_caching', model_name='Cache')
        return Cache.objects.get(
            defined_storage_name=STORAGE_NAME_DOCUMENT_FILE_PAGE_IMAGE_CACHE
        )

    @cached_property
    def cache_partition(self):
        partition, created = self.cache.partitions.get_or_create(
            name='file-{}'.format(self.uuid)
        )
        return partition

    def checksum_update(self, save=True):
        """
        Open a document file's file and update the checksum field using
        the user provided checksum function.
        """
        block_size = setting_hash_block_size.value
        if block_size == 0:
            # If the setting value is 0 that means disable read limit. To disable
            # the read limit passing None won't work, we pass -1 instead as per
            # the Python documentation.
            # https://docs.python.org/2/tutorial/inputoutput.html#methods-of-file-objects
            block_size = -1

        if self.exists():
            hash_object = DocumentFile.hash_function()
            with self.open() as file_object:
                while (True):
                    data = file_object.read(block_size)
                    if not data:
                        break

                    hash_object.update(data)

            self.checksum = force_text(s=hash_object.hexdigest())
            if save:
                self.save(update_fields=('checksum',))

            return self.checksum

    @method_event(
        event_manager_class=EventManagerMethodAfter,
        event=event_document_file_deleted,
        target='document',
    )
    def delete(self, *args, **kwargs):
        for page in self.pages.all():
            page.delete()

        self.file.storage.delete(name=self.file.name)
        self.cache_partition.delete()

        result = super().delete(*args, **kwargs)

        if self.document.files.count() == 0:
            self.document.is_stub = False
            self.document._event_ignore = True
            self.document.save(update_fields=('is_stub',))

        return result

    def execute_pre_save_hooks(self):
        """
        Helper method to allow checking if new files are possible from
        outside the model. Currently used by the document file upload link
        condition.
        """
        DocumentFile._execute_hooks(
            hook_list=DocumentFile._pre_save_hooks, instance=self
        )

    def exists(self):
        """
        Returns a boolean value that indicates if the document's file
        exists in storage. Returns True if the document's file is verified to
        be in the document storage. This is a diagnostic flag to help users
        detect if the storage has desynchronized (ie: Amazon's S3).
        """
        return self.file.storage.exists(self.file.name)

    def get_absolute_url(self):
        return reverse(
            viewname='documents:document_file_preview', kwargs={
                'document_file_id': self.pk
            }
        )

    def get_api_image_url(self, *args, **kwargs):
        first_page = self.pages.first()
        if first_page:
            return first_page.get_api_image_url(*args, **kwargs)

    def get_cache_partitions(self):
        result = [self.cache_partition]
        for page in self.file_pages.all():
            result.append(page.cache_partition)

        return result

    @method_event(
        event_manager_class=EventManagerMethodAfter,
        event=event_document_file_downloaded,
        target='self',
    )
    def get_download_file_object(self):
        # Thin wrapper to make sure the normal views and API views trigger
        # then download event in the same way.
        return self.open()

    def get_intermediate_file(self):
        cache_filename = 'intermediate_file'

        try:
            cache_file = self.cache_partition.get_file(filename=cache_filename)
        except CachePartitionFile.DoesNotExist:
            logger.debug('Intermediate file not found.')

            try:
                with self.open() as file_object:
                    converter = ConverterBase.get_converter_class()(
                        file_object=file_object
                    )
                    with converter.to_pdf() as pdf_file_object:
                        with self.cache_partition.create_file(filename=cache_filename) as file_object:
                            shutil.copyfileobj(
                                fsrc=pdf_file_object, fdst=file_object
                            )

                        return self.cache_partition.get_file(filename=cache_filename).open()
            except InvalidOfficeFormat:
                return self.open()
            except Exception as exception:
                logger.error(
                    'Error creating intermediate file "%s"; %s.',
                    cache_filename, exception, exc_info=True
                )
                try:
                    cache_file = self.cache_partition.get_file(
                        filename=cache_filename
                    )
                except CachePartitionFile.DoesNotExist:
                    """Non fatal, ignore."""
                else:
                    cache_file.delete()
                raise exception
        else:
            logger.debug('Intermediate file found.')
            return cache_file.open()

    def get_label(self):
        return self.filename
    get_label.short_description = _('Label')

    def mimetype_update(self, save=True):
        """
        Read a document verions's file and determine the mimetype by calling
        the get_mimetype wrapper.
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
                    self.save(update_fields=('encoding', 'mimetype'))

    def natural_key(self):
        return (self.checksum, self.document.natural_key())
    natural_key.dependencies = ['documents.Document']

    @property
    def is_in_trash(self):
        return self.document.is_in_trash

    def open(self, raw=False):
        """
        Return a file descriptor to a document file's file irrespective of
        the storage backend.
        """
        if raw:
            return self.file.storage.open(name=self.file.name)
        else:
            file_object = self.file.storage.open(name=self.file.name)

            result = DocumentFile._execute_hooks(
                hook_list=DocumentFile._pre_open_hooks,
                instance=self, file_object=file_object
            )

            if result:
                return result['file_object']
            else:
                return file_object

    def page_count_update(self, save=True):
        try:
            with self.open() as file_object:
                converter = ConverterBase.get_converter_class()(
                    file_object=file_object, mime_type=self.mimetype
                )
                detected_pages = converter.get_page_count()
        except PageCountError:
            """Converter backend doesn't understand the format."""
        else:
            DocumentFilePage = apps.get_model(
                app_label='documents', model_name='DocumentFilePage'
            )

            self.pages.all().delete()

            for page_number in range(detected_pages):
                DocumentFilePage.objects.create(
                    document_file=self, page_number=page_number + 1
                )

            if save:
                self.save()

            return detected_pages

    @property
    def pages(self):
        DocumentFilePage = apps.get_model(
            app_label='documents', model_name='DocumentFilePage'
        )
        queryset = ModelQueryFields.get(model=DocumentFilePage).get_queryset()
        return queryset.filter(pk__in=self.file_pages.values('pk'))

    def save(self, *args, **kwargs):
        """
        Overloaded save method that updates the document file's checksum,
        mimetype, and page count when created.
        """
        user = kwargs.pop('_user', self.__dict__.pop('_event_actor', None))
        new_document_file = not self.pk

        if new_document_file:
            logger.info('Creating new file for document: %s', self.document)
            DocumentFile.execute_pre_create_hooks(
                kwargs={
                    'document': self.document,
                    'shared_uploaded_file': None,
                    'user': user
                }
            )

        try:
            with transaction.atomic():
                self.execute_pre_save_hooks()

                signal_mayan_pre_save.send(
                    instance=self, sender=DocumentFile, user=user
                )

                super().save(*args, **kwargs)

                DocumentFile._execute_hooks(
                    hook_list=DocumentFile._post_save_hooks,
                    instance=self
                )

                if new_document_file:
                    # Only do this for new documents.
                    event_document_file_created.commit(
                        actor=user, target=self, action_object=self.document
                    )
                    self.checksum_update(save=False)
                    self.mimetype_update(save=False)
                    self._event_actor = user
                    self.save()
                    self.page_count_update(save=False)

                    logger.info(
                        'New document file "%s" created for document: %s',
                        self, self.document
                    )

                    self.document.is_stub = False
                    if not self.document.label:
                        self.document.label = force_text(s=self.file)

                    self.document._event_ignore = True
                    self.document.save(update_fields=('is_stub', 'label'))
                else:
                    event_document_file_edited.commit(
                        actor=user, target=self, action_object=self.document
                    )
        except Exception as exception:
            logger.error(
                'Error creating new document file for document "%s"; %s',
                self.document, exception, exc_info=True
            )
            raise
        else:
            if new_document_file:
                signal_post_document_file_upload.send(
                    sender=DocumentFile, instance=self
                )

                if tuple(self.document.files.all()) == (self,):
                    signal_post_document_created.send(
                        instance=self.document, sender=Document
                    )

    def save_to_file(self, file_object):
        """
        Save a copy of the document from the document storage backend
        to the local filesystem.
        """
        with self.open() as input_file_object:
            shutil.copyfileobj(fsrc=input_file_object, fdst=file_object)

    @property
    def size(self):
        if self.exists():
            return self.file.storage.size(self.file.name)
        else:
            return None

    @property
    def uuid(self):
        # Make cache UUID a mix of document UUID, file ID.
        return '{}-{}'.format(self.document.uuid, self.pk)


class DocumentFileSearchResult(DocumentFile):
    class Meta:
        proxy = True
