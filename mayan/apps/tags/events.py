from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from events import EventTypeNamespace

namespace = EventTypeNamespace(name='tags', label=_('Tags'))

event_tag_attach = namespace.add_event_type(
    label=_('Tag attached to document'), name='attach'
)
event_tag_created = namespace.add_event_type(
    label=_('Tag created'), name='tag_created'
)
event_tag_edited = namespace.add_event_type(
    label=_('Tag edited'), name='tag_edited'
)
event_tag_remove = namespace.add_event_type(
    label=_('Tag removed from document'), name='remove'
)
