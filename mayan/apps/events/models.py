from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from .managers import EventTypeManager


@python_2_unicode_compatible
class EventType(models.Model):
    _labels = {}

    name = models.CharField(max_length=64, unique=True, verbose_name=_('Name'))

    objects = EventTypeManager()

    def __str__(self):
        return unicode(self.get_label())

    def get_label(self):
        try:
            return self.__class__._labels[self.name]
        except KeyError:
            return _('Unknown or obsolete event type: {0}'.format(self.name))

    #@models.permalink
    #def get_absolute_url(self):
    #    return ('history_type_list', [self.pk])

    class Meta:
        verbose_name = _('Event type')
        verbose_name_plural = _('Event types')
