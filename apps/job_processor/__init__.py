from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from scheduler.api import register_interval_job
from navigation.api import bind_links, register_model_list_columns
from project_tools.api import register_tool
from common.utils import encapsulate

from .tasks import job_queue_poll
from .links import node_workers
from clustering.models import Node

JOB_QUEUE_POLL_INTERVAL = 1

register_interval_job('job_queue_poll', _(u'Poll a job queue for pending jobs.'), job_queue_poll, seconds=JOB_QUEUE_POLL_INTERVAL)

#register_tool(tool_link)
#bind_links([Node, 'node_list'], [node_list], menu_name='secondary_menu')
bind_links([Node], [node_workers])

Node.add_to_class('workers', lambda node: node.worker_set)

register_model_list_columns(Node, [
    {
        'name': _(u'total workers'),
        'attribute': encapsulate(lambda x: x.workers().all().count())
    },
])
