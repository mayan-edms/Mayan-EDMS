from __future__ import absolute_import, unicode_literals

import logging

from furl import furl

from django.db import models
from django.urls import reverse
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from mayan.apps.converter.literals import DEFAULT_ZOOM_LEVEL, DEFAULT_ROTATION

from mayan.apps.converter.models import LayerTransformation
from mayan.apps.converter.transformations import (
    BaseTransformation, TransformationResize, TransformationRotate,
    TransformationZoom
)
from mayan.apps.converter.utils import get_converter_class

from ..managers import DocumentVersionPageManager
from ..settings import (
    setting_display_width, setting_display_height, setting_zoom_max_level,
    setting_zoom_min_level
)

from .document_version_models import DocumentVersion

__all__ = ('DocumentVersionPage', 'DocumentVersionPageResult')
logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class DocumentVersionPage(models.Model):
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

    objects = DocumentVersionPageManager()

    class Meta:
        ordering = ('page_number',)
        verbose_name = _('Document version page')
        verbose_name_plural = _('Document version pages')

    def __str__(self):
        return self.get_label()

    @cached_property
    def cache_partition(self):
        partition, created = self.document_version.cache.partitions.get_or_create(
            name=self.uuid
        )
        return partition

    def delete(self, *args, **kwargs):
        self.cache_partition.delete()
        super(DocumentVersionPage, self).delete(*args, **kwargs)

    @property
    def document(self):
        return self.document_version.document

    def generate_image(self, user=None, **kwargs):
        transformation_list = self.get_combined_transformation_list(user=user, **kwargs)
        combined_cache_filename = BaseTransformation.combine(transformation_list)

        # Check is transformed image is available
        logger.debug('transformations cache filename: %s', combined_cache_filename)

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

    def get_absolute_url(self):
        return reverse(
            viewname='documents:document_version_page_view', kwargs={
                'pk': self.pk
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
            viewname='rest_api:documentversionpage-image', kwargs={
                'pk': self.document.pk, 'version_pk': self.document_version.pk,
                'page_pk': self.pk
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
            self, maximum_layer_order=maximum_layer_order, as_classes=True,
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
                converter = get_converter_class()(
                    file_object=file_object
                )

                converter.seek_page(page_number=0)

                # This code is also repeated below to allow using a context
                # manager with cache_file.open and close it automatically.
                # Apply runtime transformations
                for transformation in transformations or []:
                    converter.transform(transformation=transformation)

                return converter.get_page()
        else:
            logger.debug('Page cache file "%s" not found', cache_filename)

            try:
                with self.document_version.get_intermediate_file() as file_object:
                    converter = get_converter_class()(
                        file_object=file_object
                    )
                    converter.seek_page(page_number=self.page_number - 1)

                    page_image = converter.get_page()

                    # Since open "wb+" doesn't create files, create it explicitly
                    with self.cache_partition.create_file(filename=cache_filename) as file_object:
                        file_object.write(page_image.getvalue())

                    # Apply runtime transformations
                    for transformation in transformations or []:
                        converter.transform(transformation=transformation)

                    return converter.get_page()
            except Exception as exception:
                # Cleanup in case of error
                logger.error(
                    'Error creating page cache file "%s"; %s',
                    cache_filename, exception
                )
                raise

    def get_label(self):
        return _(
            'Version page %(page_number)d out of %(total_pages)d of %(document)s'
        ) % {
            'document': force_text(self.document),
            'page_number': self.page_number,
            'total_pages': self.document_version.pages.count()
        }
    get_label.short_description = _('Label')

    @property
    def is_in_trash(self):
        return self.document_version.document.is_in_trash

    def natural_key(self):
        return (self.page_number, self.document_version.natural_key())
    natural_key.dependencies = ['documents.DocumentVersion']

    @property
    def siblings(self):
        return DocumentVersionPage.objects.filter(
            document_version=self.document_version
        )

    @property
    def uuid(self):
        """
        Make cache UUID a mix of version ID and page ID to avoid using stale
        images
        """
        return '{}-{}'.format(self.document_version.uuid, self.pk)


class DocumentVersionPageResult(DocumentVersionPage):
    class Meta:
        ordering = ('document_version__document', 'page_number')
        proxy = True
        verbose_name = _('Document version page')
        verbose_name_plural = _('Document version pages')
