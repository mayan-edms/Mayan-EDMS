from __future__ import absolute_import

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from navigation.api import bind_links, register_multi_item_links, Link
from project_setup.api import register_setup

from .conf.settings import DEFAULT_ROLES
from .models import Role, Permission, PermissionNamespace
from .permissions import (PERMISSION_ROLE_VIEW, PERMISSION_ROLE_EDIT,
    PERMISSION_ROLE_CREATE, PERMISSION_ROLE_DELETE,
    PERMISSION_PERMISSION_GRANT, PERMISSION_PERMISSION_REVOKE)

role_list = Link(text=_(u'roles'), view='role_list', sprite='medal_gold_1', icon='medal_gold_1.png', permissions=[PERMISSION_ROLE_VIEW])#, 'children_view_regex': [r'^permission_', r'^role_'])
role_create = Link(text=_(u'create new role'), view='role_create', sprite='medal_gold_add', permissions=[PERMISSION_ROLE_CREATE])
role_edit = Link(text=_(u'edit'), view='role_edit', args='object.id', sprite='medal_gold_1', permissions=[PERMISSION_ROLE_EDIT])
role_members = Link(text=_(u'members'), view='role_members', args='object.id', sprite='group_key', permissions=[PERMISSION_ROLE_EDIT])
role_permissions = Link(text=_(u'role permissions'), view='role_permissions', args='object.id', sprite='key_go', permissions=[PERMISSION_PERMISSION_GRANT, PERMISSION_PERMISSION_REVOKE])
role_delete = Link(text=_(u'delete'), view='role_delete', args='object.id', sprite='medal_gold_delete', permissions=[PERMISSION_ROLE_DELETE])

permission_grant = Link(text=_(u'grant'), view='permission_multiple_grant', sprite='key_add', permissions=[PERMISSION_PERMISSION_GRANT])
permission_revoke = Link(text=_(u'revoke'), view='permission_multiple_revoke', sprite='key_delete', permissions=[PERMISSION_PERMISSION_REVOKE])

bind_links([Role], [role_edit, role_delete, role_permissions, role_members])
bind_links([Role, 'role_list', 'role_create'], [role_list, role_create], menu_name='secondary_menu')
register_multi_item_links(['role_permissions'], [permission_grant, permission_revoke])

# TODO: eliminate this
permission_views = ['role_list', 'role_create', 'role_edit', 'role_members', 'role_permissions', 'role_delete']


def user_post_save(sender, instance, **kwargs):
    if kwargs.get('created', False):
        for default_role in DEFAULT_ROLES:
            if isinstance(default_role, Role):
                #If a model is passed, execute method
                default_role.add_member(instance)
            else:
                #If a role name is passed, lookup the corresponding model
                try:
                    role = Role.objects.get(name=default_role)
                    role.add_member(instance)
                except ObjectDoesNotExist:
                    pass

post_save.connect(user_post_save, sender=User)

register_setup(role_list)
