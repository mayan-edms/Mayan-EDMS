from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(
    label=_('Smart settings'), name='smart_settings'
)

permission_settings_edit = namespace.add_permission(
    label=_('Edit settings'), name='permission_settings_edit'
)
permission_settings_view = namespace.add_permission(
    label=_('View settings'), name='permission_settings_view'
)
