from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from events import EventTypeNamespace

namespace = EventTypeNamespace(name='metadata', label=_('Metadata'))

event_metadata_type_created = namespace.add_event_type(
    name='metadata_type_created', label=_('Metadata type created')
)
event_metadata_type_edited = namespace.add_event_type(
    name='metadata_type_edited', label=_('Metadata type edited')
)
event_metadata_type_relationship = namespace.add_event_type(
    name='metadata_type_relationship', label=_(
        'Metadata type relationship updated'
    )
)
