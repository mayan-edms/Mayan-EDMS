from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from events import EventTypeNamespace

namespace = EventTypeNamespace(
    name='document_parsing', label=_('Document parsing')
)

event_parsing_document_version_submit = namespace.add_event_type(
    label=_('Document version submitted for parsing'), name='version_submit'
)
event_parsing_document_version_finish = namespace.add_event_type(
    label=_('Document version parsing finished'), name='version_finish'
)
