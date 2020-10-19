import logging

from furl import furl

from django.db import models
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from mayan.apps.converter.classes import ConverterBase
from mayan.apps.converter.literals import DEFAULT_ZOOM_LEVEL, DEFAULT_ROTATION
from mayan.apps.converter.models import LayerTransformation
from mayan.apps.converter.transformations import (
    BaseTransformation, TransformationResize, TransformationRotate,
    TransformationZoom
)
from mayan.apps.lock_manager.backends.base import LockingBackend

from ..managers import DocumentFilePageManager
from ..settings import (
    setting_display_width, setting_display_height, setting_zoom_max_level,
    setting_zoom_min_level
)

from .document_file_models import DocumentFile
from .mixins import ModelMixinPagedModel

__all__ = ('DocumentFilePage', 'DocumentFilePageResult')
logger = logging.getLogger(name=__name__)


class DocumentFilePage(ModelMixinPagedModel, models.Model):
    """
    Model that describes a document file page
    """
    _paged_model_parent_field = 'document_file'

    document_file = models.ForeignKey(
        on_delete=models.CASCADE, related_name='file_pages', to=DocumentFile,
        verbose_name=_('Document file')
    )
    page_number = models.PositiveIntegerField(
        db_index=True, default=1, editable=False,
        verbose_name=_('Page number')
    )

    objects = DocumentFilePageManager()

    class Meta:
        ordering = ('page_number',)
        verbose_name = _('Document file page')
        verbose_name_plural = _('Document file pages')

    def __str__(self):
        return self.get_label()

    @cached_property
    def cache_partition(self):
        partition, created = self.document_file.cache.partitions.get_or_create(
            name=self.uuid
        )
        return partition

    def delete(self, *args, **kwargs):
        self.cache_partition.delete()
        super().delete(*args, **kwargs)

    @property
    def document(self):
        return self.document_file.document

    def generate_image(self, user=None, **kwargs):
        transformation_list = self.get_combined_transformation_list(user=user, **kwargs)
        combined_cache_filename = BaseTransformation.combine(
            transformations=transformation_list
        )

        # Check is transformed image is available
        logger.debug('transformations cache filename: %s', combined_cache_filename)

        try:
            lock = LockingBackend.get_instance().acquire_lock(
                name='document_file_page_generate_image_{}_{}'.format(
                    self.pk, combined_cache_filename
                )
            )
        except Exception:
            raise
        else:
            # Second try block to release the lock even on fatal errors inside
            # the block.
            try:
                if self.cache_partition.get_file(filename=combined_cache_filename):
                    logger.debug(
                        'transformations cache file "%s" found', combined_cache_filename
                    )
                else:
                    logger.debug(
                        'transformations cache file "%s" not found', combined_cache_filename
                    )
                    image = self.get_image(transformations=transformation_list)
                    with self.cache_partition.create_file(filename=combined_cache_filename) as file_object:
                        file_object.write(image.getvalue())
                return combined_cache_filename
            finally:
                lock.release()

    def get_absolute_url(self):
        return reverse(
            viewname='documents:document_file_page_view', kwargs={
                'document_file_page_id': self.pk
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
        transformations_hash = BaseTransformation.combine(
            self.get_combined_transformation_list(*args, **kwargs)
        )

        kwargs.pop('transformations', None)

        final_url = furl()
        final_url.args = kwargs
        final_url.path = reverse(
            viewname='rest_api:documentfilepage-image', kwargs={
                'document_id': self.document_file.document_id,
                'document_file_id': self.document_file_id,
                'document_file_page_id': self.pk
            }
        )
        final_url.args['_hash'] = transformations_hash

        return final_url.tostr()

    def get_combined_transformation_list(self, user=None, *args, **kwargs):
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

        maximum_layer_order = kwargs.get('maximum_layer_order', None)

        # Stored transformations first
        for stored_transformation in LayerTransformation.objects.get_for_object(
            obj=self, maximum_layer_order=maximum_layer_order, as_classes=True,
            user=user
        ):
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
        cache_filename = 'base_image'
        logger.debug('Page cache filename: %s', cache_filename)

        cache_file = self.cache_partition.get_file(filename=cache_filename)

        if cache_file:
            logger.debug('Page cache file "%s" found', cache_filename)

            with cache_file.open() as file_object:
                converter = ConverterBase.get_converter_class()(
                    file_object=file_object
                )

                converter.seek_page(page_number=0)

                # This code is also repeated below to allow using a context
                # manager with cache_file.open and close it automatically.
                # Apply runtime transformations
                for transformation in transformations:
                    converter.transform(transformation=transformation)

                return converter.get_page()
        else:
            logger.debug('Page cache file "%s" not found', cache_filename)

            try:
                with self.document_file.get_intermediate_file() as file_object:
                    converter = ConverterBase.get_converter_class()(
                        file_object=file_object
                    )
                    converter.seek_page(page_number=self.page_number - 1)

                    page_image = converter.get_page()

                    # Since open "wb+" doesn't create files, create it explicitly
                    with self.cache_partition.create_file(filename=cache_filename) as file_object:
                        file_object.write(page_image.getvalue())

                    # Apply runtime transformations
                    for transformation in transformations:
                        converter.transform(transformation=transformation)

                    return converter.get_page()
            except Exception as exception:
                # Cleanup in case of error
                logger.error(
                    'Error creating page cache file "%s"; %s',
                    cache_filename, exception
                )
                raise

    @property
    def is_in_trash(self):
        return self.document.is_in_trash

    def get_label(self):
        return _(
            'Document file page %(page_num)d of %(total_pages)d from %(document_file)s'
        ) % {
            'document_file': force_text(self.document_file),
            'page_num': self.page_number,
            'total_pages': self.get_pages_last_number() or 1
        }
    get_label.short_description = _('Label')

    def natural_key(self):
        return (self.page_number, self.document_file.natural_key())
    natural_key.dependencies = ['documents.DocumentFile']

    @property
    def uuid(self):
        """
        Make cache UUID a mix of file ID and page ID to avoid using stale
        images
        """
        return '{}-{}'.format(self.document_file.uuid, self.pk)


class DocumentFilePageResult(DocumentFilePage):
    class Meta:
        ordering = ('document_file__document', 'page_number')
        proxy = True
        verbose_name = _('Document file page')
        verbose_name_plural = _('Document file pages')
