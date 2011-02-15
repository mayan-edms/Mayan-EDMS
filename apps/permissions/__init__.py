from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from common.api import register_links, register_menu, \
    register_model_list_columns
    
from permissions.conf.settings import DEFAULT_ROLES

from models import Role

role_list = {'text':_(u'roles'), 'view':'role_list', 'famfam':'medal_gold_1'}#, 'permissions':{'namespace':'documents', 'permissions':[PERMISSION_DOCUMENT_VIEW]}}
role_view = {'text':_(u'role details'), 'view':'role_view', 'args':'object.id', 'famfam':'medal_gold_1'}#, 'permissions':{'namespace':'documents', 'permissions':[PERMISSION_DOCUMENT_VIEW]}}
role_create = {'text':_(u'create new role'), 'view':'role_create', 'famfam':'medal_gold_add'}#, 'permissions':{'namespace':'documents', 'permissions':[PERMISSION_DOCUMENT_VIEW]}}
role_delete = {'text':_(u'delete'), 'view':'role_delete', 'args':'object.id', 'famfam':'medal_gold_delete'}#, 'permissions':{'namespace':'documents', 'permissions':[PERMISSION_DOCUMENT_VIEW]}}

register_links(Role, [role_view], menu_name='sidebar')
register_links(Role, [role_delete])
register_links(['role_list', 'role_view', 'role_create', 'role_delete'], [role_create], menu_name='sidebar')


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
