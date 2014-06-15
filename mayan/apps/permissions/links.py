from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .permissions import (PERMISSION_ROLE_VIEW, PERMISSION_ROLE_EDIT,
    PERMISSION_ROLE_CREATE, PERMISSION_ROLE_DELETE,
    PERMISSION_PERMISSION_GRANT, PERMISSION_PERMISSION_REVOKE)

role_list = {'text': _(u'roles'), 'view': 'role_list', 'famfam': 'medal_gold_1', 'icon': 'medal_gold_1.png', 'permissions': [PERMISSION_ROLE_VIEW], 'children_view_regex': [r'^permission_', r'^role_']}
role_create = {'text': _(u'create new role'), 'view': 'role_create', 'famfam': 'medal_gold_add', 'permissions': [PERMISSION_ROLE_CREATE]}
role_edit = {'text': _(u'edit'), 'view': 'role_edit', 'args': 'object.id', 'famfam': 'medal_gold_1', 'permissions': [PERMISSION_ROLE_EDIT]}
role_members = {'text': _(u'members'), 'view': 'role_members', 'args': 'object.id', 'famfam': 'group_key', 'permissions': [PERMISSION_ROLE_EDIT]}
role_permissions = {'text': _(u'role permissions'), 'view': 'role_permissions', 'args': 'object.id', 'famfam': 'key_go', 'permissions': [PERMISSION_PERMISSION_GRANT, PERMISSION_PERMISSION_REVOKE]}
role_delete = {'text': _(u'delete'), 'view': 'role_delete', 'args': 'object.id', 'famfam': 'medal_gold_delete', 'permissions': [PERMISSION_ROLE_DELETE]}

permission_grant = {'text': _(u'grant'), 'view': 'permission_multiple_grant', 'famfam': 'key_add', 'permissions': [PERMISSION_PERMISSION_GRANT]}
permission_revoke = {'text': _(u'revoke'), 'view': 'permission_multiple_revoke', 'famfam': 'key_delete', 'permissions': [PERMISSION_PERMISSION_REVOKE]}
