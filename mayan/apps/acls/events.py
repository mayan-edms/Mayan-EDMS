from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(
    label=_('Access control lists'), name='acls'
)

event_acl_created = namespace.add_event_type(
    label=_('ACL created'), name='acl_created'
)
event_acl_edited = namespace.add_event_type(
    label=_('ACL edited'), name='acl_edited'
)
