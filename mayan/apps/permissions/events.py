from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(
    label=_('Permissions'), name='permissions'
)

event_role_created = namespace.add_event_type(
    label=_('Role created'), name='role_created'
)
event_role_edited = namespace.add_event_type(
    label=_('Role edited'), name='role_edited'
)
