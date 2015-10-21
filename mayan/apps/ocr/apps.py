from __future__ import unicode_literals

import logging

from kombu import Exchange, Queue
import sh

from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from acls import ModelPermission
from common import (
    MayanAppConfig, menu_facet, menu_multi_item, menu_object, menu_secondary,
    menu_tools
)
from common.settings import settings_db_sync_task_delay
from documents.models import Document, DocumentType, DocumentVersion
from documents.search import document_search
from documents.signals import post_version_upload
from documents.widgets import document_link
from installation import PropertyNamespace
from mayan.celery import app
from navigation import SourceColumn
from rest_api.classes import APIEndPoint

from .handlers import initialize_new_ocr_settings, post_version_upload_ocr
from .links import (
    link_document_content, link_document_submit, link_document_submit_all,
    link_document_submit_multiple, link_document_type_ocr_settings,
    link_document_type_submit, link_entry_list
)
from .models import DocumentVersionOCRError
from .permissions import permission_ocr_document, permission_ocr_content_view
from .settings import (
    setting_pdftotext_path, setting_tesseract_path
)
from .tasks import task_do_ocr

logger = logging.getLogger(__name__)


def document_ocr_submit(self):
    task_do_ocr.apply_async(args=(self.latest_version.pk,))


def document_version_ocr_submit(self):
    task_do_ocr.apply_async(
        kwargs={'document_version_pk': self.pk},
        countdown=settings_db_sync_task_delay.value
    )


class OCRApp(MayanAppConfig):
    name = 'ocr'
    test = True
    verbose_name = _('OCR')

    def ready(self):
        super(OCRApp, self).ready()

        APIEndPoint(app=self, version_string='1')

        Document.add_to_class('submit_for_ocr', document_ocr_submit)
        DocumentVersion.add_to_class(
            'submit_for_ocr', document_version_ocr_submit
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_ocr_document, permission_ocr_content_view
            )
        )

        SourceColumn(
            source=DocumentVersionOCRError, label=_('Document'),
            func=lambda context: document_link(context['object'].document_version.document)
        )
        SourceColumn(
            source=DocumentVersionOCRError, label=_('Added'),
            attribute='datetime_submitted'
        )
        SourceColumn(
            source=DocumentVersionOCRError, label=_('Result'),
            attribute='result'
        )

        app.conf.CELERY_QUEUES.append(
            Queue('ocr', Exchange('ocr'), routing_key='ocr'),
        )

        app.conf.CELERY_ROUTES.update(
            {
                'ocr.tasks.task_do_ocr': {
                    'queue': 'ocr'
                },
            }
        )

        document_search.add_model_field(
            field='versions__pages__ocr_content__content', label=_('Content')
        )

        menu_facet.bind_links(
            links=(link_document_content,), sources=(Document,)
        )
        menu_multi_item.bind_links(
            links=(link_document_submit_multiple,), sources=(Document,)
        )
        menu_object.bind_links(
            links=(link_document_submit,), sources=(Document,)
        )
        menu_object.bind_links(
            links=(link_document_type_ocr_settings,), sources=(DocumentType,)
        )
        menu_secondary.bind_links(
            links=(link_entry_list,),
            sources=(
                'ocr:entry_list', 'ocr:entry_delete_multiple',
                'ocr:entry_re_queue_multiple', DocumentVersionOCRError
            )
        )
        menu_tools.bind_links(
            links=(
                link_document_submit_all, link_document_type_submit,
                link_entry_list
            )
        )

        post_save.connect(
            initialize_new_ocr_settings,
            dispatch_uid='initialize_new_ocr_settings', sender=DocumentType
        )
        post_version_upload.connect(
            post_version_upload_ocr, dispatch_uid='post_version_upload_ocr',
            sender=DocumentVersion
        )

        namespace = PropertyNamespace('ocr', _('OCR'))

        try:
            pdftotext = sh.Command(setting_pdftotext_path.value)
        except sh.CommandNotFound:
            namespace.add_property(
                'pdftotext', _('pdftotext version'), _('not found'),
                report=True
            )
        except Exception:
            namespace.add_property(
                'pdftotext', _('pdftotext version'),
                _('error getting version'), report=True
            )
        else:
            namespace.add_property(
                'pdftotext', _('pdftotext version'), pdftotext('-v').stderr,
                report=True
            )

        try:
            tesseract = sh.Command(setting_tesseract_path.value)
        except sh.CommandNotFound:
            namespace.add_property(
                'tesseract', _('tesseract version'), _('not found'),
                report=True
            )
        except Exception:
            namespace.add_property(
                'tesseract', _('tesseract version'),
                _('error getting version'), report=True
            )
        else:
            namespace.add_property(
                'tesseract', _('tesseract version'), tesseract('-v').stderr,
                report=True
            )
