from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .models import Permission, PermissionNamespace

permissions_namespace = PermissionNamespace('permissions', _(u'Permissions'))

PERMISSION_ROLE_VIEW = Permission.objects.register(permissions_namespace, 'role_view', _(u'View roles'))
PERMISSION_ROLE_EDIT = Permission.objects.register(permissions_namespace, 'role_edit', _(u'Edit roles'))
PERMISSION_ROLE_CREATE = Permission.objects.register(permissions_namespace, 'role_create', _(u'Create roles'))
PERMISSION_ROLE_DELETE = Permission.objects.register(permissions_namespace, 'role_delete', _(u'Delete roles'))
PERMISSION_PERMISSION_GRANT = Permission.objects.register(permissions_namespace, 'permission_grant', _(u'Grant permissions'))
PERMISSION_PERMISSION_REVOKE = Permission.objects.register(permissions_namespace, 'permission_revoke', _(u'Revoke permissions'))
