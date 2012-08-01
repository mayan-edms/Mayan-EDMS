from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from scheduler.api import LocalScheduler
from navigation.api import bind_links, register_model_list_columns
from project_tools.api import register_tool
from common.utils import encapsulate

from clustering.models import Node

from .models import JobQueue
from .tasks import job_queue_poll
from .links import (node_workers, job_queues, tool_link,
    job_queue_items_pending, job_queue_items_error, job_queue_items_active)

#TODO: fix this, make it cluster wide
JOB_QUEUE_POLL_INTERVAL = 1

job_processor_scheduler = LocalScheduler('job_processor', _(u'Job processor'))
job_processor_scheduler.add_interval_job('job_queue_poll', _(u'Poll a job queue for pending jobs.'), job_queue_poll, seconds=JOB_QUEUE_POLL_INTERVAL)
job_processor_scheduler.start()

register_tool(tool_link)
bind_links([JobQueue, 'job_queues'], [job_queues], menu_name='secondary_menu')
bind_links([JobQueue], [job_queue_items_pending, job_queue_items_active, job_queue_items_error])

bind_links([Node], [node_workers])

Node.add_to_class('workers', lambda node: node.worker_set)

register_model_list_columns(Node, [
    {
        'name': _(u'active workers'),
        'attribute': encapsulate(lambda x: x.workers().all().count())
    },
])
