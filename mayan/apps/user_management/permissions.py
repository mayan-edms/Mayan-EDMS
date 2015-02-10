from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

user_management_namespace = PermissionNamespace('user_management', _('User management'))

PERMISSION_USER_CREATE = Permission.objects.register(user_management_namespace, 'user_create', _('Create new users'))
PERMISSION_USER_EDIT = Permission.objects.register(user_management_namespace, 'user_edit', _('Edit existing users'))
PERMISSION_USER_VIEW = Permission.objects.register(user_management_namespace, 'user_view', _('View existing users'))
PERMISSION_USER_DELETE = Permission.objects.register(user_management_namespace, 'user_delete', _('Delete existing users'))

PERMISSION_GROUP_CREATE = Permission.objects.register(user_management_namespace, 'group_create', _('Create new groups'))
PERMISSION_GROUP_EDIT = Permission.objects.register(user_management_namespace, 'group_edit', _('Edit existing groups'))
PERMISSION_GROUP_VIEW = Permission.objects.register(user_management_namespace, 'group_view', _('View existing groups'))
PERMISSION_GROUP_DELETE = Permission.objects.register(user_management_namespace, 'group_delete', _('Delete existing groups'))
