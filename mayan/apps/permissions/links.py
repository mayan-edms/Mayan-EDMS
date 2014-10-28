from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .permissions import (PERMISSION_PERMISSION_GRANT,
                          PERMISSION_PERMISSION_REVOKE, PERMISSION_ROLE_CREATE,
                          PERMISSION_ROLE_DELETE, PERMISSION_ROLE_EDIT,
                          PERMISSION_ROLE_VIEW)

permission_grant = {'text': _(u'Grant'), 'view': 'permissions:permission_multiple_grant', 'famfam': 'key_add', 'permissions': [PERMISSION_PERMISSION_GRANT]}
permission_revoke = {'text': _(u'Revoke'), 'view': 'permissions:permission_multiple_revoke', 'famfam': 'key_delete', 'permissions': [PERMISSION_PERMISSION_REVOKE]}

role_create = {'text': _(u'Create new role'), 'view': 'permissions:role_create', 'famfam': 'medal_gold_add', 'permissions': [PERMISSION_ROLE_CREATE]}
role_delete = {'text': _(u'Delete'), 'view': 'permissions:role_delete', 'args': 'object.id', 'famfam': 'medal_gold_delete', 'permissions': [PERMISSION_ROLE_DELETE]}
role_edit = {'text': _(u'Edit'), 'view': 'permissions:role_edit', 'args': 'object.id', 'famfam': 'medal_gold_1', 'permissions': [PERMISSION_ROLE_EDIT]}
role_list = {'text': _(u'Roles'), 'view': 'permissions:role_list', 'famfam': 'medal_gold_1', 'icon': 'medal_gold_red.png', 'permissions': [PERMISSION_ROLE_VIEW]}
role_members = {'text': _(u'Members'), 'view': 'permissions:role_members', 'args': 'object.id', 'famfam': 'group_key', 'permissions': [PERMISSION_ROLE_EDIT]}
role_permissions = {'text': _(u'Role permissions'), 'view': 'permissions:role_permissions', 'args': 'object.id', 'famfam': 'key_go', 'permissions': [PERMISSION_PERMISSION_GRANT, PERMISSION_PERMISSION_REVOKE]}
