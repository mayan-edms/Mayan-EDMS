from __future__ import absolute_import

import logging

from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.db.models.signals import post_save, post_syncdb
from django.dispatch import receiver
from django.db.utils import DatabaseError

from navigation.api import (bind_links, register_multi_item_links,
    register_multi_item_links)
from documents.models import Document, DocumentVersion
from maintenance.api import register_maintenance_links
from project_tools.api import register_tool
from acls.api import class_permissions
from scheduler.api import register_interval_job
from statistics.api import register_statistics
from job_processor.models import JobQueue, JobType

from .conf.settings import (AUTOMATIC_OCR, QUEUE_PROCESSING_INTERVAL)
from .models import OCRProcessingSingleton
from .api import do_document_ocr
from .permissions import PERMISSION_OCR_DOCUMENT
from .exceptions import AlreadyQueued
from . import models as ocr_models
from .statistics import get_statistics
from .literals import OCR_QUEUE_NAME

logger = logging.getLogger(__name__)
ocr_job_queue = None

from .links import (submit_document, re_queue_multiple_document,
    queue_document_multiple_delete, ocr_disable,
    ocr_enable, all_document_ocr_cleanup, ocr_log,
    ocr_tool_link, submit_document_multiple)

bind_links([Document], [submit_document])
bind_links([OCRProcessingSingleton], [ocr_disable, ocr_enable])
#register_multi_item_links(['queue_document_list'], [re_queue_multiple_document, queue_document_multiple_delete])

register_maintenance_links([all_document_ocr_cleanup], namespace='ocr', title=_(u'OCR'))
register_multi_item_links(['folder_view', 'search', 'results', 'index_instance_node_view', 'document_find_duplicates', 'document_type_document_list', 'document_group_view', 'document_list', 'document_list_recent'], [submit_document_multiple])


@transaction.commit_on_success
def create_ocr_job_queue():
    global ocr_job_queue
    try:
        ocr_job_queue, created = JobQueue.objects.get_or_create(name=OCR_QUEUE_NAME, defaults={'label': _('OCR'), 'unique_jobs': True})
    except DatabaseError:
        transaction.rollback()


@receiver(post_save, dispatch_uid='document_post_save', sender=DocumentVersion)
def document_post_save(sender, instance, **kwargs):
    logger.debug('received post save signal')
    logger.debug('instance: %s' % instance)
    if kwargs.get('created', False):
        if AUTOMATIC_OCR:
            try:
                DocumentQueue.objects.queue_document(instance.document)
            except AlreadyQueued:
                pass

# Disabled because it appears Django execute signals using the same
# process of the signal emiter effectively blocking the view until
# the OCR process completes which could take several minutes :/
#@receiver(post_save, dispatch_uid='call_queue', sender=QueueDocument)
#def call_queue(sender, **kwargs):
#    if kwargs.get('created', False):
#        logger.debug('got call_queue signal: %s' % kwargs)
#        task_process_document_queues()

register_tool(ocr_tool_link)

class_permissions(Document, [
    PERMISSION_OCR_DOCUMENT,
])

#register_statistics(get_statistics)
create_ocr_job_queue()
ocr_job_type = JobType('ocr', _(u'OCR'), do_document_ocr)
