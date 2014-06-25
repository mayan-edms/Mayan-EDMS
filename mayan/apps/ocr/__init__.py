from __future__ import absolute_import

import logging

from django.db import transaction
from django.db.utils import DatabaseError
from django.db.models.signals import post_save, post_syncdb
from django.dispatch import receiver
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from acls.api import class_permissions
from documents.models import Document, DocumentVersion
from main.api import register_maintenance_links
from navigation.api import register_links, register_multi_item_links
from project_tools.api import register_tool
from scheduler.api import register_interval_job

from . import models as ocr_models
from .conf.settings import (AUTOMATIC_OCR, QUEUE_PROCESSING_INTERVAL)
from .exceptions import AlreadyQueued
from .links import (submit_document, submit_document_multiple,
    re_queue_multiple_document, queue_document_multiple_delete,
    document_queue_disable, document_queue_enable,
    all_document_ocr_cleanup, queue_document_list,
    ocr_tool_link, setup_queue_transformation_list,
    setup_queue_transformation_create, setup_queue_transformation_edit,
    setup_queue_transformation_delete)
from .models import DocumentQueue, QueueTransformation
from .permissions import PERMISSION_OCR_DOCUMENT
from .tasks import task_process_document_queues

logger = logging.getLogger(__name__)


register_links(Document, [submit_document])
register_multi_item_links(['document_find_duplicates', 'folder_view', 'index_instance_node_view', 'document_type_document_list', 'search', 'results', 'document_group_view', 'document_list', 'document_list_recent', 'tag_tagged_item_list'], [submit_document_multiple])

register_links(DocumentQueue, [document_queue_disable, document_queue_enable, setup_queue_transformation_list])
register_links(QueueTransformation, [setup_queue_transformation_edit, setup_queue_transformation_delete])

register_multi_item_links(['queue_document_list'], [re_queue_multiple_document, queue_document_multiple_delete])

register_links(['setup_queue_transformation_create', 'setup_queue_transformation_edit', 'setup_queue_transformation_delete', 'document_queue_disable', 'document_queue_enable', 'queue_document_list', 'setup_queue_transformation_list'], [queue_document_list], menu_name='secondary_menu')
register_links(['setup_queue_transformation_edit', 'setup_queue_transformation_delete', 'setup_queue_transformation_list', 'setup_queue_transformation_create'], [setup_queue_transformation_create], menu_name='sidebar')

register_maintenance_links([all_document_ocr_cleanup], namespace='ocr', title=_(u'OCR'))


@transaction.commit_on_success
def create_default_queue():
    try:
        default_queue, created = DocumentQueue.objects.get_or_create(name='default')
    except DatabaseError:
        transaction.rollback()
    else:
        if created:
            default_queue.label = ugettext(u'Default')
            default_queue.save()


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


@receiver(post_syncdb, dispatch_uid='create_default_queue', sender=ocr_models)
def create_default_queue_signal_handler(sender, **kwargs):
    create_default_queue()

register_interval_job('task_process_document_queues', _(u'Checks the OCR queue for pending documents.'), task_process_document_queues, seconds=QUEUE_PROCESSING_INTERVAL)

register_tool(ocr_tool_link)

class_permissions(Document, [
    PERMISSION_OCR_DOCUMENT,
])
