from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.events import EventTypeNamespace

namespace = EventTypeNamespace(name='documents', label=_('Documents'))

event_document_create = namespace.add_event_type(
    name='document_create', label=_('Document created')
)
event_document_download = namespace.add_event_type(
    name='document_download', label=_('Document downloaded')
)
event_document_new_version = namespace.add_event_type(
    name='document_new_version', label=_('New version uploaded')
)
event_document_properties_edit = namespace.add_event_type(
    name='document_edit', label=_('Document properties edited')
)
# The type of an existing document is changed to another type
event_document_type_change = namespace.add_event_type(
    name='document_type_change', label=_('Document type changed')
)
# A document type is created
event_document_type_created = namespace.add_event_type(
    name='document_type_created', label=_('Document type created')
)
# An existing document type is modified
event_document_type_edited = namespace.add_event_type(
    name='document_type_edit', label=_('Document type edited')
)
event_document_version_revert = namespace.add_event_type(
    name='document_version_revert', label=_('Document version reverted')
)
event_document_view = namespace.add_event_type(
    name='document_view', label=_('Document viewed')
)
