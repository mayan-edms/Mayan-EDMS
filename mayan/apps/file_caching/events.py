from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(
    label=_('File caching'), name='file_caching'
)

event_cache_created = namespace.add_event_type(
    label=_('Cache created'), name='cache_created'
)
event_cache_edited = namespace.add_event_type(
    label=_('Cache edited'), name='cache_edited'
)
event_cache_purged = namespace.add_event_type(
    label=_('Cache purged'), name='cache_purged'
)
