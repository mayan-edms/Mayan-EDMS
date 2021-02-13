from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(label=_('Announcements'), name='announcement')

event_announcement_created = namespace.add_event_type(
    label=_('Announcement created'), name='announcement_created'
)
event_announcement_edited = namespace.add_event_type(
    label=_('Announcement edited'), name='announcement_edited'
)
