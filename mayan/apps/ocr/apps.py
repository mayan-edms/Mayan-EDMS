from __future__ import unicode_literals

import logging

from kombu import Exchange, Queue

from django.apps import apps
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from acls import ModelPermission
from common import (
    MayanAppConfig, menu_facet, menu_multi_item, menu_object, menu_secondary,
    menu_tools
)
from common.settings import settings_db_sync_task_delay
from documents.search import document_search, document_page_search
from documents.signals import post_version_upload
from documents.widgets import document_link
from mayan.celery import app
from navigation import SourceColumn
from rest_api.classes import APIEndPoint

from .handlers import initialize_new_ocr_settings, post_version_upload_ocr
from .links import (
    link_document_content, link_document_submit, link_document_submit_all,
    link_document_submit_multiple, link_document_type_ocr_settings,
    link_document_type_submit, link_entry_list
)
from .permissions import permission_ocr_document, permission_ocr_content_view

logger = logging.getLogger(__name__)


def document_ocr_submit(self):
    from .tasks import task_do_ocr

    task_do_ocr.apply_async(args=(self.latest_version.pk,))


def document_version_ocr_submit(self):
    from .tasks import task_do_ocr

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

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        DocumentType = apps.get_model(
            app_label='documents', model_name='DocumentType'
        )

        DocumentVersion = apps.get_model(
            app_label='documents', model_name='DocumentVersion'
        )

        DocumentVersionOCRError = self.get_model('DocumentVersionOCRError')

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
            field='versions__pages__ocr_content__content', label=_('OCR')
        )

        document_page_search.add_model_field(
            field='ocr_content__content', label=_('OCR')
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
