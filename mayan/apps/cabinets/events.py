from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(label=_('Cabinets'), name='cabinets')


event_cabinet_created = namespace.add_event_type(
    label=_('Cabinet created'), name='cabinet_created'
)
event_cabinet_edited = namespace.add_event_type(
    label=_('Cabinet edited'), name='cabinet_edited'
)
event_cabinet_add_document = namespace.add_event_type(
    label=_('Document added to cabinet'), name='add_document'
)
event_cabinet_remove_document = namespace.add_event_type(
    label=_('Document removed from cabinet'), name='remove_document'
)
