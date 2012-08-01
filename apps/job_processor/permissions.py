from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

namespace = PermissionNamespace('job_processor', _(u'Job processor'))
PERMISSION_JOB_QUEUE_VIEW = Permission.objects.register(namespace, 'job_queue_view', _(u'View the job queues in a Mayan cluster'))
