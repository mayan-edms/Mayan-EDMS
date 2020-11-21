from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link
from mayan.apps.user_management.permissions import permission_group_edit

from .icons import (
    icon_group_roles, icon_role_create, icon_role_delete, icon_role_edit,
    icon_role_groups, icon_role_list, icon_role_permissions
)
from .permissions import (
    permission_role_create, permission_role_delete, permission_role_edit,
    permission_role_view
)

link_group_roles = Link(
    args='object.id', icon=icon_group_roles,
    permissions=(permission_group_edit,), text=_('Roles'),
    view='permissions:group_roles',
)

link_role_create = Link(
    icon=icon_role_create, permissions=(permission_role_create,),
    text=_('Create new role'), view='permissions:role_create'
)
link_role_delete = Link(
    args='object.id', icon=icon_role_delete,
    permissions=(permission_role_delete,), tags='dangerous',
    text=_('Delete'), view='permissions:role_delete',
)
link_role_edit = Link(
    args='object.id', icon=icon_role_edit,
    permissions=(permission_role_edit,), text=_('Edit'),
    view='permissions:role_edit',
)
link_role_list = Link(
    icon=icon_role_list, permissions=(permission_role_view,),
    text=_('Roles'), view='permissions:role_list'
)
link_role_groups = Link(
    args='object.id', icon=icon_role_groups,
    permissions=(permission_role_edit,), text=_('Groups'),
    view='permissions:role_groups',
)
link_role_permissions = Link(
    args='object.id', icon=icon_role_permissions,
    permissions=(permission_role_edit,),
    text=_('Role permissions'), view='permissions:role_permissions',
)
