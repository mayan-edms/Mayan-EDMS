from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(label=_('Checkouts'), name='checkouts')

event_document_auto_check_in = namespace.add_event_type(
    label=_('Document automatically checked in'),
    name='document_auto_check_in'
)
event_document_check_in = namespace.add_event_type(
    label=_('Document checked in'), name='document_check_in'
)
event_document_check_out = namespace.add_event_type(
    label=_('Document checked out'), name='document_check_out'
)
event_document_forceful_check_in = namespace.add_event_type(
    label=_('Document forcefully checked in'),
    name='document_forceful_check_in'
)
