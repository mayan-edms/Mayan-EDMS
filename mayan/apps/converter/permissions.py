from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions.models import Permission, PermissionNamespace

namespace = PermissionNamespace('converter', _('Converter'))
permission_transformation_create = Permission.objects.register(namespace, 'transformation_create', _('Create new transformations'))
permission_transformation_delete = Permission.objects.register(namespace, 'transformation_delete', _('Delete transformations'))
permission_transformation_edit = Permission.objects.register(namespace, 'transformation_edit', _('Edit transformations'))
permission_transformation_view = Permission.objects.register(namespace, 'transformation_view', _('View existing transformations'))
