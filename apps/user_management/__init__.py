from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group

from navigation.api import register_links, register_multi_item_links
from permissions.api import register_permission, set_namespace_title

PERMISSION_USER_CREATE = {'namespace': 'user_management', 'name': 'user_create', 'label': _(u'Create new users')}
PERMISSION_USER_EDIT = {'namespace': 'user_management', 'name': 'user_edit', 'label': _(u'Edit existing users')}
PERMISSION_USER_VIEW = {'namespace': 'user_management', 'name': 'user_view', 'label': _(u'View existing users')}
PERMISSION_USER_DELETE = {'namespace': 'user_management', 'name': 'user_delete', 'label': _(u'Delete existing users')}

PERMISSION_GROUP_CREATE = {'namespace': 'user_management', 'name': 'group_create', 'label': _(u'Create new groups')}
PERMISSION_GROUP_EDIT = {'namespace': 'user_management', 'name': 'group_edit', 'label': _(u'Edit existing groups')}
PERMISSION_GROUP_VIEW = {'namespace': 'user_management', 'name': 'group_view', 'label': _(u'View existing groups')}
PERMISSION_GROUP_DELETE = {'namespace': 'user_management', 'name': 'group_delete', 'label': _(u'Delete existing groups')}

set_namespace_title('user_management', _(u'User management'))
register_permission(PERMISSION_USER_CREATE)
register_permission(PERMISSION_USER_EDIT)
register_permission(PERMISSION_USER_VIEW)
register_permission(PERMISSION_USER_DELETE)
register_permission(PERMISSION_GROUP_CREATE)
register_permission(PERMISSION_GROUP_EDIT)
register_permission(PERMISSION_GROUP_VIEW)
register_permission(PERMISSION_GROUP_DELETE)

user_list = {'text': _(u'user list'), 'view': 'user_list', 'famfam': 'user', 'permissions': [PERMISSION_USER_VIEW]}
user_edit = {'text': _(u'edit'), 'view': 'user_edit', 'args': 'object.id', 'famfam': 'user_edit', 'permissions': [PERMISSION_USER_EDIT]}
user_add = {'text': _(u'create new user'), 'view': 'user_add', 'famfam': 'user_add', 'permissions': [PERMISSION_USER_CREATE]}
user_delete = {u'text': _('delete'), 'view': 'user_delete', 'args': 'object.id', 'famfam': 'user_delete', 'permissions': [PERMISSION_USER_DELETE]}
user_multiple_delete = {u'text': _('delete'), 'view': 'user_multiple_delete', 'famfam': 'user_delete', 'permissions': [PERMISSION_USER_DELETE]}
user_set_password = {u'text': _('reset password'), 'view': 'user_set_password', 'args': 'object.id', 'famfam': 'lock_edit', 'permissions': [PERMISSION_USER_EDIT]}
user_multiple_set_password = {u'text': _('reset password'), 'view': 'user_multiple_set_password', 'famfam': 'lock_edit', 'permissions': [PERMISSION_USER_EDIT]}

group_list = {'text': _(u'group list'), 'view': 'group_list', 'famfam': 'group', 'permissions': [PERMISSION_GROUP_VIEW]}
group_edit = {'text': _(u'edit'), 'view': 'group_edit', 'args': 'object.id', 'famfam': 'group_edit', 'permissions': [PERMISSION_GROUP_EDIT]}
group_add = {'text': _(u'create new group'), 'view': 'group_add', 'famfam': 'group_add', 'permissions': [PERMISSION_GROUP_CREATE]}
group_delete = {u'text': _('delete'), 'view': 'group_delete', 'args': 'object.id', 'famfam': 'group_delete', 'permissions': [PERMISSION_GROUP_DELETE]}
group_multiple_delete = {u'text': _('delete'), 'view': 'group_multiple_delete', 'famfam': 'group_delete', 'permissions': [PERMISSION_GROUP_DELETE]}
group_members = {'text': _(u'members'), 'view': 'group_members', 'args': 'object.id', 'famfam': 'group_link', 'permissions': [PERMISSION_GROUP_EDIT]}

register_links(User, [user_edit, user_set_password, user_delete])
register_links(['user_multiple_set_password', 'user_set_password', 'user_multiple_delete', 'user_delete', 'user_edit', 'user_list', 'user_add'], [user_add], menu_name=u'sidebar')
register_multi_item_links(['user_list'], [user_multiple_set_password, user_multiple_delete])

register_links(Group, [group_edit, group_members, group_delete])
register_links(['group_multiple_delete', 'group_delete', 'group_edit', 'group_list', 'group_add', 'group_members'], [group_add], menu_name=u'sidebar')
register_multi_item_links(['group_list'], [group_multiple_delete])

user_management_views = [
    'user_list', 'user_edit', 'user_add', 'user_delete',
    'user_multiple_delete', 'user_set_password',
    'user_multiple_set_password', 'group_list', 'group_edit', 'group_add',
    'group_delete', 'group_multiple_delete', 'group_members'
]
