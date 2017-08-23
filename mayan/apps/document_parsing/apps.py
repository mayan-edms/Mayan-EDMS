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

from .handlers import handler_parse_document_version
from .links import (
    link_document_content, link_entry_list, link_document_content_errors_list,
    link_document_content_download
)
from .permissions import permission_content_view

logger = logging.getLogger(__name__)


class DocumentParsingApp(MayanAppConfig):
    has_tests = True
    name = 'document_parsing'
    verbose_name = _('Document parsing')

    def ready(self):
        super(DocumentParsingApp, self).ready()

        APIEndPoint(app=self, version_string='1')

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        DocumentType = apps.get_model(
            app_label='documents', model_name='DocumentType'
        )

        DocumentVersion = apps.get_model(
            app_label='documents', model_name='DocumentVersion'
        )

        DocumentVersionParseError = self.get_model('DocumentVersionParseError')

        ModelPermission.register(
            model=Document, permissions=(permission_content_view,)
        )

        SourceColumn(
            source=DocumentVersionParseError, label=_('Document'),
            func=lambda context: document_link(context['object'].document_version.document)
        )
        SourceColumn(
            source=DocumentVersionParseError, label=_('Added'),
            attribute='datetime_submitted'
        )
        SourceColumn(
            source=DocumentVersionParseError, label=_('Result'),
            attribute='result'
        )

        document_search.add_model_field(
            field='versions__pages__content__content', label=_('Content')
        )

        document_page_search.add_model_field(
            field='content__content', label=_('Content')
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
            links=(
                link_document_content, link_document_ocr_erros_list,
                link_document_ocr_download
            ),
            sources=(
                'document_parsing:document_content',
                'document_parsing:document_ocr_error_list',
                'document_parsing:document_ocr_download',
            )
        )
        menu_secondary.bind_links(
            links=(link_entry_list,),
            sources=(
                'document_parsing:entry_list',
                'document_parsing:entry_delete_multiple',
                'document_parsing:entry_re_queue_multiple',
                DocumentVersionParseError
            )
        )
        menu_tools.bind_links(
            links=(
                link_entry_list
            )
        )

        post_version_upload.connect(
            dispatch_uid='document_parsing_handler_parse_document_version',
            receiver=handler_parse_document_version,
            sender=DocumentVersion
        )
