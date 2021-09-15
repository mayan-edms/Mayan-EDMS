from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(label=_('Documents'), name='documents')

# Document

event_document_created = namespace.add_event_type(
    label=_('Document created'), name='document_create'
)
event_document_edited = namespace.add_event_type(
    label=_('Document edited'), name='document_edit'
)
event_document_viewed = namespace.add_event_type(
    label=_('Document viewed'), name='document_view'
)

# Document File

event_document_file_created = namespace.add_event_type(
    label=_('Document file created'), name='document_file_created'
)
event_document_file_deleted = namespace.add_event_type(
    label=_('Document file deleted'), name='document_file_deleted'
)
event_document_file_downloaded = namespace.add_event_type(
    label=_('Document file downloaded'), name='document_file_downloaded'
)
event_document_file_edited = namespace.add_event_type(
    label=_('Document file edited'), name='document_file_edited'
)

# Document type

event_document_type_created = namespace.add_event_type(
    label=_('Document type created'), name='document_type_created'
)
event_document_type_edited = namespace.add_event_type(
    label=_('Document type edited'), name='document_type_edit'
)
event_document_type_quick_label_created = namespace.add_event_type(
    label=_('Document type quick label created'),
    name='document_type_quick_label_created'
)
event_document_type_quick_label_deleted = namespace.add_event_type(
    label=_('Document type quick label deleted'),
    name='document_type_quick_label_deleted'
)
event_document_type_quick_label_edited = namespace.add_event_type(
    label=_('Document type quick label edited'),
    name='document_type_quick_label_edited'
)
# The type of an existing document is changed to another type
event_document_type_changed = namespace.add_event_type(
    label=_('Document type changed'), name='document_type_change'
)

# Document version

event_document_version_created = namespace.add_event_type(
    label=_('Document version created'), name='document_version_created'
)
event_document_version_deleted = namespace.add_event_type(
    label=_('Document version deleted'), name='document_version_deleted'
)
event_document_version_edited = namespace.add_event_type(
    label=_('Document version edited'), name='document_version_edited'
)
event_document_version_exported = namespace.add_event_type(
    label=_('Document version exported'), name='document_version_exported'
)

# Document version page

event_document_version_page_created = namespace.add_event_type(
    label=_('Document version page created'),
    name='document_version_page_created'
)
event_document_version_page_deleted = namespace.add_event_type(
    label=_('Document version page deleted'),
    name='document_version_page_deleted'
)
event_document_version_page_edited = namespace.add_event_type(
    label=_('Document version page edited'),
    name='document_version_page_edited'
)

# Trashed document

event_document_trashed = namespace.add_event_type(
    label=_('Document trashed'), name='document_trashed'
)
event_trashed_document_deleted = namespace.add_event_type(
    label=_('Trashed document deleted'), name='trashed_document_deleted'
)
event_trashed_document_restored = namespace.add_event_type(
    label=_('Trashed document restored'), name='trashed_document_restored'
)

# Historic events

event_document_download = namespace.add_event_type(
    label=_('Document downloaded (historic)'), name='document_download'
)
event_document_file_pre_save = namespace.add_event_type(
    label=_('Document file created (historic)'),
    name='document_file_pre_save'
)
event_document_version_revert = namespace.add_event_type(
    label=_('Document version reverted (historic)'),
    name='document_version_revert'
)
event_document_version_new = namespace.add_event_type(
    label=_('Document version uploaded (historic)'),
    name='document_new_version'
)
