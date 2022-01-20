from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(label=_('Locales'), name='locales')

event_user_locale_profile_edited = namespace.add_event_type(
    label=_('User locale profile edited'), name='user_locale_profile_edited'
)
