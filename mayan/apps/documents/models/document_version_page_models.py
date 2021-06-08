import logging

from furl import furl
from PIL import Image

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.converter.classes import ConverterBase
from mayan.apps.converter.literals import DEFAULT_ZOOM_LEVEL, DEFAULT_ROTATION
from mayan.apps.converter.models import LayerTransformation
from mayan.apps.converter.transformations import (
    BaseTransformation, TransformationResize, TransformationRotate,
    TransformationZoom
)
from mayan.apps.events.classes import EventManagerMethodAfter, EventManagerSave
from mayan.apps.events.decorators import method_event
from mayan.apps.file_caching.models import CachePartitionFile
from mayan.apps.lock_manager.backends.base import LockingBackend

from ..events import (
    event_document_version_page_created, event_document_version_page_deleted,
    event_document_version_page_edited
)
from ..literals import DOCUMENT_IMAGE_TASK_TIMEOUT
from ..managers import ValidDocumentVersionPageManager
from ..settings import (
    setting_display_width, setting_display_height, setting_zoom_max_level,
    setting_zoom_min_level
)

from .document_version_models import DocumentVersion
from .mixins import PagedModelMixin

__all__ = ('DocumentVersionPage', 'DocumentVersionPageSearchResult')
logger = logging.getLogger(name=__name__)


