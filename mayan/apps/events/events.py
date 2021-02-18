from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(label=_('Events'), name='events')

event_events_exported = namespace.add_event_type(
    label=_('Events exported'), name='event_exported'
)
