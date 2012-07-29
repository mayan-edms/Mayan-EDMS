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
from queue_manager.models import Queue

from .conf.settings import (AUTOMATIC_OCR, QUEUE_PROCESSING_INTERVAL)
from .models import OCRProcessingSingleton
from .tasks import task_process_document_queues
from .permissions import PERMISSION_OCR_DOCUMENT
from .exceptions import AlreadyQueued
from . import models as ocr_models
from .statistics import get_statistics
from .literals import OCR_QUEUE_NAME

logger = logging.getLogger(__name__)

from .links import (submit_document, re_queue_multiple_document,
    queue_document_multiple_delete, ocr_disable,
    ocr_enable, all_document_ocr_cleanup, ocr_log,
    ocr_tool_link, submit_document_multiple)

bind_links([Document], [submit_document])
bind_links([OCRProcessingSingleton], [ocr_disable, ocr_enable])
#bind_links([QueueTransformation], [setup_queue_transformation_edit, setup_queue_transformation_delete])

#register_multi_item_links(['queue_document_list'], [re_queue_multiple_document, queue_document_multiple_delete])

#bind_links(['setup_queue_transformation_create', 'setup_queue_transformation_edit', 'setup_queue_transformation_delete', 'document_queue_disable', 'document_queue_enable', 'queue_document_list', 'setup_queue_transformation_list'], [queue_document_list], menu_name='secondary_menu')
#bind_links(['setup_queue_transformation_edit', 'setup_queue_transformation_delete', 'setup_queue_transformation_list', 'setup_queue_transformation_create'], [setup_queue_transformation_create], menu_name='sidebar')

register_maintenance_links([all_document_ocr_cleanup], namespace='ocr', title=_(u'OCR'))
#register_multi_item_links(['folder_view', 'search', 'results', 'index_instance_node_view', 'document_find_duplicates', 'document_type_document_list', 'document_group_view', 'document_list', 'document_list_recent'], [submit_document_multiple])


@transaction.commit_on_success
def create_ocr_queue():
    try:
        queue, created = Queue.objects.get_or_create(name=OCR_QUEUE_NAME, defaults={'label': _('OCR'), 'unique_names': True})
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


#@receiver(post_syncdb, dispatch_uid='create_ocr_queue_on_syncdb', sender=ocr_models)
#def create_ocr_queue_on_syncdb(sender, **kwargs):

#register_interval_job('task_process_document_queues', _(u'Checks the OCR queue for pending documents.'), task_process_document_queues, seconds=QUEUE_PROCESSING_INTERVAL)

register_tool(ocr_tool_link)

class_permissions(Document, [
    PERMISSION_OCR_DOCUMENT,
])

#register_statistics(get_statistics)
create_ocr_queue()
