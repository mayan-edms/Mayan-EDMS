from __future__ import unicode_literals

import logging

from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from acls.api import class_permissions
from common.utils import encapsulate
from documents.models import Document, DocumentVersion
from documents.signals import post_version_upload
from documents.widgets import document_link
from main.api import register_maintenance_links
from navigation.api import register_links, register_model_list_columns
from navigation.links import link_spacer
from project_tools.api import register_tool
from rest_api.classes import APIEndPoint

from .links import (
    link_document_all_ocr_cleanup, link_document_submit,
    link_document_submit_multiple, link_entry_delete,
    link_entry_delete_multiple, link_entry_list, link_entry_re_queue,
    link_entry_re_queue_multiple
)
from .models import DocumentVersionOCRError
from .permissions import PERMISSION_OCR_DOCUMENT
from .tasks import task_do_ocr

logger = logging.getLogger(__name__)

register_links(Document, [link_document_submit])
register_links([Document], [link_document_submit_multiple, link_spacer], menu_name='multi_item_links')

register_links([DocumentVersionOCRError], [link_entry_re_queue_multiple, link_entry_delete_multiple], menu_name='multi_item_links')
register_links([DocumentVersionOCRError], [link_entry_re_queue, link_entry_delete])
register_links(['ocr:entry_list', 'ocr:entry_delete_multiple', 'ocr:entry_re_queue_multiple', DocumentVersionOCRError], [link_entry_list], menu_name='secondary_menu')
register_maintenance_links([link_document_all_ocr_cleanup], namespace='ocr', title=_('OCR'))


def document_ocr_submit(self):
    task_do_ocr.apply_async(args=[self.latest_version.pk], queue='ocr')


def document_version_ocr_submit(self):
    task_do_ocr.apply_async(args=[self.pk], queue='ocr')


@receiver(post_version_upload, dispatch_uid='post_version_upload_ocr', sender=DocumentVersion)
def post_version_upload_ocr(sender, instance, **kwargs):
    logger.debug('received post_version_upload')
    logger.debug('instance pk: %s', instance.pk)
    if instance.document.document_type.ocr:
        instance.submit_for_ocr()


Document.add_to_class('submit_for_ocr', document_ocr_submit)
DocumentVersion.add_to_class('submit_for_ocr', document_version_ocr_submit)

class_permissions(Document, [PERMISSION_OCR_DOCUMENT])

register_tool(link_entry_list)

APIEndPoint('ocr')

register_model_list_columns(DocumentVersionOCRError, [
    {
        'name': _('Document'), 'attribute': encapsulate(lambda entry: document_link(entry.document_version.document))
    },
    {
        'name': _('Added'), 'attribute': 'datetime_submitted'
    },
    {
        'name': _('Result'), 'attribute': 'result'
    },
])
