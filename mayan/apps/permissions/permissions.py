from django.utils.translation import ugettext_lazy as _

from . import PermissionNamespace

namespace = PermissionNamespace(label=_('Permissions'), name='permissions')

permission_role_create = namespace.add_permission(
    label=_('Create roles'), name='role_create'
)
permission_role_delete = namespace.add_permission(
    label=_('Delete roles'), name='role_delete'
)
permission_role_edit = namespace.add_permission(
    label=_('Edit roles'), name='role_edit'
)
permission_role_view = namespace.add_permission(
    label=_('View roles'), name='role_view'
)
