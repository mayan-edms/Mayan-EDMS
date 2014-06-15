from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

namespace = PermissionNamespace('scheduler', _(u'Scheduler'))
PERMISSION_VIEW_JOB_LIST = Permission.objects.register(namespace, 'jobs_list', _(u'View the interval job list'))
