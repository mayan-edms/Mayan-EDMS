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
link_role_create = {'text': _('Create new role'), 'view': 'permissions:role_create', 'famfam': 'medal_gold_add', 'permissions': [PERMISSION_ROLE_CREATE]}
link_role_delete = {'text': _('Delete'), 'view': 'permissions:role_delete', 'args': 'object.id', 'famfam': 'medal_gold_delete', 'permissions': [PERMISSION_ROLE_DELETE]}
link_role_edit = {'text': _('Edit'), 'view': 'permissions:role_edit', 'args': 'object.id', 'famfam': 'medal_gold_1', 'permissions': [PERMISSION_ROLE_EDIT]}
link_role_list = Link(icon='fa fa-child', permissions=[PERMISSION_ROLE_VIEW], text=_('Roles'), view='permissions:role_list')
link_role_members = {'text': _('Members'), 'view': 'permissions:role_members', 'args': 'object.id', 'famfam': 'group_key', 'permissions': [PERMISSION_ROLE_EDIT]}
link_role_permissions = {'text': _('Role permissions'), 'view': 'permissions:role_permissions', 'args': 'object.id', 'famfam': 'key_go', 'permissions': [PERMISSION_PERMISSION_GRANT, PERMISSION_PERMISSION_REVOKE]}
