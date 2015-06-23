from __future__ import unicode_literals

from ast import literal_eval
import logging

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .classes import BaseTransformation
from .managers import TransformationManager

logger = logging.getLogger(__name__)


def argument_validator(value):
    """
    Validates that the input evaluates correctly.
    """
    value = value.strip()
    try:
        literal_eval(value)
    except (ValueError, SyntaxError):
        raise ValidationError(_('Enter a valid value.'), code='invalid')


@python_2_unicode_compatible
class Transformation(models.Model):
    """
    Model that stores the transformation and transformation arguments
    for a given object
    """

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    order = models.PositiveIntegerField(default=0, blank=True, help_text=_('Order in which the transformations will be executed.'), null=True, verbose_name=_('Order'), db_index=True)
    name = models.CharField(choices=BaseTransformation.get_transformation_choices(), max_length=128, verbose_name=_('Name'))
    arguments = models.TextField(blank=True, help_text=_('Enter the arguments for the transformation as a Python dictionary. ie: {"degrees": 180}'), verbose_name=_('Arguments'), validators=[argument_validator])

    objects = TransformationManager()

    def __str__(self):
        return self.get_name_display()

    class Meta:
        ordering = ('order',)
        verbose_name = _('Transformation')
        verbose_name_plural = _('Transformations')
