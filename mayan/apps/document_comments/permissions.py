from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

comments_namespace = PermissionNamespace('comments', _('Comments'))

PERMISSION_COMMENT_CREATE = Permission.objects.register(comments_namespace, 'comment_create', _('Create new comments'))
PERMISSION_COMMENT_DELETE = Permission.objects.register(comments_namespace, 'comment_delete', _('Delete comments'))
PERMISSION_COMMENT_VIEW = Permission.objects.register(comments_namespace, 'comment_view', _('View comments'))
