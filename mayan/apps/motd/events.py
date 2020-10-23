from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(label=_('Messages'), name='motd')

event_message_created = namespace.add_event_type(
    label=_('Message created'), name='message_created'
)
event_message_edited = namespace.add_event_type(
    label=_('Message edited'), name='message_edited'
)
