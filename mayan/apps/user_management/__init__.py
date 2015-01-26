from __future__ import unicode_literals

from django.contrib.auth.models import User, Group

from navigation.api import register_links
from project_setup.api import register_setup
from rest_api.classes import APIEndPoint

from .links import (
    group_add, group_delete, group_edit, group_list, group_members,
    group_multiple_delete, group_setup, user_add, user_delete, user_edit,
    user_groups, user_list, user_multiple_delete, user_multiple_set_password,
    user_set_password, user_setup
)

register_links(User, [user_edit, user_set_password, user_groups, user_delete])
register_links([User, 'user_management:user_multiple_set_password', 'user_management:user_multiple_delete', 'user_management:user_list', 'user_management:user_add'], [user_list, user_add], menu_name='secondary_menu')
register_links(['user_management:user_list'], [user_multiple_set_password, user_multiple_delete], menu_name='multi_item_links')

register_links(Group, [group_edit, group_members, group_delete])
register_links(['user_management:group_multiple_delete', 'user_management:group_delete', 'user_management:group_edit', 'user_management:group_list', 'user_management:group_add', 'user_management:group_members'], [group_list, group_add], menu_name='secondary_menu')
register_links(['user_management:group_list'], [group_multiple_delete], menu_name='multi_item_links')

register_setup(user_setup)
register_setup(group_setup)

APIEndPoint('users', app_name='user_management')
