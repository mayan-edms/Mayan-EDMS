from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(label=_('Documents'), name='documents')

# Document

event_document_create = namespace.add_event_type(
    label=_('Document created'), name='document_create'
)
event_document_properties_edit = namespace.add_event_type(
    label=_('Document properties edited'), name='document_edit'
)
event_document_viewed = namespace.add_event_type(
    label=_('Document viewed'), name='document_view'
)

# Document File

event_document_file_deleted = namespace.add_event_type(
    label=_('Document file deleted'), name='document_file_deleted'
)
event_document_file_downloaded = namespace.add_event_type(
    label=_('Document file downloaded'), name='document_file_downloaded'
)
event_document_file_new = namespace.add_event_type(
    label=_('Document file uploaded'), name='document_file_new'
)
event_document_file_pre_save = namespace.add_event_type(
    label=_('Document file created'), name='document_file_pre_save'
)

# Document type

event_document_type_created = namespace.add_event_type(
    label=_('Document type created'), name='document_type_created'
)
event_document_type_edited = namespace.add_event_type(
    label=_('Document type edited'), name='document_type_edit'
)
# The type of an existing document is changed to another type
event_document_type_changed = namespace.add_event_type(
    label=_('Document type changed'), name='document_type_change'
)

# Document Version

event_document_version_created = namespace.add_event_type(
    label=_('Document version created'), name='document_version_created'
)
event_document_version_deleted = namespace.add_event_type(
    label=_('Document version deleted'), name='document_version_deleted'
)
event_document_version_edited = namespace.add_event_type(
    label=_('Document version edited'), name='document_version_edited'
)

# Trashed document

event_document_trashed = namespace.add_event_type(
    label=_('Document trashed'), name='document_trashed'
)

# Historic events

event_document_download = namespace.add_event_type(
    label=_('Document downloaded'), name='document_download'
)
event_document_version_revert = namespace.add_event_type(
    label=_('Document version revert'), name='document_version_revert'
)
event_document_version_new = namespace.add_event_type(
    label=_('Document version uploaded'), name='document_new_version'
)
