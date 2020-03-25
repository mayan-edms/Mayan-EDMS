from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(
    label=_('Authentication'), name='authentication'
)

permission_users_impersonate = namespace.add_permission(
    label=_('Impersonate users'), name='users_impersonate'
)
