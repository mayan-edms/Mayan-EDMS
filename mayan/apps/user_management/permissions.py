from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(
    label=_('User management'), name='user_management'
)

permission_group_create = namespace.add_permission(
    label=_('Create new groups'), name='group_create'
)
permission_group_delete = namespace.add_permission(
    label=_('Delete existing groups'), name='group_delete'
)
permission_group_edit = namespace.add_permission(
    label=_('Edit existing groups'), name='group_edit'
)
permission_group_view = namespace.add_permission(
    label=_('View existing groups'), name='group_view'
)
permission_user_create = namespace.add_permission(
    label=_('Create new users'), name='user_create'
)
permission_user_delete = namespace.add_permission(
    label=_('Delete existing users'), name='user_delete'
)
permission_user_edit = namespace.add_permission(
    label=_('Edit existing users'), name='user_edit'
)
permission_user_view = namespace.add_permission(
    label=_('View existing users'), name='user_view'
)
