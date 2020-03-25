from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(
    label=_('Quotas'), name='quotas'
)

event_quota_created = namespace.add_event_type(
    label=_('Quota created'), name='quota_created'
)
event_quota_edited = namespace.add_event_type(
    label=_('Quota edited'), name='quota_edited'
)
