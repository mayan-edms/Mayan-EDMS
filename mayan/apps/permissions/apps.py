from __future__ import unicode_literals

from django import apps
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from common.menus import (
    menu_multi_item, menu_object, menu_secondary, menu_setup
)
from rest_api.classes import APIEndPoint

from .models import Role
from .links import (
    link_permission_grant, link_permission_revoke, link_role_create,
    link_role_delete, link_role_edit, link_role_list, link_role_members,
    link_role_permissions
)
from .settings import DEFAULT_ROLES


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


class PermissionsApp(apps.AppConfig):
    name = 'permissions'
    verbose_name = _('Permissions')

    def ready(self):
        APIEndPoint('permissions')

        menu_object.bind_links(links=[link_role_edit, link_role_members, link_role_permissions, link_role_delete], sources=[Role])
        menu_multi_item.bind_links(links=[link_permission_grant, link_permission_revoke], sources=['permissions:role_permissions'])
        menu_secondary.bind_links(links=[link_role_list, link_role_create], sources=[Role, 'permissions:role_create', 'permissions:role_list'])
        menu_setup.bind_links(links=[link_role_list])

        post_save.connect(user_post_save, sender=User)
