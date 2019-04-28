from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(
    label=_('Document indexing'), name='document_indexing'
)

event_index_template_created = namespace.add_event_type(
    label=_('Index created'), name='index_created'
)
event_index_template_edited = namespace.add_event_type(
    label=_('Index edited'), name='index_edited'
)
