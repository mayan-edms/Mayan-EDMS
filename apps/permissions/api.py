from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.utils import DatabaseError
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.core.exceptions import PermissionDenied

from permissions import PERMISSION_ROLE_VIEW, PERMISSION_ROLE_EDIT, \
    PERMISSION_ROLE_CREATE, PERMISSION_ROLE_DELETE, \
    PERMISSION_PERMISSION_GRANT, PERMISSION_PERMISSION_REVOKE

from permissions.models import Permission, Role


def register_permissions(namespace, permissions):
    if permissions:
        for permission in permissions:
            try:
                permission_obj, created = Permission.objects.get_or_create(
                    namespace=namespace, name=permission['name'])
                permission_obj.label = unicode(permission['label'])
                permission_obj.save()
            except DatabaseError:
                #Special case for ./manage.py syncdb
                pass


#TODO: Handle anonymous users
def check_permissions(requester, namespace, permission_list):
    if isinstance(requester, User):
        if requester.is_superuser:
            return True

    for permission_item in permission_list:
        permission = get_object_or_404(Permission,
            namespace=namespace, name=permission_item)
        if check_permission(requester, permission):
            return True

    raise PermissionDenied(ugettext(u'Insufficient permissions.'))


def check_permission(requester, permission):
    for permission_holder in permission.permissionholder_set.all():
        if check_requester(requester, permission_holder):
            return True


def check_requester(requester, permission_holder):
    ct = ContentType.objects.get_for_model(requester)
    if permission_holder.holder_type == ct and permission_holder.holder_id == requester.id:
        return True

    if isinstance(permission_holder.holder_object, Role):
        requester_list = [role_member.member_object for role_member in permission_holder.holder_object.rolemember_set.all()]
        if check_elements(requester, requester_list):
            return True

    #Untested
    if isinstance(permission_holder.holder_object, Group):
        if check_elements(requester, permission_holder.holder_object.user_set.all()):
            return True


#TODO: a role may contain groups, make recursive
def check_elements(requester, requester_list):
    #ct = ContentType.objects.get_for_model(requester)
    for requester_object in requester_list:
        if requester == requester_object:
            return True


register_permissions('permissions', [
    {'name': PERMISSION_ROLE_VIEW, 'label':_(u'View roles')},
    {'name': PERMISSION_ROLE_EDIT, 'label':_(u'Edit roles')},
    {'name': PERMISSION_ROLE_CREATE, 'label':_(u'Create roles')},
    {'name': PERMISSION_ROLE_DELETE, 'label':_(u'Delete roles')},
    {'name': PERMISSION_PERMISSION_GRANT, 'label':_(u'Grant permissions')},
    {'name': PERMISSION_PERMISSION_REVOKE, 'label':_(u'Revoke permissions')},
])
