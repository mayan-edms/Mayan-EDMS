from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from . import PermissionNamespace

namespace = PermissionNamespace(name='permissions', label=_('Permissions'))

permission_role_view = namespace.add_permission(
    name='role_view', label=_('View roles')
)
permission_role_edit = namespace.add_permission(
    name='role_edit', label=_('Edit roles')
)
permission_role_create = namespace.add_permission(
    name='role_create', label=_('Create roles')
)
permission_role_delete = namespace.add_permission(
    name='role_delete', label=_('Delete roles')
)
