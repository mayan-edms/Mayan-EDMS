from __future__ import absolute_import

from django.contrib.auth.models import User, Group

from navigation.api import register_links, register_multi_item_links
from project_setup.api import register_setup

from .links import (user_list, user_setup, user_edit, user_add, user_delete,
    user_multiple_delete, user_set_password, user_multiple_set_password,
    user_groups, group_list, group_setup, group_edit, group_add, group_delete,
    group_multiple_delete, group_members)

register_links(User, [user_edit, user_set_password, user_groups, user_delete])
register_links([User, 'user_multiple_set_password', 'user_multiple_delete', 'user_list', 'user_add'], [user_list, user_add], menu_name=u'secondary_menu')
register_multi_item_links(['user_list'], [user_multiple_set_password, user_multiple_delete])

register_links(Group, [group_edit, group_members, group_delete])
register_links(['group_multiple_delete', 'group_delete', 'group_edit', 'group_list', 'group_add', 'group_members'], [group_list, group_add], menu_name=u'secondary_menu')
register_multi_item_links(['group_list'], [group_multiple_delete])

user_management_views = [
    'user_list', 'user_edit', 'user_add', 'user_delete',
    'user_multiple_delete', 'user_set_password',
    'user_multiple_set_password', 'group_list', 'group_edit', 'group_add',
    'group_delete', 'group_multiple_delete', 'group_members'
]

register_setup(user_setup)
register_setup(group_setup)
