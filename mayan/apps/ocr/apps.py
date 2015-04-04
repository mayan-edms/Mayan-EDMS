from __future__ import unicode_literals

import logging

import sh

from django import apps
from django.utils.translation import ugettext_lazy as _

from acls.api import class_permissions
from common import menu_multi_item, menu_object, menu_secondary, menu_tools
from common.utils import encapsulate
from documents.models import Document, DocumentVersion
from documents.signals import post_version_upload
from documents.widgets import document_link
from installation import PropertyNamespace
from main.api import register_maintenance_links
from navigation.api import register_model_list_columns
from rest_api.classes import APIEndPoint

from .links import (
    link_document_all_ocr_cleanup, link_document_submit,
    link_document_submit_multiple, link_entry_delete,
    link_entry_delete_multiple, link_entry_list, link_entry_re_queue,
    link_entry_re_queue_multiple
)
from .models import DocumentVersionOCRError
from .permissions import PERMISSION_OCR_DOCUMENT
from .settings import PDFTOTEXT_PATH, TESSERACT_PATH, UNPAPER_PATH
from .tasks import task_do_ocr

logger = logging.getLogger(__name__)


def document_ocr_submit(self):
    task_do_ocr.apply_async(args=[self.latest_version.pk], queue='ocr')


def document_version_ocr_submit(self):
    task_do_ocr.apply_async(args=[self.pk], queue='ocr')


def post_version_upload_ocr(sender, instance, **kwargs):
    logger.debug('received post_version_upload')
    logger.debug('instance pk: %s', instance.pk)
    if instance.document.document_type.ocr:
        instance.submit_for_ocr()


class OCRApp(apps.AppConfig):
    name = 'ocr'
    verbose_name = _('OCR')

    def ready(self):
        APIEndPoint('ocr')

        Document.add_to_class('submit_for_ocr', document_ocr_submit)
        DocumentVersion.add_to_class('submit_for_ocr', document_version_ocr_submit)

        class_permissions(Document, [PERMISSION_OCR_DOCUMENT])

        menu_multi_item.bind_links(links=[link_document_submit_multiple], sources=[Document])
        menu_multi_item.bind_links(links=[link_entry_re_queue_multiple, link_entry_delete_multiple], sources=[DocumentVersionOCRError])
        menu_object.bind_links(links=[link_document_submit], sources=[Document])
        menu_object.bind_links(links=[link_entry_re_queue, link_entry_delete], sources=[DocumentVersionOCRError])
        menu_secondary.bind_links(links=[link_entry_list], sources=['ocr:entry_list', 'ocr:entry_delete_multiple', 'ocr:entry_re_queue_multiple', DocumentVersionOCRError])
        menu_tools.bind_links(links=[link_entry_list])

        post_version_upload.connect(post_version_upload_ocr, dispatch_uid='post_version_upload_ocr', sender=DocumentVersion)

        namespace = PropertyNamespace('ocr', _('OCR'))

        try:
            pdftotext = sh.Command(PDFTOTEXT_PATH)
        except sh.CommandNotFound:
            namespace.add_property('pdftotext', _('pdftotext version'), _('not found'), report=True)
        except Exception:
            namespace.add_property('pdftotext', _('pdftotext version'), _('error getting version'), report=True)
        else:
            namespace.add_property('pdftotext', _('pdftotext version'), pdftotext('-v').stderr, report=True)

        try:
            tesseract = sh.Command(TESSERACT_PATH)
        except sh.CommandNotFound:
            namespace.add_property('tesseract', _('tesseract version'), _('not found'), report=True)
        except Exception:
            namespace.add_property('tesseract', _('tesseract version'), _('error getting version'), report=True)
        else:
            namespace.add_property('tesseract', _('tesseract version'), tesseract('-v').stderr, report=True)

        try:
            unpaper = sh.Command(UNPAPER_PATH)
        except sh.CommandNotFound:
            namespace.add_property('unpaper', _('unpaper version'), _('not found'), report=True)
        except Exception:
            namespace.add_property('unpaper', _('unpaper version'), _('error getting version'), report=True)
        else:
            namespace.add_property('unpaper', _('unpaper version'), unpaper('-V').stdout, report=True)

        register_maintenance_links([link_document_all_ocr_cleanup], namespace='ocr', title=_('OCR'))

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
