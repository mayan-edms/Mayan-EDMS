from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(
    label=_('File metadata'), name='file_metadata'
)

event_file_metadata_document_file_submit = namespace.add_event_type(
    label=_('Document file submitted for file metadata processing'),
    name='document_version_submit'
)
event_file_metadata_document_file_finish = namespace.add_event_type(
    label=_('Document file file metadata processing finished'),
    name='document_version_finish'
)
