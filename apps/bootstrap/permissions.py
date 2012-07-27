from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

namespace = PermissionNamespace('bootstrap', _(u'Database bootstrap'))

PERMISSION_BOOTSTRAP_EXECUTE = Permission.objects.register(namespace, 'bootstrap_execute', _(u'Execute document bootstraps'))
PERMISSION_NUKE_DATABASE = Permission.objects.register(namespace, 'nuke_database', _(u'Erase the entire database and document storage'))

