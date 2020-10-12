from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(
    label=_('Document parsing'), name='document_parsing'
)

event_parsing_document_file_content_deleted = namespace.add_event_type(
    label=_('Document parsed content deleted'),
    name='document_content_deleted'
)
event_parsing_document_file_submit = namespace.add_event_type(
    label=_('Document file submitted for parsing'), name='version_submit'
)
event_parsing_document_file_finish = namespace.add_event_type(
    label=_('Document file parsing finished'), name='version_finish'
)
