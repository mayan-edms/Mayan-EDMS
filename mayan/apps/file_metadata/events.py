from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.events import EventTypeNamespace

namespace = EventTypeNamespace(
    label=_('File metadata'), name='file_metadata'
)

event_file_metadata_document_version_submit = namespace.add_event_type(
    label=_('Document version submitted for file metadata processing'),
    name='document_version_submit'
)
event_file_metadata_document_version_finish = namespace.add_event_type(
    label=_('Document version file metadata processing finished'),
    name='document_version_finish'
)
