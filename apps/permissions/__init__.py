from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_multi_item_links
from project_setup.api import register_setup

from permissions.conf.settings import DEFAULT_ROLES
from permissions.models import Role, Permission, PermissionNamespace

permissions_namespace = PermissionNamespace('permissions', _(u'Permissions'))

PERMISSION_ROLE_VIEW = Permission.objects.register(permissions_namespace, 'role_view', _(u'View roles'))
PERMISSION_ROLE_EDIT = Permission.objects.register(permissions_namespace, 'role_edit', _(u'Edit roles'))
PERMISSION_ROLE_CREATE = Permission.objects.register(permissions_namespace, 'role_create', _(u'Create roles'))
PERMISSION_ROLE_DELETE = Permission.objects.register(permissions_namespace, 'role_delete', _(u'Delete roles'))
PERMISSION_PERMISSION_GRANT = Permission.objects.register(permissions_namespace, 'permission_grant', _(u'Grant permissions'))
PERMISSION_PERMISSION_REVOKE = Permission.objects.register(permissions_namespace, 'permission_revoke', _(u'Revoke permissions'))

role_list = {'text': _(u'roles'), 'view': 'role_list', 'famfam': 'medal_gold_1', 'icon': 'medal_gold_1.png', 'permissions': [PERMISSION_ROLE_VIEW]}
role_create = {'text': _(u'create new role'), 'view': 'role_create', 'famfam': 'medal_gold_add', 'permissions': [PERMISSION_ROLE_CREATE]}
role_edit = {'text': _(u'edit'), 'view': 'role_edit', 'args': 'object.id', 'famfam': 'medal_gold_1', 'permissions': [PERMISSION_ROLE_EDIT]}
role_members = {'text': _(u'members'), 'view': 'role_members', 'args': 'object.id', 'famfam': 'group_key', 'permissions': [PERMISSION_ROLE_EDIT]}
role_permissions = {'text': _(u'role permissions'), 'view': 'role_permissions', 'args': 'object.id', 'famfam': 'key_go', 'permissions': [PERMISSION_PERMISSION_GRANT, PERMISSION_PERMISSION_REVOKE]}
role_delete = {'text': _(u'delete'), 'view': 'role_delete', 'args': 'object.id', 'famfam': 'medal_gold_delete', 'permissions': [PERMISSION_ROLE_DELETE]}

permission_grant = {'text': _(u'grant'), 'view': 'permission_multiple_grant', 'famfam': 'key_add', 'permissions': [PERMISSION_PERMISSION_GRANT]}
permission_revoke = {'text': _(u'revoke'), 'view': 'permission_multiple_revoke', 'famfam': 'key_delete', 'permissions': [PERMISSION_PERMISSION_REVOKE]}

register_links(Role, [role_edit, role_delete, role_permissions, role_members])
register_links(['role_members', 'role_list', 'role_view', 'role_create', 'role_edit', 'role_permissions', 'role_delete'], [role_list, role_create], menu_name='sidebar')
register_multi_item_links(['role_permissions'], [permission_grant, permission_revoke])

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
