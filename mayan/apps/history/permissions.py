from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

history_namespace = PermissionNamespace('history', _(u'History'))
PERMISSION_HISTORY_VIEW = Permission.objects.register(history_namespace, 'history_view', _(u'Access the history of an object'))
