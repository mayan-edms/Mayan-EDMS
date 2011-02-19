from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from common.api import register_links, register_menu, \
    register_model_list_columns
    
from permissions.conf.settings import DEFAULT_ROLES

from models import Role
from api import register_permissions

PERMISSION_ROLE_VIEW = 'role_view'
PERMISSION_ROLE_EDIT = 'role_edit'
PERMISSION_ROLE_CREATE = 'role_create'
PERMISSION_ROLE_DELETE = 'role_delete'
PERMISSION_PERMISSION_GRANT = 'permission_grant'
PERMISSION_PERMISSION_REVOKE = 'permission_revoke'

register_permissions('permissions', [
    {'name':PERMISSION_ROLE_VIEW, 'label':_(u'View roles')},
    {'name':PERMISSION_ROLE_EDIT, 'label':_(u'Edit roles')},
    {'name':PERMISSION_ROLE_CREATE, 'label':_(u'Create roles')},
    {'name':PERMISSION_ROLE_DELETE, 'label':_(u'Delete roles')},
    {'name':PERMISSION_PERMISSION_GRANT, 'label':_(u'Grant permissions')},
    {'name':PERMISSION_PERMISSION_REVOKE, 'label':_(u'Revoke permissions')},
])


role_list = {'text':_(u'roles'), 'view':'role_list', 'famfam':'medal_gold_1', 'permissions':{'namespace':'permissions', 'permissions':[PERMISSION_ROLE_VIEW]}}
role_create = {'text':_(u'create new role'), 'view':'role_create', 'famfam':'medal_gold_add', 'permissions':{'namespace':'permissions', 'permissions':[PERMISSION_ROLE_CREATE]}}
role_edit = {'text':_(u'edit'), 'view':'role_edit', 'args':'object.id', 'famfam':'medal_gold_1', 'permissions':{'namespace':'permissions', 'permissions':[PERMISSION_ROLE_EDIT]}}
role_permissions = {'text':_(u'role permissions'), 'view':'role_permissions', 'args':'object.id', 'famfam':'key_go', 'permissions':{'namespace':'permissions', 'permissions':[PERMISSION_PERMISSION_GRANT, PERMISSION_PERMISSION_REVOKE]}}
role_delete = {'text':_(u'delete'), 'view':'role_delete', 'args':'object.id', 'famfam':'medal_gold_delete', 'permissions':{'namespace':'permissions', 'permissions':[PERMISSION_ROLE_DELETE]}}

register_links(Role, [role_permissions, role_edit, role_delete])
register_links(['role_list', 'role_view', 'role_create', 'role_edit', 'role_permissions', 'role_delete'], [role_create], menu_name='sidebar')


def user_post_save(sender, instance, **kwargs):
    for default_role in DEFAULT_ROLES:
        if isinstance(default_role, Role):
            default_role.add_member(instance)
        else:
            try:
                role = Role.objects.get(name=default_role)
                role.add_member(instance)
            except ObjectDoesNotExist:
                pass

post_save.connect(user_post_save, sender=User)
