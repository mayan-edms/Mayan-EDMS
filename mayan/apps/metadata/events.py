from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.events import EventTypeNamespace

namespace = EventTypeNamespace(name='metadata', label=_('Metadata'))

event_document_metadata_added = namespace.add_event_type(
    name='document_metadata_added', label=_(
        'Document metadata added'
    )
)
event_document_metadata_edited = namespace.add_event_type(
    name='document_metadata_edited', label=_(
        'Document metadata edited'
    )
)
event_document_metadata_removed = namespace.add_event_type(
    name='document_metadata_removed', label=_(
        'Document metadata removed'
    )
)
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
