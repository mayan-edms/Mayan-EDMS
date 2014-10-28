from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .permissions import (PERMISSION_GROUP_CREATE, PERMISSION_GROUP_DELETE,
                          PERMISSION_GROUP_EDIT, PERMISSION_GROUP_VIEW,
                          PERMISSION_USER_CREATE, PERMISSION_USER_DELETE,
                          PERMISSION_USER_EDIT, PERMISSION_USER_VIEW)

user_list = {'text': _(u'Users'), 'view': 'user_management:user_list', 'famfam': 'user', 'permissions': [PERMISSION_USER_VIEW]}
user_setup = {'text': _(u'Users'), 'view': 'user_management:user_list', 'famfam': 'user', 'icon': 'user.png', 'permissions': [PERMISSION_USER_VIEW]}
user_edit = {'text': _(u'Edit'), 'view': 'user_management:user_edit', 'args': 'object.id', 'famfam': 'user_edit', 'permissions': [PERMISSION_USER_EDIT]}
user_add = {'text': _(u'Create new user'), 'view': 'user_management:user_add', 'famfam': 'user_add', 'permissions': [PERMISSION_USER_CREATE]}
user_delete = {u'text': _('Delete'), 'view': 'user_management:user_delete', 'args': 'object.id', 'famfam': 'user_delete', 'permissions': [PERMISSION_USER_DELETE]}
user_multiple_delete = {u'text': _('Delete'), 'view': 'user_management:user_multiple_delete', 'famfam': 'user_delete', 'permissions': [PERMISSION_USER_DELETE]}
user_set_password = {u'text': _('Reset password'), 'view': 'user_management:user_set_password', 'args': 'object.id', 'famfam': 'lock_edit', 'permissions': [PERMISSION_USER_EDIT]}
user_multiple_set_password = {u'text': _('Reset password'), 'view': 'user_management:user_multiple_set_password', 'famfam': 'lock_edit', 'permissions': [PERMISSION_USER_EDIT]}
user_groups = {'text': _(u'Groups'), 'view': 'user_management:user_groups', 'args': 'object.id', 'famfam': 'group_link', 'permissions': [PERMISSION_USER_EDIT]}

group_list = {'text': _(u'Groups'), 'view': 'user_management:group_list', 'famfam': 'group', 'permissions': [PERMISSION_GROUP_VIEW]}
group_setup = {'text': _(u'Groups'), 'view': 'user_management:group_list', 'famfam': 'group', 'icon': 'group.png', 'permissions': [PERMISSION_GROUP_VIEW]}
group_edit = {'text': _(u'Edit'), 'view': 'user_management:group_edit', 'args': 'object.id', 'famfam': 'group_edit', 'permissions': [PERMISSION_GROUP_EDIT]}
group_add = {'text': _(u'Create new group'), 'view': 'user_management:group_add', 'famfam': 'group_add', 'permissions': [PERMISSION_GROUP_CREATE]}
group_delete = {u'text': _('Delete'), 'view': 'user_management:group_delete', 'args': 'object.id', 'famfam': 'group_delete', 'permissions': [PERMISSION_GROUP_DELETE]}
group_multiple_delete = {u'text': _('Delete'), 'view': 'user_management:group_multiple_delete', 'famfam': 'group_delete', 'permissions': [PERMISSION_GROUP_DELETE]}
group_members = {'text': _(u'Members'), 'view': 'user_management:group_members', 'args': 'object.id', 'famfam': 'group_link', 'permissions': [PERMISSION_GROUP_EDIT]}
