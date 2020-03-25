from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(label=_('OCR'), name='ocr')

event_ocr_document_content_deleted = namespace.add_event_type(
    label=_('Document OCR content deleted'),
    name='document_content_deleted'
)
event_ocr_document_version_submit = namespace.add_event_type(
    label=_('Document version submitted for OCR'),
    name='document_version_submit'
)
event_ocr_document_version_finish = namespace.add_event_type(
    label=_('Document version OCR finished'),
    name='document_version_finish'
)
