from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(label=_('Appearance'), name='appearance')

event_theme_created = namespace.add_event_type(
    label=_('Theme created'), name='theme_created'
)
event_theme_edited = namespace.add_event_type(
    label=_('Theme edited'), name='theme_edited'
)
