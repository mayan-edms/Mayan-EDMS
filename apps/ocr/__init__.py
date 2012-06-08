from __future__ import absolute_import

import logging

from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.db.models.signals import post_save, post_syncdb
from django.dispatch import receiver
from django.db.utils import DatabaseError

from navigation.api import bind_links, register_multi_item_links, Link
from documents.models import Document, DocumentVersion
from main.api import register_maintenance_links
from project_tools.api import register_tool
from acls.api import class_permissions

from scheduler.api import register_interval_job

from .conf.settings import (AUTOMATIC_OCR, QUEUE_PROCESSING_INTERVAL)
from .models import DocumentQueue, QueueTransformation
from .tasks import task_process_document_queues
from .permissions import (PERMISSION_OCR_DOCUMENT,
    PERMISSION_OCR_DOCUMENT_DELETE, PERMISSION_OCR_QUEUE_ENABLE_DISABLE,
    PERMISSION_OCR_CLEAN_ALL_PAGES)
from .exceptions import AlreadyQueued
from . import models as ocr_models

logger = logging.getLogger(__name__)

#Links
submit_document = Link(text=_('submit to OCR queue'), view='submit_document', args='object.id', sprite='hourglass_add', permissions=[PERMISSION_OCR_DOCUMENT])
submit_document_multiple = Link(text=_('submit to OCR queue'), view='submit_document_multiple', sprite='hourglass_add', permissions=[PERMISSION_OCR_DOCUMENT])
re_queue_document = Link(text=_('re-queue'), view='re_queue_document', args='object.id', sprite='hourglass_add', permissions=[PERMISSION_OCR_DOCUMENT])
re_queue_multiple_document = Link(text=_('re-queue'), view='re_queue_multiple_document', sprite='hourglass_add', permissions=[PERMISSION_OCR_DOCUMENT])
queue_document_delete = Link(text=_(u'delete'), view='queue_document_delete', args='object.id', sprite='hourglass_delete', permissions=[PERMISSION_OCR_DOCUMENT_DELETE])
queue_document_multiple_delete = Link(text=_(u'delete'), view='queue_document_multiple_delete', sprite='hourglass_delete', permissions=[PERMISSION_OCR_DOCUMENT_DELETE])

document_queue_disable = Link(text=_(u'stop queue'), view='document_queue_disable', args='queue.id', sprite='control_stop_blue', permissions=[PERMISSION_OCR_QUEUE_ENABLE_DISABLE])
document_queue_enable = Link(text=_(u'activate queue'), view='document_queue_enable', args='queue.id', sprite='control_play_blue', permissions=[PERMISSION_OCR_QUEUE_ENABLE_DISABLE])

all_document_ocr_cleanup = Link(text=_(u'clean up pages content'), view='all_document_ocr_cleanup', sprite='text_strikethrough', permissions=[PERMISSION_OCR_CLEAN_ALL_PAGES], description=_(u'Runs a language filter to remove common OCR mistakes from document pages content.'))

queue_document_list = Link(text=_(u'queue document list'), view='queue_document_list', sprite='hourglass', permissions=[PERMISSION_OCR_DOCUMENT])
ocr_tool_link = Link(text=_(u'OCR'), view='queue_document_list', sprite='hourglass', icon='text.png', permissions=[PERMISSION_OCR_DOCUMENT], children_view_regex=[r'queue_', r'document_queue'])

setup_queue_transformation_list = Link(text=_(u'transformations'), view='setup_queue_transformation_list', args='queue.pk', sprite='shape_move_front')
setup_queue_transformation_create = Link(text=_(u'add transformation'), view='setup_queue_transformation_create', args='queue.pk', sprite='shape_square_add')
setup_queue_transformation_edit = Link(text=_(u'edit'), view='setup_queue_transformation_edit', args='transformation.pk', sprite='shape_square_edit')
setup_queue_transformation_delete = Link(text=_(u'delete'), view='setup_queue_transformation_delete', args='transformation.pk', sprite='shape_square_delete')

bind_links([Document], [submit_document])
bind_links([DocumentQueue], [document_queue_disable, document_queue_enable, setup_queue_transformation_list])
bind_links([QueueTransformation], [setup_queue_transformation_edit, setup_queue_transformation_delete])

register_multi_item_links(['queue_document_list'], [re_queue_multiple_document, queue_document_multiple_delete])

bind_links(['setup_queue_transformation_create', 'setup_queue_transformation_edit', 'setup_queue_transformation_delete', 'document_queue_disable', 'document_queue_enable', 'queue_document_list', 'setup_queue_transformation_list'], [queue_document_list], menu_name='secondary_menu')
bind_links(['setup_queue_transformation_edit', 'setup_queue_transformation_delete', 'setup_queue_transformation_list', 'setup_queue_transformation_create'], [setup_queue_transformation_create], menu_name='sidebar')

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

# Disabled because it appears Django execute signals using the same
# process of the signal emiter effectively blocking the view until
# the OCR process completes which could take several minutes :/
#@receiver(post_save, dispatch_uid='call_queue', sender=QueueDocument)
#def call_queue(sender, **kwargs):
#    if kwargs.get('created', False):
#        logger.debug('got call_queue signal: %s' % kwargs)
#        task_process_document_queues()


@receiver(post_syncdb, dispatch_uid='create_default_queue', sender=ocr_models)
def create_default_queue_signal_handler(sender, **kwargs):
    create_default_queue()

register_interval_job('task_process_document_queues', _(u'Checks the OCR queue for pending documents.'), task_process_document_queues, seconds=QUEUE_PROCESSING_INTERVAL)

register_tool(ocr_tool_link)

class_permissions(Document, [
    PERMISSION_OCR_DOCUMENT,
])
