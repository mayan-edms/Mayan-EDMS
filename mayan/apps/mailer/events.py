from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(label=_('Mailing'), name='mailing')

event_email_sent = namespace.add_event_type(
    label=_('Email sent'), name='email_send'
)
event_profile_created = namespace.add_event_type(
    label=_('Mailing profile created'), name='profile_created'
)
event_profile_edited = namespace.add_event_type(
    label=_('Mailing profile edited'), name='profile_edited'
)
