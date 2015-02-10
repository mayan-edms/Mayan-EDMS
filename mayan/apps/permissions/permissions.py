from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from .models import Permission, PermissionNamespace

permissions_namespace = PermissionNamespace('permissions', _('Permissions'))

PERMISSION_ROLE_VIEW = Permission.objects.register(permissions_namespace, 'role_view', _('View roles'))
PERMISSION_ROLE_EDIT = Permission.objects.register(permissions_namespace, 'role_edit', _('Edit roles'))
PERMISSION_ROLE_CREATE = Permission.objects.register(permissions_namespace, 'role_create', _('Create roles'))
PERMISSION_ROLE_DELETE = Permission.objects.register(permissions_namespace, 'role_delete', _('Delete roles'))
PERMISSION_PERMISSION_GRANT = Permission.objects.register(permissions_namespace, 'permission_grant', _('Grant permissions'))
PERMISSION_PERMISSION_REVOKE = Permission.objects.register(permissions_namespace, 'permission_revoke', _('Revoke permissions'))
