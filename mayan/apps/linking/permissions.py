from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

linking_namespace = PermissionNamespace('linking', _(u'Smart links'))

PERMISSION_SMART_LINK_VIEW = Permission.objects.register(linking_namespace, 'smart_link_view', _(u'View existing smart links'))
PERMISSION_SMART_LINK_CREATE = Permission.objects.register(linking_namespace, 'smart_link_create', _(u'Create new smart links'))
PERMISSION_SMART_LINK_DELETE = Permission.objects.register(linking_namespace, 'smart_link_delete', _(u'Delete smart links'))
PERMISSION_SMART_LINK_EDIT = Permission.objects.register(linking_namespace, 'smart_link_edit', _(u'Edit smart links'))
