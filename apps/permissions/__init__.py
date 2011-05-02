from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links

from permissions.conf.settings import DEFAULT_ROLES
from permissions.models import Role

PERMISSION_ROLE_VIEW = 'role_view'
PERMISSION_ROLE_EDIT = 'role_edit'
PERMISSION_ROLE_CREATE = 'role_create'
PERMISSION_ROLE_DELETE = 'role_delete'
PERMISSION_PERMISSION_GRANT = 'permission_grant'
PERMISSION_PERMISSION_REVOKE = 'permission_revoke'


role_list = {'text': _(u'roles'), 'view': 'role_list', 'famfam': 'medal_gold_1', 'permissions': {'namespace': 'permissions', 'permissions': [PERMISSION_ROLE_VIEW]}}
role_create = {'text': _(u'create new role'), 'view': 'role_create', 'famfam': 'medal_gold_add', 'permissions': {'namespace': 'permissions', 'permissions': [PERMISSION_ROLE_CREATE]}}
role_edit = {'text': _(u'edit'), 'view': 'role_edit', 'args': 'object.id', 'famfam': 'medal_gold_1', 'permissions': {'namespace': 'permissions', 'permissions': [PERMISSION_ROLE_EDIT]}}
role_members = {'text': _(u'members'), 'view': 'role_members', 'args': 'object.id', 'famfam': 'group_key', 'permissions': {'namespace': 'permissions', 'permissions': [PERMISSION_ROLE_EDIT]}}
role_permissions = {'text': _(u'role permissions'), 'view': 'role_permissions', 'args': 'object.id', 'famfam': 'key_go', 'permissions': {'namespace': 'permissions', 'permissions': [PERMISSION_PERMISSION_GRANT, PERMISSION_PERMISSION_REVOKE]}}
role_delete = {'text': _(u'delete'), 'view': 'role_delete', 'args': 'object.id', 'famfam': 'medal_gold_delete', 'permissions': {'namespace': 'permissions', 'permissions': [PERMISSION_ROLE_DELETE]}}

register_links(Role, [role_edit, role_delete, role_permissions, role_members])
register_links(['role_members', 'role_list', 'role_view', 'role_create', 'role_edit', 'role_permissions', 'role_delete'], [role_create, role_list], menu_name='sidebar')


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
