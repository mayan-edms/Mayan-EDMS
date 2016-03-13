from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .managers import MessageOfTheDayManager


@python_2_unicode_compatible
class MessageOfTheDay(models.Model):
    label = models.CharField(max_length=32, verbose_name=_('Label'))
    message = models.TextField(verbose_name=_('Message'))
    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))
    start_datetime = models.DateTimeField(
        blank=True, null=True, verbose_name=_('Start date time')
    )
    end_datetime = models.DateTimeField(
        blank=True, null=True, verbose_name=_('End date time')
    )

    objects = MessageOfTheDayManager()

    class Meta:
        verbose_name = _('Message of the day')
        verbose_name_plural = _('Messages of the day')

    def __str__(self):
        return self.label
