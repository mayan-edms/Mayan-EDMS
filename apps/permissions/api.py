from django.db.utils import DatabaseError
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.core.exceptions import PermissionDenied

from permissions import PERMISSION_ROLE_VIEW, PERMISSION_ROLE_EDIT, \
    PERMISSION_ROLE_CREATE, PERMISSION_ROLE_DELETE, \
    PERMISSION_PERMISSION_GRANT, PERMISSION_PERMISSION_REVOKE

from permissions.models import Permission


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
    for permission_item in permission_list:
        permission = get_object_or_404(Permission,
            namespace=namespace, name=permission_item)
        #if check_permission(requester, permission):
        if permission.has_permission(requester):
            return True

    raise PermissionDenied(ugettext(u'Insufficient permissions.'))


register_permissions('permissions', [
    {'name': PERMISSION_ROLE_VIEW, 'label':_(u'View roles')},
    {'name': PERMISSION_ROLE_EDIT, 'label':_(u'Edit roles')},
    {'name': PERMISSION_ROLE_CREATE, 'label':_(u'Create roles')},
    {'name': PERMISSION_ROLE_DELETE, 'label':_(u'Delete roles')},
    {'name': PERMISSION_PERMISSION_GRANT, 'label':_(u'Grant permissions')},
    {'name': PERMISSION_PERMISSION_REVOKE, 'label':_(u'Revoke permissions')},
])
