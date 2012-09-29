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
from maintenance.api import MaintenanceNamespace
from acls.api import class_permissions
from job_processor.models import JobQueue, JobType
from job_processor.exceptions import JobQueuePushError

from .settings import AUTOMATIC_OCR
from .api import do_document_ocr
from .permissions import PERMISSION_OCR_DOCUMENT
from .exceptions import AlreadyQueued
from .literals import OCR_QUEUE_NAME
from .links import (submit_document, ocr_disable,
    ocr_enable, all_document_ocr_cleanup, ocr_log,
    ocr_tool_link, submit_document_multiple)

logger = logging.getLogger(__name__)
ocr_job_queue = None


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
                instance.submit_for_ocr()
            except JobQueuePushError:
                pass


bind_links([Document], [submit_document])

#namespace = MaintenanceNamespace(label=_(u'OCR'))
#namespace.create_tool(all_document_ocr_cleanup)

register_multi_item_links(['folder_view', 'search', 'results', 'index_instance_node_view', 'document_find_duplicates', 'document_type_document_list', 'document_group_view', 'document_list', 'document_list_recent'], [submit_document_multiple])

class_permissions(Document, [
    PERMISSION_OCR_DOCUMENT,
])

create_ocr_job_queue()
ocr_job_type = JobType('ocr', _(u'OCR'), do_document_ocr)

Document.add_to_class('submit_for_ocr', lambda document: ocr_job_queue.push(ocr_job_type, document_version_pk=document.latest_version.pk))
DocumentVersion.add_to_class('submit_for_ocr', lambda document_version: ocr_job_queue.push(ocr_job_type, document_version_pk=document_version.pk))
