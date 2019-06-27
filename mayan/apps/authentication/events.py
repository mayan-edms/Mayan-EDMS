from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(
    label=_('Authentication'), name='authentication'
)

event_user_authentication_error = namespace.add_event_type(
    label=_('User authentication error'), name='user_authentication_error'
)
event_user_password_reset_started = namespace.add_event_type(
    label=_('User password reset started'), name='user_password_reset_started'
)
event_user_password_reset_complete = namespace.add_event_type(
    label=_('User password reset complete'), name='user_password_reset_complete'
)
