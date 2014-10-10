from __future__ import absolute_import

from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_multi_item_links
from project_setup.api import register_setup
from rest_api.classes import APIEndPoint

from .links import (group_add, group_delete, group_edit, group_list,
                    group_members, group_multiple_delete, group_setup,
                    user_add, user_delete, user_edit, user_groups, user_list,
                    user_multiple_delete, user_multiple_set_password,
                    user_set_password, user_setup)
from .urls import api_urls

register_links(User, [user_edit, user_set_password, user_groups, user_delete])
register_links([User, 'user_management:user_multiple_set_password', 'user_management:user_multiple_delete', 'user_management:user_list', 'user_management:user_add'], [user_list, user_add], menu_name=u'secondary_menu')
register_multi_item_links(['user_management:user_list'], [user_multiple_set_password, user_multiple_delete])

register_links(Group, [group_edit, group_members, group_delete])
register_links(['user_management:group_multiple_delete', 'user_management:group_delete', 'user_management:group_edit', 'user_management:group_list', 'user_management:group_add', 'user_management:group_members'], [group_list, group_add], menu_name=u'secondary_menu')
register_multi_item_links(['user_management:group_list'], [group_multiple_delete])

user_management_views = [
    'user_management:user_list', 'user_management:user_edit', 'user_management:user_add', 'user_management:user_delete',
    'user_management:user_multiple_delete', 'user_management:user_set_password',
    'user_management:user_multiple_set_password', 'user_management:group_list', 'user_management:group_edit', 'user_management:group_add',
    'user_management:group_delete', 'user_management:group_multiple_delete', 'user_management:group_members'
]

register_setup(user_setup)
register_setup(group_setup)

endpoint = APIEndPoint('users')
endpoint.register_urls(api_urls)
endpoint.add_endpoint('user-list', _(u'Returns a list of all the users.'))
