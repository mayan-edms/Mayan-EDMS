from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.events import EventTypeNamespace

namespace = EventTypeNamespace(name='cabinets', label=_('Cabinets'))

event_cabinets_add_document = namespace.add_event_type(
    label=_('Document added to cabinet'), name='add_document'
)
event_cabinets_remove_document = namespace.add_event_type(
    label=_('Document removed from cabinet'), name='remove_document'
)
