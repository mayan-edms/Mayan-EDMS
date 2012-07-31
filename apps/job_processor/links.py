from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import Link

from clustering.permissions import PERMISSION_NODES_VIEW

from .permissions import PERMISSION_JOB_QUEUE_VIEW


node_workers = Link(text=_(u'workers'), view='node_workers', args='object.pk', sprite='lorry_go', permissions=[PERMISSION_NODES_VIEW])

tool_link = Link(text=_(u'job queues'), view='job_queues', icon='hourglass.png', permissions=[PERMISSION_JOB_QUEUE_VIEW])
job_queues = Link(text=_(u'job queues list'), view='job_queues', sprite='hourglass', permissions=[PERMISSION_JOB_QUEUE_VIEW])
job_queue_items_pending = Link(text=_(u'pending jobs'), view='job_queue_items_pending', args='object.pk', sprite='text_list_bullets', permissions=[PERMISSION_JOB_QUEUE_VIEW])
job_queue_items_error = Link(text=_(u'error jobs'), view='job_queue_items_error', args='object.pk', sprite='text_list_bullets', permissions=[PERMISSION_JOB_QUEUE_VIEW])
job_queue_items_active = Link(text=_(u'active jobs'), view='job_queue_items_active', args='object.pk', sprite='text_list_bullets', permissions=[PERMISSION_JOB_QUEUE_VIEW])
