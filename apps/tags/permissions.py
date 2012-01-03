from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

tags_namespace = PermissionNamespace('tags', _(u'Tags'))

PERMISSION_TAG_CREATE = Permission.objects.register(tags_namespace, 'tag_create', _(u'Create new tags'))
PERMISSION_TAG_DELETE = Permission.objects.register(tags_namespace, 'tag_delete', _(u'Delete tags'))
PERMISSION_TAG_EDIT = Permission.objects.register(tags_namespace, 'tag_edit', _(u'Edit tags'))
PERMISSION_TAG_VIEW = Permission.objects.register(tags_namespace, 'tag_view', _(u'View tags'))
PERMISSION_TAG_ATTACH = Permission.objects.register(tags_namespace, 'tag_attach', _(u'Attach tags to documents'))
PERMISSION_TAG_REMOVE = Permission.objects.register(tags_namespace, 'tag_remove', _(u'Remove tags from documents'))
