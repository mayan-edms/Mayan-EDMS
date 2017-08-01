from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from events import EventTypeNamespace

namespace = EventTypeNamespace(name='documents', label=_('Documents'))

event_document_create = namespace.add_event_type(
    name='document_create', label=_('Document created')
)
event_document_download = namespace.add_event_type(
    name='document_download', label=_('Document downloaded')
)
event_document_properties_edit = namespace.add_event_type(
    name='document_edit', label=_('Document properties edited')
)
event_document_type_change = namespace.add_event_type(
    name='document_type_change', label=_('Document type changed')
)
event_document_new_version = namespace.add_event_type(
    name='document_new_version', label=_('New version uploaded')
)
event_document_version_revert = namespace.add_event_type(
    name='document_version_revert', label=_('Document version reverted')
)
event_document_view = namespace.add_event_type(
    name='document_view', label=_('Document viewed')
)
