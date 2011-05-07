from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from navigation.api import register_links, register_multi_item_links
from permissions.api import register_permissions

PERMISSION_USER_CREATE = 'user_create'
PERMISSION_USER_EDIT = 'user_edit'
PERMISSION_USER_VIEW = 'user_view'
PERMISSION_USER_DELETE = 'user_delete'

register_permissions('user_management', [
    {'name': PERMISSION_USER_CREATE, 'label': _(u'Create new users')},
    {'name': PERMISSION_USER_EDIT, 'label': _(u'Edit existing users')},
    {'name': PERMISSION_USER_VIEW, 'label': _(u'View existing users')},
    {'name': PERMISSION_USER_DELETE, 'label': _(u'Delete existing users')},
])

user_list = {'text': _(u'user list'), 'view': 'user_list', 'famfam': 'user', 'permissions': {'namespace': 'user_management', 'permissions': [PERMISSION_USER_VIEW]}}
user_edit = {'text': _(u'edit'), 'view': 'user_edit', 'args': 'object.id', 'famfam': 'user_edit', 'permissions': {'namespace': 'user_management', 'permissions': [PERMISSION_USER_EDIT]}}
user_add = {'text': _(u'create new user'), 'view': 'user_add', 'famfam': 'user_add', 'permissions': {'namespace': 'user_management', 'permissions': [PERMISSION_USER_CREATE]}}
user_delete = {u'text': _('delete'), 'view': 'user_delete', 'args': 'object.id', 'famfam': 'user_delete', 'permissions': {'namespace': 'user_management', 'permissions': [PERMISSION_USER_DELETE]}}
user_multiple_delete = {u'text': _('delete'), 'view': 'user_multiple_delete', 'famfam': 'user_delete', 'permissions': {'namespace': 'user_management', 'permissions': [PERMISSION_USER_DELETE]}}
user_set_password = {u'text': _('reset password'), 'view': 'user_set_password', 'args': 'object.id', 'famfam': 'lock_edit', 'permissions': {'namespace': 'user_management', 'permissions': [PERMISSION_USER_EDIT]}}
user_multiple_set_password = {u'text': _('reset password'), 'view': 'user_multiple_set_password', 'famfam': 'lock_edit', 'permissions': {'namespace': 'user_management', 'permissions': [PERMISSION_USER_EDIT]}}

register_links(User, [user_edit, user_set_password, user_delete])
register_links(['user_multiple_set_password', 'user_set_password', 'user_multiple_delete', 'user_delete', 'user_edit', 'user_list','user_add'], [user_add, user_list], menu_name=u'sidebar')
register_multi_item_links(['user_list'], [user_multiple_set_password, user_multiple_delete])
