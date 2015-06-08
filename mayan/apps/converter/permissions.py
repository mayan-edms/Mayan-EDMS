from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions.models import Permission, PermissionNamespace

namespace = PermissionNamespace('converter', _('Converter'))
PERMISSION_TRANSFORMATION_CREATE = Permission.objects.register(namespace, 'transformation_create', _('Create new transformations'))
PERMISSION_TRANSFORMATION_DELETE = Permission.objects.register(namespace, 'transformation_delete', _('Delete transformations'))
PERMISSION_TRANSFORMATION_EDIT = Permission.objects.register(namespace, 'transformation_edit', _('Edit transformations'))
PERMISSION_TRANSFORMATION_VIEW = Permission.objects.register(namespace, 'transformation_view', _('View existing transformations'))
