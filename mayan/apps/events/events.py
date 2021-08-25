from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

from .literals import (
    EVENT_TYPE_NAMESPACE_NAME, EVENT_EVENTS_CLEARED_NAME,
    EVENT_EVENTS_EXPORTED_NAME
)

namespace = EventTypeNamespace(
    label=_('Events'), name=EVENT_TYPE_NAMESPACE_NAME
)

event_events_cleared = namespace.add_event_type(
    label=_('Events cleared'), name=EVENT_EVENTS_CLEARED_NAME
)
event_events_exported = namespace.add_event_type(
    label=_('Events exported'), name=EVENT_EVENTS_EXPORTED_NAME
)
