from __future__ import absolute_import

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from south.signals import post_migrate

from acls.api import class_permissions
from documents.models import Document, DocumentVersion
from main.api import register_maintenance_links
from navigation.api import register_links, register_multi_item_links
from project_tools.api import register_tool

from .links import (all_document_ocr_cleanup, ocr_tool_link,
                    queue_document_list, queue_document_multiple_delete,
                    re_queue_multiple_document, submit_document,
                    submit_document_multiple)
from .models import DocumentQueue
from .permissions import PERMISSION_OCR_DOCUMENT
from .settings import AUTOMATIC_OCR
from .tasks import task_do_ocr

logger = logging.getLogger(__name__)

register_links(Document, [submit_document])
register_multi_item_links(['folders:folder_view', 'indexing:index_instance_node_view', 'documents:document_type_document_list', 'search:search', 'search:results', 'linking:document_group_view', 'documents:document_list', 'document:document_list_recent', 'tags:tag_tagged_item_list'], [submit_document_multiple])
register_multi_item_links(['ocr:queue_document_list'], [re_queue_multiple_document, queue_document_multiple_delete])
register_links(['ocr:queue_document_list'], [queue_document_list], menu_name='secondary_menu')

register_maintenance_links([all_document_ocr_cleanup], namespace='ocr', title=_(u'OCR'))


def document_ocr_submit(self):
    task_do_ocr.apply_async(args=[self.pk], queue='ocr')


@receiver(post_save, dispatch_uid='document_post_save', sender=DocumentVersion)
def document_post_save(sender, instance, **kwargs):
    logger.debug('received post save signal')
    logger.debug('instance: %s' % instance)
    if kwargs.get('created', False):
        if AUTOMATIC_OCR:
            instance.document.submit_for_ocr()


@receiver(post_migrate, dispatch_uid='create_default_queue')
def create_default_queue_signal_handler(sender, **kwargs):
    if kwargs['app'] == 'ocr':
        DocumentQueue.objects.get_or_create(name='default')


Document.add_to_class('submit_for_ocr', document_ocr_submit)

class_permissions(Document, [PERMISSION_OCR_DOCUMENT])

register_tool(ocr_tool_link)
