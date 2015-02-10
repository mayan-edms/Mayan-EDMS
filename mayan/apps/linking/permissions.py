from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

linking_namespace = PermissionNamespace('linking', _('Smart links'))

PERMISSION_SMART_LINK_VIEW = Permission.objects.register(linking_namespace, 'smart_link_view', _('View existing smart links'))
PERMISSION_SMART_LINK_CREATE = Permission.objects.register(linking_namespace, 'smart_link_create', _('Create new smart links'))
PERMISSION_SMART_LINK_DELETE = Permission.objects.register(linking_namespace, 'smart_link_delete', _('Delete smart links'))
PERMISSION_SMART_LINK_EDIT = Permission.objects.register(linking_namespace, 'smart_link_edit', _('Edit smart links'))
