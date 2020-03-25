from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Statistics'), name='statistics')

permission_statistics_view = namespace.add_permission(
    label=_('View statistics'), name='statistics_view'
)
