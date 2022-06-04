import hashlib
import io
import logging

import cairosvg
from furl import furl
from PIL import Image

from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.utils.encoding import force_bytes
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.validators import validate_internal_name
from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.documents.models.document_models import Document
from mayan.apps.events.classes import (
    EventManagerMethodAfter, EventManagerSave
)
from mayan.apps.events.decorators import method_event
from mayan.apps.file_caching.models import Cache, CachePartitionFile
from mayan.apps.templating.classes import Template

from .events import (
    event_signature_capture_created, event_signature_capture_deleted,
    event_signature_capture_edited,
)
from .literals import STORAGE_NAME_SIGNATURE_CAPTURES_CACHE
from .managers import ValidSignatureCaptureManager

logger = logging.getLogger(name=__name__)


class SignatureCapture(ExtraDataModelMixin, models.Model):
    document = models.ForeignKey(
        on_delete=models.CASCADE, related_name='signature_captures',
        to=Document, verbose_name=_('Document')
    )
    data = models.TextField(
        blank=True, help_text=_(
            'Data representing the handwritten signature.'
        ), verbose_name=_('Signature capture data')
    )
    svg = models.TextField(
        blank=True, help_text=_(
            'Vector representation of the handwritten signature.'
        ), verbose_name=_('SVG signature capture data')
    )
    text = models.CharField(
        help_text=_('Print version of the captured signature.'),
        max_length=224, verbose_name=_('Text')
    )
    user = models.ForeignKey(
        on_delete=models.CASCADE, related_name='signature_captures',
        to=settings.AUTH_USER_MODEL, verbose_name=_('User')
    )
    date_time_created = models.DateTimeField(
        auto_now_add=True, db_index=True,
        verbose_name=_('Date and time created')
    )
    date_time_edited = models.DateTimeField(
        auto_now=True, db_index=True,
        verbose_name=_('Date and time edited')
    )
    internal_name = models.CharField(
        db_index=True, help_text=_(
            'This value will be used when referencing this signature '
            'capture in relationship to the document. Can only contain '
            'letters, numbers, and underscores.'
        ), max_length=255, validators=[validate_internal_name],
        verbose_name=_('Internal name')
    )

    objects = models.Manager()
    valid = ValidSignatureCaptureManager()

    class Meta:
        ordering = ('-date_time_created',)
        unique_together = ('document', 'internal_name')
        verbose_name = _('Signature capture')
        verbose_name_plural = _('Signature captures')

    def __str__(self):
        return '{} - {}'.format(self.text, self.get_date_time_created())

    @cached_property
    def cache(self):
        return Cache.objects.get(
            defined_storage_name=STORAGE_NAME_SIGNATURE_CAPTURES_CACHE
        )

    @cached_property
    def cache_partition(self):
        partition, created = self.cache.partitions.get_or_create(
            name='{}'.format(self.pk)
        )
        return partition

    @method_event(
        action_object='self',
        event=event_signature_capture_deleted,
        event_manager_class=EventManagerMethodAfter,
        target='document'
    )
    def delete(self, *args, **kwargs):
        self.cache_partition.delete()
        return super().delete(*args, **kwargs)

    def generate_image(
        self, maximum_layer_order=None, transformation_instance_list=None,
        user=None
    ):
        # The parameters 'maximum_layer_order',
        # `transformation_instance_list`, `user` are not used, but added
        # to retain interface compatibility.
        cache_filename = '{}'.format(self.get_hash())

        try:
            self.cache_partition.get_file(filename=cache_filename)
        except CachePartitionFile.DoesNotExist:
            logger.debug(
                'signature capture cache file "%s" not found', cache_filename
            )

            image = self.get_image()
            with io.BytesIO() as image_buffer:
                image.save(image_buffer, format='PNG')

                with self.cache_partition.create_file(filename=cache_filename) as file_object:
                    file_object.write(image_buffer.getvalue())
        else:
            logger.debug(
                'signature_capture cache file "%s" found', cache_filename
            )

        return cache_filename

    def get_absolute_url(self):
        return reverse(
            viewname='signature_captures:signature_capture_detail', kwargs={
                'signature_capture_id': self.pk
            }
        )

    def get_api_image_url(self, *args, **kwargs):
        final_url = furl()
        final_url.args = kwargs
        final_url.path = reverse(
            viewname='rest_api:signature_capture-image',
            kwargs={
                'document_id': self.document.pk,
                'signature_capture_id': self.pk
            }
        )
        final_url.args['_hash'] = self.get_hash()

        return final_url.tostr()

    def get_date_time_created(self):
        return Template(
            template_string='{{ instance.date_time_created }}'
        ).render(
            context={'instance': self}
        )
    get_date_time_created.short_description = _('Creation date and time')

    def get_hash(self):
        return hashlib.sha256(force_bytes(self.svg)).hexdigest()

    def get_image(self):
        stream = io.BytesIO()
        cairosvg.svg2png(url=self.svg, write_to=stream)
        image = Image.open(stream)

        return image

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'actor': 'user',
            'action_object': 'document',
            'event': event_signature_capture_created,
            'target': 'self'
        },
        edited={
            'action_object': 'document',
            'event': event_signature_capture_edited,
            'target': 'self'
        }
    )
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