class DocumentVersionPage(
    ExtraDataModelMixin, PagedModelMixin, models.Model
):
    _paged_model_parent_field = 'document_version'

    document_version = models.ForeignKey(
        on_delete=models.CASCADE, related_name='version_pages',
        to=DocumentVersion, verbose_name=_('Document version')
    )
    page_number = models.PositiveIntegerField(
        db_index=True, default=1, help_text=_(
            'Unique integer number for the page. Pages are ordered by '
            'this number.'
        ), verbose_name=_('Page number')
    )
    content_type = models.ForeignKey(
        help_text=_('Content type for the source object of the page.'),
        on_delete=models.CASCADE, to=ContentType
    )
    object_id = models.PositiveIntegerField(
        help_text=_('ID for the source object of the page.')
    )
    content_object = GenericForeignKey(
        ct_field='content_type', fk_field='object_id'
    )

    class Meta:
        ordering = ('page_number',)
        unique_together = ('document_version', 'page_number')
        verbose_name = _('Document version page')
        verbose_name_plural = _('Document version pages')

    objects = models.Manager()
    valid = ValidDocumentVersionPageManager()

    def __str__(self):
        return self.get_label()

    @cached_property
    def cache_partition(self):
        partition, created = self.document_version.cache.partitions.get_or_create(
            name=self.uuid
        )
        return partition

    @method_event(
        event_manager_class=EventManagerMethodAfter,
        event=event_document_version_page_deleted,
        target='document_version',
    )
    def delete(self, *args, **kwargs):
        self.cache_partition.delete()
        super().delete(*args, **kwargs)

    def export(self, file_object, append=False, resolution=None):
        if not resolution:
            resolution = 300.0

        cache_filename = self.generate_image()
        with self.cache_partition.get_file(filename=cache_filename).open() as image_file_object:
            Image.open(fp=image_file_object).save(
                append=append, format='PDF', fp=file_object,
                resolution=resolution
            )

    def generate_image(self, user=None, _acquire_lock=True, **kwargs):
        transformation_list = self.get_combined_transformation_list(
            user=user, **kwargs
        )
        combined_cache_filename = self.get_combined_cache_filename(
            _transformation_list=transformation_list
        )

        logger.debug(
            'transformations cache filename: %s', combined_cache_filename
        )

        content_object_lock_name = self.content_object.get_lock_name(user=user)
        try:
            content_object_lock = LockingBackend.get_backend().acquire_lock(
                name=content_object_lock_name,
                timeout=DOCUMENT_IMAGE_TASK_TIMEOUT * 2
            )
        except Exception:
            raise
        else:
            lock_name = self.get_lock_name(
                _combined_cache_filename=combined_cache_filename
            )
            try:
                if _acquire_lock:
                    lock = LockingBackend.get_backend().acquire_lock(
                        name=lock_name, timeout=DOCUMENT_IMAGE_TASK_TIMEOUT
                    )
            except Exception:
                raise
            else:
                # Second try block to release the lock even on fatal errors inside
                # the block.
                try:
                    try:
                        self.cache_partition.get_file(
                            filename=combined_cache_filename
                        )
                    except CachePartitionFile.DoesNotExist:
                        logger.debug(
                            'transformations cache file "%s" not found, '
                            'generating new image', combined_cache_filename
                        )
                        image = self.get_image(transformations=transformation_list)
                        with self.cache_partition.create_file(filename=combined_cache_filename) as file_object:
                            file_object.write(image.getvalue())
                    else:
                        logger.debug(
                            'transformations cache file "%s" found, '
                            'returning it to caller', combined_cache_filename
                        )

                    return combined_cache_filename
                finally:
                    if _acquire_lock:
                        lock.release()
            finally:
                content_object_lock.release()

    def get_absolute_url(self):
        return reverse(
            viewname='documents:document_version_page_view', kwargs={
                'document_version_page_id': self.pk
            }
        )

    def get_api_image_url(self, *args, **kwargs):
        """
        Create an unique URL combining:
        - the page's image URL
        - the interactive argument
        - a hash from the server side and interactive transformations
        The purpose of this unique URL is to allow client side caching
        if document page images.
        """
        if not self.content_object:
            return '#'

        # Source object transformations first.
        transformation_list = LayerTransformation.objects.get_for_object(
            obj=self.content_object, as_classes=True,
        )

        transformation_list.extend(
            self.get_combined_transformation_list(*args, **kwargs)
        )
        transformations_hash = BaseTransformation.combine(
            transformations=transformation_list
        )

        kwargs.pop('transformations', None)

        final_url = furl()
        final_url.args = kwargs
        final_url.path = reverse(
            viewname='rest_api:documentversionpage-image', kwargs={
                'document_id': self.document_version.document_id,
                'document_version_id': self.document_version_id,
                'document_version_page_id': self.pk
            }
        )
        final_url.args['_hash'] = transformations_hash

        return final_url.tostr()

    def get_combined_cache_filename(self, _transformation_list=None, user=None, **kwargs):
        transformation_list = _transformation_list or self.get_combined_transformation_list(
            user=user, **kwargs
        )

        content_object_cache_filename = self.content_object.get_combined_cache_filename(
            user=user
        )
        return '{}-{}'.format(
            content_object_cache_filename,
            BaseTransformation.combine(transformations=transformation_list)
        )

    def get_combined_transformation_list(self, user=None, *args, **kwargs):
        """
        Return a list of transformation containing the server side
        document page transformation as well as tranformations created
        from the arguments as transient interactive transformation.
        """
        # Convert arguments into transformations.
        transformations = kwargs.get('transformations', [])

        # Set sensible defaults if the argument is not specified or if the
        # argument is None.
        width = kwargs.get('width', setting_display_width.value) or setting_display_width.value
        height = kwargs.get('height', setting_display_height.value) or setting_display_height.value
        rotation = kwargs.get('rotation', DEFAULT_ROTATION) or DEFAULT_ROTATION
        zoom_level = kwargs.get('zoom', DEFAULT_ZOOM_LEVEL) or DEFAULT_ZOOM_LEVEL

        if zoom_level < setting_zoom_min_level.value:
            zoom_level = setting_zoom_min_level.value

        if zoom_level > setting_zoom_max_level.value:
            zoom_level = setting_zoom_max_level.value

        # Generate transformation hash.
        transformation_list = []

        maximum_layer_order = kwargs.get('maximum_layer_order', None)

        # Stored transformations first.
        transformation_list.extend(
            LayerTransformation.objects.get_for_object(
                obj=self, maximum_layer_order=maximum_layer_order,
                as_classes=True, user=user
            )
        )

        # Interactive transformations second.
        transformation_list.extend(transformations)

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
        cache_filename = '{}-base_image'.format(self.content_object.get_combined_cache_filename())
        logger.debug('Page cache filename: %s', cache_filename)

        try:
            cache_file = self.cache_partition.get_file(filename=cache_filename)
        except CachePartitionFile.DoesNotExist:
            logger.debug('Page cache version "%s" not found', cache_filename)

            try:
                content_object_cache_filename = self.content_object.generate_image(
                    _acquire_lock=False
                )
                content_object_cache_file = self.content_object.cache_partition.get_file(
                    filename=content_object_cache_filename
                )

                with content_object_cache_file.open() as file_object:
                    converter = ConverterBase.get_converter_class()(
                        file_object=file_object
                    )
                    converter.seek_page(page_number=0)

                    page_image = converter.get_page()

                    # Since open "wb+" doesn't create versions, create it
                    # explicitly.
                    with self.cache_partition.create_file(filename=cache_filename) as file_object:
                        file_object.write(page_image.getvalue())

                    # Apply runtime transformations.
                    for transformation in transformations or ():
                        converter.transform(transformation=transformation)

                    return converter.get_page()
            except Exception as exception:
                # Cleanup in case of error.
                logger.error(
                    'Error creating document version page cache file '
                    'named "%s"; %s', cache_filename, exception,
                    exc_info=True
                )
                raise
        else:
            logger.debug('Page cache version "%s" found', cache_filename)

            with cache_file.open() as file_object:
                converter = ConverterBase.get_converter_class()(
                    file_object=file_object
                )

                converter.seek_page(page_number=0)

                # This code is also repeated below to allow using a context
                # manager with cache_version.open and close it automatically.
                # Apply runtime transformations.
                for transformation in transformations or ():
                    converter.transform(transformation=transformation)

                return converter.get_page()

    def get_label(self):
        return _(
            '%(document_version)s page %(page_number)d of %(total_pages)d'
        ) % {
            'document_version': force_text(s=self.document_version),
            'page_number': self.page_number,
            'total_pages': self.get_pages_last_number() or 1
        }
    get_label.short_description = _('Label')

    def get_lock_name(self, _combined_cache_filename=None, user=None, **kwargs):
        if _combined_cache_filename:
            combined_cache_filename = _combined_cache_filename
        else:
            transformation_list = self.get_combined_transformation_list(
                user=user, **kwargs
            )

            combined_cache_filename = self.get_combined_cache_filename(
                _transformation_list=transformation_list, user=None, **kwargs
            )

        return 'document_version_page_generate_image_{}_{}'.format(
            self.pk, combined_cache_filename
        )

    @property
    def is_in_trash(self):
        return self.document_version.is_in_trash

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_document_version_page_created,
            'action_object': 'document_version',
            'target': 'self',
        },
        edited={
            'event': event_document_version_page_edited,
            'action_object': 'document_version',
            'target': 'self',
        }
    )
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    @property
    def uuid(self):
        """
        Make cache UUID a mix of version ID and page ID to avoid using stale
        images.
        """
        return '{}-{}'.format(self.document_version.uuid, self.pk)


class DocumentVersionPageSearchResult(DocumentVersionPage):
    class Meta:
        proxy = True
        verbose_name = _('Document version page')
        verbose_name_plural = _('Document version pages')
