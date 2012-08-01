from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

namespace = PermissionNamespace('clustering', _(u'Clustering'))
PERMISSION_NODES_VIEW = Permission.objects.register(namespace, 'nodes_view', _(u'View the nodes in a Mayan cluster'))
