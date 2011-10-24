try:
    from psycopg2 import OperationalError
except ImportError:
    class OperationalError(Exception):
        pass

from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.db.utils import DatabaseError
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _

from permissions import PERMISSION_ROLE_VIEW, PERMISSION_ROLE_EDIT, \
    PERMISSION_ROLE_CREATE, PERMISSION_ROLE_DELETE, \
    PERMISSION_PERMISSION_GRANT, PERMISSION_PERMISSION_REVOKE

from permissions.models import Permission

namespace_titles = {
    'permissions': _(u'Permissions')
}


def set_namespace_title(namespace, title):
    namespace_titles.setdefault(namespace, title)


@transaction.commit_manually
def register_permission(permission):
    try:
        permission_obj, created = Permission.objects.get_or_create(
            namespace=permission['namespace'], name=permission['name'])
        permission_obj.label = unicode(permission['label'])
        permission_obj.save()
    except DatabaseError:
        transaction.rollback()
        # Special case for ./manage.py syncdb
    except (OperationalError, ImproperlyConfigured):
        transaction.rollback()
        # Special for DjangoZoom, which executes collectstatic media
        # doing syncdb and creating the database tables
    else:
        transaction.commit()


def check_permissions(requester, permission_list):
    for permission_item in permission_list:
        permission = get_object_or_404(Permission,
            namespace=permission_item['namespace'], name=permission_item['name'])
        if permission.has_permission(requester):
            return True

    raise PermissionDenied(ugettext(u'Insufficient permissions.'))

register_permission(PERMISSION_ROLE_VIEW)
register_permission(PERMISSION_ROLE_EDIT)
register_permission(PERMISSION_ROLE_CREATE)
register_permission(PERMISSION_ROLE_DELETE)
register_permission(PERMISSION_PERMISSION_GRANT)
register_permission(PERMISSION_PERMISSION_REVOKE)
