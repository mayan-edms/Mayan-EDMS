from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(label=_('Key management'), name='django_gpg')

event_key_created = namespace.add_event_type(
    label=_('Key created'),
    name='key_created'
)
event_key_downloaded = namespace.add_event_type(
    label=_('Key downloaded'), name='key_downloaded'
)
