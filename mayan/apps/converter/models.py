import hashlib
import io
import logging
import uuid

from PIL import Image
from furl import furl

from django.apps import apps
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Max
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext, ugettext_lazy as _

from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.common.validators import (
    YAMLValidator, validate_internal_name
)
from mayan.apps.events.classes import EventManagerSave
from mayan.apps.events.decorators import method_event
from mayan.apps.storage.classes import DefinedStorageLazy

from .classes import Layer
from .events import event_asset_created, event_asset_edited
from .literals import STORAGE_NAME_ASSETS, STORAGE_NAME_ASSETS_CACHE
from .managers import LayerTransformationManager, ObjectLayerManager
from .transformations import BaseTransformation

logger = logging.getLogger(name=__name__)


def upload_to(instance, filename):
    return 'converter-asset-{}'.format(uuid.uuid4().hex)


class Asset(ExtraDataModelMixin, models.Model):
    """
    This model keeps track of files that will be available for use with
    transformations.
    """
    label = models.CharField(
        max_length=96, unique=True, verbose_name=_('Label')
    )
    internal_name = models.CharField(
        db_index=True, help_text=_(
            'This value will be used when referencing this asset. '
            'Can only contain letters, numbers, and underscores.'
        ), max_length=255, unique=True, validators=[validate_internal_name],
        verbose_name=_('Internal name')
    )
    file = models.FileField(
        storage=DefinedStorageLazy(name=STORAGE_NAME_ASSETS),
        upload_to=upload_to, verbose_name=_('File')
    )

    class Meta:
        ordering = ('label',)
        verbose_name = _('Asset')
        verbose_name_plural = _('Assets')

    def __str__(self):
        return self.label

    @cached_property
    def cache(self):
        Cache = apps.get_model(app_label='file_caching', model_name='Cache')
        return Cache.objects.get(
            defined_storage_name=STORAGE_NAME_ASSETS_CACHE
        )

    @cached_property
    def cache_partition(self):
        partition, created = self.cache.partitions.get_or_create(
            name='{}'.format(self.pk)
        )
        return partition

    def delete(self, *args, **kwargs):
        self.cache_partition.delete()
        self.file.storage.delete(name=self.file.name)
        return super().delete(*args, **kwargs)

    def generate_image(self):
        cache_filename = '{}'.format(self.get_hash())

        if self.cache_partition.get_file(filename=cache_filename):
            logger.debug(
                'asset cache file "%s" found', cache_filename
            )
        else:
            logger.debug(
                'asset cache file "%s" not found', cache_filename
            )

            image = self.get_image()
            image_buffer = io.BytesIO()
            image.save(image_buffer, format='PNG')
            with self.cache_partition.create_file(filename=cache_filename) as file_object:
                file_object.write(image_buffer.getvalue())

        return cache_filename

    def get_absolute_url(self):
        return reverse(
            viewname='converter:asset_detail', kwargs={
                'asset_id': self.pk
            }
        )

    def get_api_image_url(self, *args, **kwargs):
        final_url = furl()
        final_url.args = kwargs
        final_url.path = reverse(
            viewname='rest_api:asset-image',
            kwargs={'asset_id': self.pk}
        )
        final_url.args['_hash'] = self.get_hash()

        return final_url.tostr()

    def get_hash(self):
        with self.open() as file_object:
            return hashlib.sha256(file_object.read()).hexdigest()

    def get_image(self):
        with self.open() as file_object:
            image = Image.open(fp=file_object)

            if image.mode != 'RGBA':
                image.putalpha(alpha=255)

            return image

    def open(self):
        return self.file.storage.open(name=self.file.name)

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_asset_created,
            'target': 'self',
        },
        edited={
            'event': event_asset_edited,
            'target': 'self',
        }
    )
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class StoredLayer(models.Model):
    name = models.CharField(
        max_length=64, unique=True, verbose_name=_('Name')
    )
    order = models.PositiveIntegerField(
        db_index=True, unique=True, verbose_name=_('Order')
    )

    class Meta:
        ordering = ('order',)
        verbose_name = _('Stored layer')
        verbose_name_plural = _('Stored layers')

    def __str__(self):
        return self.name

    def get_layer(self):
        return Layer.get(name=self.name)


class ObjectLayer(models.Model):
    content_type = models.ForeignKey(on_delete=models.CASCADE, to=ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        ct_field='content_type', fk_field='object_id'
    )
    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))
    stored_layer = models.ForeignKey(
        on_delete=models.CASCADE, related_name='object_layers', to=StoredLayer,
        verbose_name=_('Stored layer')
    )

    objects = ObjectLayerManager()

    class Meta:
        ordering = ('stored_layer__order',)
        unique_together = ('content_type', 'object_id', 'stored_layer')
        verbose_name = _('Object layer')
        verbose_name_plural = _('Object layers')

    def get_next_order(self):
        last_order = self.transformations.aggregate(
            Max('order')
        )['order__max']

        if last_order is not None:
            return last_order + 1
        else:
            return 0


class LayerTransformation(models.Model):
    """
    Model that stores the transformation and transformation arguments
    for a given object
    Fields:
    * order - Order of a Transformation - In case there are multiple
    transformations for an object, this field list the order at which
    they will be execute.
    * arguments - Arguments of a Transformation - An optional field to hold a
    transformation argument. Example: if a page is rotated with the Rotation
    transformation, this field will show by how many degrees it was rotated.
    """
    object_layer = models.ForeignKey(
        on_delete=models.CASCADE, related_name='transformations',
        to=ObjectLayer, verbose_name=_('Object layer')
    )
    order = models.PositiveIntegerField(
        blank=True, db_index=True, default=0, help_text=_(
            'Order in which the transformations will be executed. If left '
            'unchanged, an automatic order value will be assigned.'
        ), verbose_name=_('Order')
    )
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    arguments = models.TextField(
        blank=True, help_text=_(
            'Enter the arguments for the transformation as a YAML '
            'dictionary. ie: {"degrees": 180}'
        ), validators=[YAMLValidator()], verbose_name=_('Arguments')
    )
    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))

    objects = LayerTransformationManager()

    class Meta:
        ordering = ('object_layer__stored_layer__order', 'order',)
        unique_together = ('object_layer', 'order')
        verbose_name = _('Layer transformation')
        verbose_name_plural = _('Layer transformations')

    def __str__(self):
        try:
            return str(BaseTransformation.get(name=self.name))
        except KeyError:
            return ugettext('Unknown transformation class')

    def get_transformation_class(self):
        return BaseTransformation.get(name=self.name)

    def save(self, *args, **kwargs):
        if not self.order:
            self.order = self.object_layer.get_next_order()
        super().save(*args, **kwargs)
