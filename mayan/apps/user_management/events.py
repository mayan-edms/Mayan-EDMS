from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(
    label=_('User management'), name='user_management'
)

event_group_created = namespace.add_event_type(
    label=_('Group created'), name='group_created'
)
event_group_edited = namespace.add_event_type(
    label=_('Group edited'), name='group_edited'
)

event_user_created = namespace.add_event_type(
    label=_('User created'), name='user_created'
)
event_user_edited = namespace.add_event_type(
    label=_('User edited'), name='user_edited'
)
event_user_logged_in = namespace.add_event_type(
    label=_('User logged in'), name='user_logged_in'
)
event_user_logged_out = namespace.add_event_type(
    label=_('User logged out'), name='user_logged_out'
)
