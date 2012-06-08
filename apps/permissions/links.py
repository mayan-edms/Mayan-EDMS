from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import Link

from .permissions import (PERMISSION_ROLE_VIEW, PERMISSION_ROLE_EDIT,
    PERMISSION_ROLE_CREATE, PERMISSION_ROLE_DELETE,
    PERMISSION_PERMISSION_GRANT, PERMISSION_PERMISSION_REVOKE)

role_list = Link(text=_(u'roles'), view='role_list', sprite='medal_gold_1', icon='medal_gold_1.png', permissions=[PERMISSION_ROLE_VIEW])#, 'children_view_regex': [r'^permission_', r'^role_'])
role_create = Link(text=_(u'create new role'), view='role_create', sprite='medal_gold_add', permissions=[PERMISSION_ROLE_CREATE])
role_edit = Link(text=_(u'edit'), view='role_edit', args='object.id', sprite='medal_gold_1', permissions=[PERMISSION_ROLE_EDIT])
role_members = Link(text=_(u'members'), view='role_members', args='object.id', sprite='group_key', permissions=[PERMISSION_ROLE_EDIT])
role_permissions = Link(text=_(u'role permissions'), view='role_permissions', args='object.id', sprite='key_go', permissions=[PERMISSION_PERMISSION_GRANT, PERMISSION_PERMISSION_REVOKE])
role_delete = Link(text=_(u'delete'), view='role_delete', args='object.id', sprite='medal_gold_delete', permissions=[PERMISSION_ROLE_DELETE])

permission_grant = Link(text=_(u'grant'), view='permission_multiple_grant', sprite='key_add', permissions=[PERMISSION_PERMISSION_GRANT])
permission_revoke = Link(text=_(u'revoke'), view='permission_multiple_revoke', sprite='key_delete', permissions=[PERMISSION_PERMISSION_REVOKE])
