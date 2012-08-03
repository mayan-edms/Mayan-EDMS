from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import Link

from clustering.permissions import PERMISSION_NODES_VIEW

from .permissions import (PERMISSION_JOB_QUEUE_VIEW,
    PERMISSION_JOB_PROCESSING_CONFIGURATION, PERMISSION_JOB_QUEUE_START_STOP,
    PERMISSION_JOB_REQUEUE, PERMISSION_JOB_DELETE)


def is_running(context):
    return context['object'].is_running()


def is_not_running(context):
    return not context['object'].is_running()


def is_in_error_state(context):
    return context['object'].is_in_error_state


def is_in_pending_state(context):
    return context['object'].is_in_pending_state


node_workers = Link(text=_(u'workers'), view='node_workers', args='object.pk', sprite='lorry_go', permissions=[PERMISSION_NODES_VIEW])
tool_link = Link(text=_(u'job queues'), view='job_queues', icon='hourglass.png', permissions=[PERMISSION_JOB_QUEUE_VIEW])
job_queues = Link(text=_(u'job queue list'), view='job_queues', sprite='hourglass', permissions=[PERMISSION_JOB_QUEUE_VIEW])
job_queue_items_pending = Link(text=_(u'pending jobs'), view='job_queue_items_pending', args='object.pk', sprite='cog', permissions=[PERMISSION_JOB_QUEUE_VIEW])
job_queue_items_error = Link(text=_(u'error jobs'), view='job_queue_items_error', args='object.pk', sprite='cog_error', permissions=[PERMISSION_JOB_QUEUE_VIEW])
job_queue_items_active = Link(text=_(u'active jobs'), view='job_queue_items_active', args='object.pk', sprite='cog', permissions=[PERMISSION_JOB_QUEUE_VIEW])

job_queue_start = Link(text=_(u'start'), view='job_queue_start', args='object.pk', sprite='control_play_blue', permissions=[PERMISSION_JOB_QUEUE_START_STOP], condition=is_not_running)
job_queue_stop = Link(text=_(u'stop'), view='job_queue_stop', args='object.pk', sprite='control_stop_blue', permissions=[PERMISSION_JOB_QUEUE_START_STOP], condition=is_running)

job_queue_config_edit = Link(text=_(u'edit job processing configuration'), view='job_queue_config_edit', sprite='hourglass', permissions=[PERMISSION_JOB_PROCESSING_CONFIGURATION])
setup_link = Link(text=_(u'job processing configuration'), view='job_queue_config_edit', icon='hourglass.png', permissions=[PERMISSION_JOB_PROCESSING_CONFIGURATION])

job_requeue = Link(text=_(u'requeue job'), view='job_requeue', args='object.pk', sprite='cog_add', permissions=[PERMISSION_JOB_REQUEUE], condition=is_in_error_state)
job_delete = Link(text=_(u'delete job'), view='job_delete', args='object.pk', sprite='cog_delete', permissions=[PERMISSION_JOB_DELETE], condition=is_in_pending_state)
