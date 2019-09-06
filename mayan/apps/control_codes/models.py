from __future__ import unicode_literals

import hashlib
import logging

from furl import furl

from django.apps import apps
from django.core import serializers
from django.db import models
from django.db.models import Max
from django.urls import reverse
from django.utils.encoding import (
    force_bytes, force_text, python_2_unicode_compatible
)
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.serialization import yaml_load
from mayan.apps.common.validators import YAMLValidator

from .classes import ControlCode
from .literals import CONTROL_SHEET_CODE_IMAGE_CACHE_NAME
from .managers import ControlSheetCodeBusinessLogicManager

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class ControlSheet(models.Model):
    label = models.CharField(
        help_text=_('Short text to describe the control sheet.'),
        max_length=196, unique=True, verbose_name=_('Label')
    )

    class Meta:
        ordering = ('label',)
        verbose_name = _('Control sheet')
        verbose_name_plural = _('Control sheets')

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse(
            viewname='control_codes:control_sheet_detail', kwargs={
                'control_sheet_id': self.pk
            }
        )


@python_2_unicode_compatible
class ControlSheetCode(models.Model):
    control_sheet = models.ForeignKey(
        on_delete=models.CASCADE, related_name='codes', to=ControlSheet,
        verbose_name=_('Control sheet')
    )
    order = models.PositiveIntegerField(
        blank=True, db_index=True, default=0, help_text=_(
            'Order in which the control sheet codes will be interpreted. '
            'If left unchanged, an automatic order value will be assigned.'
        ), verbose_name=_('Order')
    )
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    arguments = models.TextField(
        blank=True, help_text=_(
            'The arguments for the control sheet code as a YAML '
            'dictionary.'
        ), validators=[YAMLValidator()], verbose_name=_('Arguments')
    )
    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))

    business_logic = ControlSheetCodeBusinessLogicManager()
    objects = models.Manager()

    class Meta:
        ordering = ('order',)
        verbose_name = _('Control sheet code')
        verbose_name_plural = _('Control sheet codes')

    def __str__(self):
        return force_text(self.get_label())

    @cached_property
    def cache(self):
        Cache = apps.get_model(app_label='file_caching', model_name='Cache')
        return Cache.objects.get(name=CONTROL_SHEET_CODE_IMAGE_CACHE_NAME)

    @cached_property
    def cache_partition(self):
        partition, created = self.cache.partitions.get_or_create(
            name='{}'.format(self.pk)
        )
        return partition

    def delete(self, *args, **kwargs):
        self.cache_partition.delete()
        return super(ControlSheetCode, self).delete(*args, **kwargs)

    def generate_image(self):
        cache_filename = '{}'.format(self.get_hash())

        if self.cache_partition.get_file(filename=cache_filename):
            logger.debug(
                'workflow cache file "%s" found', cache_filename
            )
        else:
            logger.debug(
                'workflow cache file "%s" not found', cache_filename
            )

            image = self.render()
            with self.cache_partition.create_file(filename=cache_filename) as file_object:
                image.save(file_object)

        return cache_filename

    def get_api_image_url(self, *args, **kwargs):
        final_url = furl()
        final_url.args = kwargs
        final_url.path = reverse(
            viewname='rest_api:controlsheet-code-image',
            kwargs={
                'control_sheet_id': self.control_sheet.pk,
                'control_sheet_code_id': self.pk
            }
        )
        final_url.args['_hash'] = self.get_hash()

        return final_url.tostr()

    def get_arguments(self):
        return yaml_load(self.arguments or '{}')

    def get_control_code_class(self):
        return ControlCode.get(name=self.name)

    def get_control_code_instance(self):
        return self.get_control_code_class()(
            **self.get_arguments()
        )

    def get_display(self):
        return force_text(self.get_control_code_instance())

    def get_hash(self):
        objects_lists = list(
            ControlSheetCode.objects.filter(pk=self.pk)
        )

        return hashlib.sha256(
            force_bytes(
                serializers.serialize('json', objects_lists)
            )
        ).hexdigest()

    def get_label(self):
        return force_text(self.get_control_code_class().label)
    get_label.short_description = _('Label')

    def render(self):
        return self.get_control_code_instance().get_image(order=self.order)

    def save(self, *args, **kwargs):
        if not self.order:
            last_order = ControlSheetCode.objects.filter(
                control_sheet=self.control_sheet
            ).aggregate(Max('order'))['order__max']
            if last_order is not None:
                self.order = last_order + 1
        super(ControlSheetCode, self).save(*args, **kwargs)
