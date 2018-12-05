from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.events import EventTypeNamespace

namespace = EventTypeNamespace(
    name='document_comments', label=_('Document comments')
)

event_document_comment_create = namespace.add_event_type(
    name='create', label=_('Document comment created')
)
event_document_comment_delete = namespace.add_event_type(
    name='delete', label=_('Document comment deleted')
)
