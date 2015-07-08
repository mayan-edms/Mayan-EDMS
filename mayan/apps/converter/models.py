from __future__ import unicode_literals

import logging

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .classes import BaseTransformation
from .managers import TransformationManager
from .validators import YAMLValidator

logger = logging.getLogger(__name__)


def validators():
    return [YAMLValidator()]


@python_2_unicode_compatible
class Transformation(models.Model):
    """
    Model that stores the transformation and transformation arguments
    for a given object
    """

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    order = models.PositiveIntegerField(blank=True, db_index=True, default=0, help_text=_('Order in which the transformations will be executed.'), null=True, verbose_name=_('Order'))
    name = models.CharField(choices=BaseTransformation.get_transformation_choices(), max_length=128, verbose_name=_('Name'))
    arguments = models.TextField(blank=True, help_text=_('Enter the arguments for the transformation as a YAML dictionary. ie: {"degrees": 180}'), validators=validators, verbose_name=_('Arguments'))

    objects = TransformationManager()

    def __str__(self):
        return self.get_name_display()

    class Meta:
        ordering = ('order',)
        verbose_name = _('Transformation')
        verbose_name_plural = _('Transformations')
