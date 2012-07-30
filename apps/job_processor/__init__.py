from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from scheduler.api import register_interval_job

from .tasks import refresh_node, job_queue_poll

NODE_REFRESH_INTERVAL = 1
JOB_QUEUE_POLL_INTERVAL = 1

register_interval_job('refresh_node', _(u'Update a node\'s properties.'), refresh_node, seconds=NODE_REFRESH_INTERVAL)
register_interval_job('job_queue_poll', _(u'Poll a job queue for pending jobs.'), job_queue_poll, seconds=JOB_QUEUE_POLL_INTERVAL)
