from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(label=_('Converter'), name='converter')

event_asset_created = namespace.add_event_type(
    label=_('Asset created'), name='asset_created'
)
event_asset_edited = namespace.add_event_type(
    label=_('Asset edited'), name='asset_edited'
)
