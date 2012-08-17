from __future__ import absolute_import

from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _

from backups.api import AppBackup, ModelBackup
from app_registry import register_app, UnableToRegister
from navigation.api import bind_links, register_multi_item_links
from project_setup.api import register_setup

from .links import (user_list, user_setup, user_edit, user_add, user_delete,
    user_multiple_delete, user_set_password, user_multiple_set_password,
    group_list, group_setup, group_edit, group_add, group_delete,
    group_multiple_delete, group_members)

bind_links([User], [user_edit, user_set_password, user_delete])
bind_links(['user_multiple_set_password', 'user_set_password', 'user_multiple_delete', 'user_delete', 'user_edit', 'user_list', 'user_add'], [user_list, user_add], menu_name=u'secondary_menu')
register_multi_item_links(['user_list'], [user_multiple_set_password, user_multiple_delete])

bind_links([Group], [group_edit, group_members, group_delete])
bind_links(['group_multiple_delete', 'group_delete', 'group_edit', 'group_list', 'group_add', 'group_members'], [group_list, group_add], menu_name=u'secondary_menu')
register_multi_item_links(['group_list'], [group_multiple_delete])

user_management_views = [
    'user_list', 'user_edit', 'user_add', 'user_delete',
    'user_multiple_delete', 'user_set_password',
    'user_multiple_set_password', 'group_list', 'group_edit', 'group_add',
    'group_delete', 'group_multiple_delete', 'group_members'
]

register_setup(user_setup)
register_setup(group_setup)

try:
    app = register_app('user_management', _(u'User management'))
except UnableToRegister:
    pass
#else:
#    AppBackup(app, [ModelBackup()])
