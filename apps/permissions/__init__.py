from __future__ import absolute_import


from django.utils.translation import ugettext_lazy as _

from navigation.api import bind_links, register_multi_item_links

from .links import (role_list, role_create, role_edit, role_members,
    role_permissions, role_delete, permission_grant, permission_revoke)
from .models import Role
from .exceptions import PermissionDenied

bind_links([Role], [role_edit, role_delete, role_permissions, role_members])
bind_links([Role, 'role_list', 'role_create'], [role_list, role_create], menu_name='secondary_menu')
register_multi_item_links(['role_permissions'], [permission_grant, permission_revoke])

# TODO: eliminate this
permission_views = ['role_list', 'role_create', 'role_edit', 'role_members', 'role_permissions', 'role_delete']
