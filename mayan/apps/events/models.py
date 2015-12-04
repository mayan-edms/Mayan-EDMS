from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .classes import Event


@python_2_unicode_compatible
class EventType(models.Model):
    name = models.CharField(
        max_length=64, unique=True, verbose_name=_('Name')
    )

    def __str__(self):
        return unicode(Event.get_label(self.name))

    class Meta:
        verbose_name = _('Event type')
        verbose_name_plural = _('Event types')
