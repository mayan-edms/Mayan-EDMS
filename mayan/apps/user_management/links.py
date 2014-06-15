from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .permissions import (PERMISSION_USER_CREATE, PERMISSION_USER_EDIT,
    PERMISSION_USER_VIEW, PERMISSION_USER_DELETE, PERMISSION_GROUP_CREATE,
    PERMISSION_GROUP_EDIT, PERMISSION_GROUP_VIEW, PERMISSION_GROUP_DELETE)

user_list = {'text': _(u'user list'), 'view': 'user_list', 'famfam': 'user', 'permissions': [PERMISSION_USER_VIEW]}
user_setup = {'text': _(u'users'), 'view': 'user_list', 'famfam': 'user', 'icon': 'user.png', 'permissions': [PERMISSION_USER_VIEW], 'children_view_regex': [r'^user_']}
user_edit = {'text': _(u'edit'), 'view': 'user_edit', 'args': 'object.id', 'famfam': 'user_edit', 'permissions': [PERMISSION_USER_EDIT]}
user_add = {'text': _(u'create new user'), 'view': 'user_add', 'famfam': 'user_add', 'permissions': [PERMISSION_USER_CREATE]}
user_delete = {u'text': _('delete'), 'view': 'user_delete', 'args': 'object.id', 'famfam': 'user_delete', 'permissions': [PERMISSION_USER_DELETE]}
user_multiple_delete = {u'text': _('delete'), 'view': 'user_multiple_delete', 'famfam': 'user_delete', 'permissions': [PERMISSION_USER_DELETE]}
user_set_password = {u'text': _('reset password'), 'view': 'user_set_password', 'args': 'object.id', 'famfam': 'lock_edit', 'permissions': [PERMISSION_USER_EDIT]}
user_multiple_set_password = {u'text': _('reset password'), 'view': 'user_multiple_set_password', 'famfam': 'lock_edit', 'permissions': [PERMISSION_USER_EDIT]}
user_groups = {'text': _(u'groups'), 'view': 'user_groups', 'args': 'object.id', 'famfam': 'group_link', 'permissions': [PERMISSION_USER_EDIT]}

group_list = {'text': _(u'group list'), 'view': 'group_list', 'famfam': 'group', 'permissions': [PERMISSION_GROUP_VIEW]}
group_setup = {'text': _(u'groups'), 'view': 'group_list', 'famfam': 'group', 'icon': 'group.png', 'permissions': [PERMISSION_GROUP_VIEW], 'children_view_regex': [r'^group_']}
group_edit = {'text': _(u'edit'), 'view': 'group_edit', 'args': 'object.id', 'famfam': 'group_edit', 'permissions': [PERMISSION_GROUP_EDIT]}
group_add = {'text': _(u'create new group'), 'view': 'group_add', 'famfam': 'group_add', 'permissions': [PERMISSION_GROUP_CREATE]}
group_delete = {u'text': _('delete'), 'view': 'group_delete', 'args': 'object.id', 'famfam': 'group_delete', 'permissions': [PERMISSION_GROUP_DELETE]}
group_multiple_delete = {u'text': _('delete'), 'view': 'group_multiple_delete', 'famfam': 'group_delete', 'permissions': [PERMISSION_GROUP_DELETE]}
group_members = {'text': _(u'members'), 'view': 'group_members', 'args': 'object.id', 'famfam': 'group_link', 'permissions': [PERMISSION_GROUP_EDIT]}
