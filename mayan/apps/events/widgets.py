from __future__ import unicode_literals

from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from .classes import EventType


def event_object_link(entry, attribute='target'):
    label = ''
    url = '#'
    obj_type = ''

    obj = getattr(entry, attribute)

    if obj:
        obj_type = '{}: '.format(obj._meta.verbose_name)
        if hasattr(obj, 'get_absolute_url'):
            url = obj.get_absolute_url()
        label = force_text(obj)

    return mark_safe(
        '<a href="%(url)s">%(obj_type)s%(label)s</a>' % {
            'url': url, 'label': label, 'obj_type': obj_type
        }
    )


def event_type_link(entry):
    return mark_safe(
        '<a href="%(url)s">%(label)s</a>' % {
            'url': reverse('events:events_by_verb', kwargs={'verb': entry.verb}),
            'label': EventType.get(name=entry.verb)
        }
    )


def event_user_link(entry):
    if entry.actor == entry.target:
        return _('System')
    else:
        return mark_safe(
            '<a href="%(url)s">%(label)s</a>' % {
                'url': reverse('events:user_events', kwargs={'pk': entry.actor.pk}),
                'label': entry.actor
            }
        )
