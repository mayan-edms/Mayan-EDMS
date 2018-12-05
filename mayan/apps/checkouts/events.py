from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.events import EventTypeNamespace

namespace = EventTypeNamespace(name='checkouts', label=_('Checkouts'))

event_document_auto_check_in = namespace.add_event_type(
    name='document_auto_check_in',
    label=_('Document automatically checked in')
)
event_document_check_in = namespace.add_event_type(
    name='document_check_in', label=_('Document checked in')
)
event_document_check_out = namespace.add_event_type(
    name='document_check_out', label=_('Document checked out')
)
event_document_forceful_check_in = namespace.add_event_type(
    name='document_forceful_check_in',
    label=_('Document forcefully checked in')
)
