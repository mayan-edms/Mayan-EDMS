from __future__ import absolute_import, unicode_literals

import hashlib
import logging
import os
import shutil
import uuid

from django.apps import apps
from django.db import models, transaction
from django.template import Template, Context
from django.urls import reverse
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from mayan.apps.converter.exceptions import InvalidOfficeFormat, PageCountError
from mayan.apps.converter.models import Transformation
from mayan.apps.converter.transformations import TransformationRotate
from mayan.apps.converter.utils import get_converter_class
from mayan.apps.mimetype.api import get_mimetype

from ..events import event_document_new_version, event_document_version_revert
from ..literals import DOCUMENT_IMAGES_CACHE_NAME
from ..managers import DocumentVersionManager
from ..settings import setting_fix_orientation, setting_hash_block_size
from ..signals import post_document_created, post_version_upload
from ..storages import storage_documentversion

from .document_models import Document

__all__ = ('DocumentVersion',)
logger = logging.getLogger(__name__)


# document image cache name hash function
def hash_function():
    return hashlib.sha256()


def UUID_FUNCTION(*args, **kwargs):
    return force_text(uuid.uuid4())


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

    @classmethod
    def register_pre_open_hook(cls, order, func):
        cls._pre_open_hooks[order] = func

    @classmethod
    def register_post_save_hook(cls, order, func):
        cls._post_save_hooks[order] = func

    def __str__(self):
        return self.get_rendered_string()

    @cached_property
    def cache(self):
        Cache = apps.get_model(app_label='file_caching', model_name='Cache')
        return Cache.objects.get(name=DOCUMENT_IMAGES_CACHE_NAME)

    @cached_property
    def cache_partition(self):
        partition, created = self.cache.partitions.get_or_create(
            name='version-{}'.format(self.uuid)
        )
        return partition

    def delete(self, *args, **kwargs):
        for page in self.pages.all():
            page.delete()

        self.file.storage.delete(self.file.name)
        self.cache_partition.delete()

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
                Transformation.objects.add_to_object(
                    obj=page, transformation=TransformationRotate,
                    arguments='{{"degrees": {}}}'.format(360 - degrees)
                )

    def get_absolute_url(self):
        return reverse(
            viewname='documents:document_version_view', kwargs={
                'pk': self.pk
            }
        )

    def get_api_image_url(self, *args, **kwargs):
        first_page = self.pages.first()
        if first_page:
            return first_page.get_api_image_url(*args, **kwargs)

    def get_intermediate_file(self):
        cache_filename = 'intermediate_file'
        cache_file = self.cache_partition.get_file(filename=cache_filename)
        if cache_file:
            logger.debug('Intermidiate file found.')
            return cache_file.open()
        else:
            logger.debug('Intermidiate file not found.')

            try:
                with self.open() as version_file_object:
                    converter = get_converter_class()(
                        file_object=version_file_object
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
                    cache_filename, exception
                )
                cache_file = self.cache_partition.get_file(filename=cache_filename)
                if cache_file:
                    cache_file.delete()
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
    def pages_all(self):
        DocumentPage = apps.get_model(
            app_label='documents', model_name='DocumentPage'
        )
        return DocumentPage.passthrough.filter(document_version=self)

    @property
    def pages(self):
        return self.version_pages.all()

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

        with transaction.atomic():
            event_document_version_revert.commit(
                actor=_user, target=self.document
            )
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

    def save_to_file(self, file_object):
        """
        Save a copy of the document from the document storage backend
        to the local filesystem
        """
        with self.open() as input_file_object:
            shutil.copyfileobj(fsrc=input_file_object, fdst=file_object)

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
                converter = get_converter_class()(
                    file_object=file_object, mime_type=self.mimetype
                )
                detected_pages = converter.get_page_count()
        except PageCountError:
            # If converter backend doesn't understand the format,
            # use 1 as the total page count
            pass
        else:
            DocumentPage = apps.get_model(
                app_label='documents', model_name='DocumentPage'
            )

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
