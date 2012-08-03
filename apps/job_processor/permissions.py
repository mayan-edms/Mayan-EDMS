from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

namespace = PermissionNamespace('job_processor', _(u'Job processor'))
PERMISSION_JOB_QUEUE_VIEW = Permission.objects.register(namespace, 'job_queue_view', _(u'View the job queues in a Mayan cluster'))
PERMISSION_JOB_PROCESSING_CONFIGURATION = Permission.objects.register(namespace, 'job_processing_edit', _(u'Edit the the job processing configuration in a Mayan cluster'))
PERMISSION_JOB_QUEUE_START_STOP = Permission.objects.register(namespace, 'job_queue_start_stop', _(u'Can start and stop a job queue in a Mayan cluster'))
PERMISSION_JOB_REQUEUE = Permission.objects.register(namespace, 'job_requeue', _(u'Requeue a job in a Mayan cluster'))
PERMISSION_JOB_DELETE = Permission.objects.register(namespace, 'job_delete', _(u'Delete a pending job in a Mayan cluster'))
PERMISSION_WORKER_TERMINATE = Permission.objects.register(namespace, 'worker_terminate', _(u'Terminate a worker processing a job in a Mayan cluster'))
