from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

comments_namespace = PermissionNamespace('comments', _(u'Comments'))

PERMISSION_COMMENT_CREATE = Permission.objects.register(comments_namespace, 'comment_create', _(u'Create new comments'))
PERMISSION_COMMENT_DELETE = Permission.objects.register(comments_namespace, 'comment_delete', _(u'Delete comments'))
PERMISSION_COMMENT_VIEW = Permission.objects.register(comments_namespace, 'comment_view', _(u'View comments'))
