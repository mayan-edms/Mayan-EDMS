from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from events import EventTypeNamespace

namespace = EventTypeNamespace(name='ocr', label=_('OCR'))

event_ocr_document_version_submit = namespace.add_event_type(
    label=_('Document version submitted for OCR'),
    name='document_version_submit'
)
event_ocr_document_version_finish = namespace.add_event_type(
    label=_('Document version OCR finished'),
    name='document_version_finish'
)
