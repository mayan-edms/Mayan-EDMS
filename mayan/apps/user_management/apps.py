from __future__ import unicode_literals

from django import apps
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _

from actstream import registry

from common import menu_setup
from rest_api.classes import APIEndPoint

from .links import (
    link_group_add, link_group_delete, link_group_edit, link_group_list,
    link_group_members, link_group_multiple_delete, link_group_setup,
    link_user_add, link_user_delete, link_user_edit, link_user_groups,
    link_user_list, link_user_multiple_delete,
    link_user_multiple_set_password, link_user_set_password, link_user_setup
)


class UserManagementApp(apps.AppConfig):
    name = 'user_management'
    verbose_name = _('User management')

    def ready(self):
        # TODO: convert
        #register_links(User, [user_edit, user_set_password, user_groups, user_delete])
        #register_links([User, 'user_management:user_multiple_set_password', 'user_management:user_multiple_delete', 'user_management:user_list', 'user_management:user_add'], [user_list, user_add], menu_name='secondary_menu')
        #register_links(['user_management:user_list'], [user_multiple_set_password, user_multiple_delete], menu_name='multi_item_links')
        #register_links(Group, [group_edit, group_members, group_delete])
        #register_links(['user_management:group_multiple_delete', 'user_management:group_delete', 'user_management:group_edit', 'user_management:group_list', 'user_management:group_add', 'user_management:group_members'], [group_list, group_add], menu_name='secondary_menu')
        #register_links(['user_management:group_list'], [group_multiple_delete], menu_name='multi_item_links')

        menu_setup.bind_links(links=[link_user_setup, link_group_setup])

        APIEndPoint('users', app_name='user_management')

        registry.register(User)
        registry.register(Group)
