from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

tags_namespace = PermissionNamespace('tags', _('Tags'))

PERMISSION_TAG_CREATE = Permission.objects.register(tags_namespace, 'tag_create', _('Create new tags'))
PERMISSION_TAG_DELETE = Permission.objects.register(tags_namespace, 'tag_delete', _('Delete tags'))
PERMISSION_TAG_EDIT = Permission.objects.register(tags_namespace, 'tag_edit', _('Edit tags'))
PERMISSION_TAG_VIEW = Permission.objects.register(tags_namespace, 'tag_view', _('View tags'))
PERMISSION_TAG_ATTACH = Permission.objects.register(tags_namespace, 'tag_attach', _('Attach tags to documents'))
PERMISSION_TAG_REMOVE = Permission.objects.register(tags_namespace, 'tag_remove', _('Remove tags from documents'))
