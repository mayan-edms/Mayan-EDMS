from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from actstream.models import Action

from common.utils import encapsulate
from navigation.api import register_model_list_columns

from .classes import Event
from .widgets import event_type_link


@python_2_unicode_compatible
class EventType(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name=_('Name'))

    def __str__(self):
        return unicode(Event.get_label(self.name))

    class Meta:
        verbose_name = _('Event type')
        verbose_name_plural = _('Event types')


register_model_list_columns(Action, [
    {
        'name': _('Timestamp'),
        'attribute': 'timestamp'
    },
    {
        'name': _('Actor'),
        'attribute': 'actor',
    },
    {
        'name': _('Verb'),
        'attribute': encapsulate(lambda entry: event_type_link(entry))
    },
])
