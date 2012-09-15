from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from clustering.permissions import PERMISSION_NODES_VIEW

from .permissions import (PERMISSION_JOB_QUEUE_VIEW,
    PERMISSION_JOB_PROCESSING_CONFIGURATION, PERMISSION_JOB_QUEUE_START_STOP,
    PERMISSION_JOB_REQUEUE, PERMISSION_JOB_DELETE, PERMISSION_WORKER_TERMINATE)
from .icons import (icon_node_workers, icon_tool_link, icon_job_queues,
    icon_job_queue_items_pending, icon_job_queue_items_error, icon_job_queue_items_active,
    icon_job_queue_start, icon_job_queue_stop, icon_job_requeue, icon_job_delete,
    icon_worker_terminate)
    

def is_running(context):
    return context['object'].is_running()


def is_not_running(context):
    return not context['object'].is_running()


def is_in_error_state(context):
    return context['object'].is_in_error_state


def is_in_pending_state(context):
    return context['object'].is_in_pending_state


#icon_job_queue_config_edit == sprite='hourglass'
#icon_setup_link icon='hourglass.png'


node_workers = Link(text=_(u'workers'), view='node_workers', args='object.pk', icon=icon_node_workers, permissions=[PERMISSION_NODES_VIEW])
tool_link = Link(text=_(u'job queues'), view='job_queues', icon=icon_tool_link, permissions=[PERMISSION_JOB_QUEUE_VIEW])
job_queues = Link(text=_(u'job queue list'), view='job_queues', icon=icon_job_queues, permissions=[PERMISSION_JOB_QUEUE_VIEW])
job_queue_items_pending = Link(text=_(u'pending jobs'), view='job_queue_items_pending', args='object.pk', icon=icon_job_queue_items_pending, permissions=[PERMISSION_JOB_QUEUE_VIEW])
job_queue_items_error = Link(text=_(u'error jobs'), view='job_queue_items_error', args='object.pk', icon=icon_job_queue_items_error, permissions=[PERMISSION_JOB_QUEUE_VIEW])
job_queue_items_active = Link(text=_(u'active jobs'), view='job_queue_items_active', args='object.pk', icon=icon_job_queue_items_active, permissions=[PERMISSION_JOB_QUEUE_VIEW])

job_queue_start = Link(text=_(u'start'), view='job_queue_start', args='object.pk', icon=icon_job_queue_start, permissions=[PERMISSION_JOB_QUEUE_START_STOP], condition=is_not_running)
job_queue_stop = Link(text=_(u'stop'), view='job_queue_stop', args='object.pk', icon=icon_job_queue_stop, permissions=[PERMISSION_JOB_QUEUE_START_STOP], condition=is_running)

job_requeue = Link(text=_(u'requeue job'), view='job_requeue', args='object.pk', icon=icon_job_requeue, permissions=[PERMISSION_JOB_REQUEUE], condition=is_in_error_state)
job_delete = Link(text=_(u'delete job'), view='job_delete', args='object.pk', icon=icon_job_delete, permissions=[PERMISSION_JOB_DELETE], condition=is_in_pending_state)

worker_terminate = Link(text=_(u'terminate worker'), view='worker_terminate', args='object.pk', icon=icon_worker_terminate, permissions=[PERMISSION_WORKER_TERMINATE])


'''
re_queue_document = Link(text=_('re-queue'), view='re_queue_document', args='object.id', sprite='hourglass_add', permissions=[PERMISSION_OCR_DOCUMENT])
re_queue_multiple_document = Link(text=_('re-queue'), view='re_queue_multiple_document', sprite='hourglass_add', permissions=[PERMISSION_OCR_DOCUMENT])
queue_document_delete = Link(text=_(u'delete'), view='queue_document_delete', args='object.id', sprite='hourglass_delete', permissions=[PERMISSION_OCR_DOCUMENT_DELETE])
queue_document_multiple_delete = Link(text=_(u'delete'), view='queue_document_multiple_delete', sprite='hourglass_delete', permissions=[PERMISSION_OCR_DOCUMENT_DELETE])
'''
