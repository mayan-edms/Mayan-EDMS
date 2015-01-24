from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save

from navigation.api import register_links
from project_setup.api import register_setup
from rest_api.classes import APIEndPoint

from .models import Permission, Role
from .links import (
    permission_grant, permission_revoke, role_create, role_delete, role_edit,
    role_list, role_members, role_permissions
)
from .settings import DEFAULT_ROLES

register_links(Role, [role_edit, role_members, role_permissions, role_delete])
register_links([Role, 'permissions:role_create', 'permissions:role_list'], [role_list, role_create], menu_name='secondary_menu')
register_links(['permissions:role_permissions'], [permission_grant, permission_revoke], menu_name='multi_item_links')


def user_post_save(sender, instance, **kwargs):
    if kwargs.get('created', False):
        for default_role in DEFAULT_ROLES:
            if isinstance(default_role, Role):
                # If a model is passed, execute method
                default_role.add_member(instance)
            else:
                # If a role name is passed, lookup the corresponding model
                try:
                    role = Role.objects.get(name=default_role)
                    role.add_member(instance)
                except ObjectDoesNotExist:
                    pass


post_save.connect(user_post_save, sender=User)

register_setup(role_list)

APIEndPoint('permissions')
