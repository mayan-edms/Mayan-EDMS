from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import (PERMISSION_ROLE_VIEW, PERMISSION_ROLE_EDIT,
    PERMISSION_ROLE_CREATE, PERMISSION_ROLE_DELETE,
    PERMISSION_PERMISSION_GRANT, PERMISSION_PERMISSION_REVOKE)
from .icons import (icon_role, icon_role_add, icon_role_delete, icon_role_edit,
    icon_permissions, icon_permission_grant, icon_permission_revoke, icon_role_members)

role_list = Link(text=_(u'roles'), view='role_list', icon=icon_role, permissions=[PERMISSION_ROLE_VIEW])#, 'children_view_regex': [r'^permission_', r'^role_'])
role_create = Link(text=_(u'create new role'), view='role_create', icon=icon_role_add, permissions=[PERMISSION_ROLE_CREATE])
role_edit = Link(text=_(u'edit'), view='role_edit', args='object.id', icon=icon_role_edit, permissions=[PERMISSION_ROLE_EDIT])
role_members = Link(text=_(u'members'), view='role_members', args='object.id', icon=icon_role_members, permissions=[PERMISSION_ROLE_EDIT])
role_permissions = Link(text=_(u'role permissions'), view='role_permissions', args='object.id', icon=icon_permissions, permissions=[PERMISSION_PERMISSION_GRANT, PERMISSION_PERMISSION_REVOKE])
role_delete = Link(text=_(u'delete'), view='role_delete', args='object.id', icon=icon_role_delete, permissions=[PERMISSION_ROLE_DELETE])

permission_grant = Link(text=_(u'grant'), view='permission_multiple_grant', icon=icon_permission_grant, permissions=[PERMISSION_PERMISSION_GRANT])
permission_revoke = Link(text=_(u'revoke'), view='permission_multiple_revoke', icon=icon_permission_revoke, permissions=[PERMISSION_PERMISSION_REVOKE])
