from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import (
    PERMISSION_PERMISSION_GRANT, PERMISSION_PERMISSION_REVOKE,
    PERMISSION_ROLE_CREATE, PERMISSION_ROLE_DELETE, PERMISSION_ROLE_EDIT,
    PERMISSION_ROLE_VIEW
)

link_permission_grant = Link(permissions=[PERMISSION_PERMISSION_GRANT], text=_('Grant'), view='permissions:permission_multiple_grant')
link_permission_revoke = Link(permissions=[PERMISSION_PERMISSION_REVOKE], text=_('Revoke'), view='permissions:permission_multiple_revoke')
link_role_create = Link(permissions=[PERMISSION_ROLE_CREATE], text=_('Create new role'), view='permissions:role_create')
link_role_delete = Link(permissions=[PERMISSION_ROLE_DELETE], tags='dangerous', text=_('Delete'), view='permissions:role_delete', args='object.id')
link_role_edit = Link(permissions=[PERMISSION_ROLE_EDIT], text=_('Edit'), view='permissions:role_edit', args='object.id')
link_role_list = Link(icon='fa fa-user-secret', permissions=[PERMISSION_ROLE_VIEW], text=_('Roles'), view='permissions:role_list')
link_role_members = Link(permissions=[PERMISSION_ROLE_EDIT], text=_('Members'), view='permissions:role_members', args='object.id')
link_role_permissions = Link(permissions=[PERMISSION_PERMISSION_GRANT, PERMISSION_PERMISSION_REVOKE], text=_('Role permissions'), view='permissions:role_permissions', args='object.id')
