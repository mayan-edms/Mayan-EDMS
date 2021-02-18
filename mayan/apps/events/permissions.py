from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Events'), name='events')

permission_events_export = namespace.add_permission(
    label=_('Export the events of an object'), name='events_export'
)
permission_events_view = namespace.add_permission(
    label=_('Access the events of an object'), name='events_view'
)
