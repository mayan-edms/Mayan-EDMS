from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from .classes import Event


def event_object_link(entry):
    return mark_safe('<a href="%(url)s">%(label)s</a>' % {
        'url': entry.target.get_absolute_url() if entry.target else '#',
        'label': entry.target}
    )


def event_type_link(entry):
    return mark_safe('<a href="%(url)s">%(label)s</a>' % {
        'url': reverse('events:events_by_verb', kwargs={'verb': entry.verb}),
        'label': Event.get_label(entry.verb)}
    )
