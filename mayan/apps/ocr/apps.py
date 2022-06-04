import logging

from django.apps import apps
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import (
    menu_list_facet, menu_multi_item, menu_secondary, menu_tools
)
from mayan.apps.databases.classes import ModelFieldRelated, ModelProperty
from mayan.apps.documents.signals import signal_post_document_version_remap
from mayan.apps.events.classes import ModelEventType
from mayan.apps.logging.classes import ErrorLog

from .events import (
    event_ocr_document_version_content_deleted,
    event_ocr_document_version_page_content_edited,
    event_ocr_document_version_finished, event_ocr_document_version_submitted
)
from .handlers import (
    handler_initialize_new_ocr_settings, handler_ocr_document_version
)
from .links import (
    link_document_version_page_ocr_content_detail_view,
    link_document_version_page_ocr_content_edit_view,
    link_document_version_ocr_content_detail,
    link_document_version_ocr_content_single_delete,
    link_document_version_ocr_content_multiple_delete,
    link_document_version_ocr_content_download,
    link_document_version_ocr_single_submit,
    link_document_version_ocr_multiple_submit,
    link_document_type_ocr_settings, link_document_type_submit
)
from .methods import (
    method_document_ocr_content, method_document_ocr_submit,
    method_document_version_ocr_content, method_document_version_ocr_submit
)
from .permissions import (
    permission_document_type_ocr_setup, permission_document_version_ocr,
    permission_document_version_ocr_content_edit,
    permission_document_version_ocr_content_view
)

logger = logging.getLogger(name=__name__)


class OCRApp(MayanAppConfig):
    app_namespace = 'ocr'
    app_url = 'ocr'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.ocr'
    verbose_name = _('OCR')

    def ready(self):
        super().ready()

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        DocumentType = apps.get_model(
            app_label='documents', model_name='DocumentType'
        )
        DocumentTypeOCRSettings = self.get_model(
            model_name='DocumentTypeOCRSettings'
        )
        DocumentVersion = apps.get_model(
            app_label='documents', model_name='DocumentVersion'
        )
        DocumentVersionPage = apps.get_model(
            app_label='documents', model_name='DocumentVersionPage'
        )

        Document.add_to_class(
            name='ocr_content', value=method_document_ocr_content
        )
        Document.add_to_class(
            name='submit_for_ocr', value=method_document_ocr_submit
        )
        DocumentVersion.add_to_class(
            name='ocr_content', value=method_document_version_ocr_content
        )
        DocumentVersion.add_to_class(
            name='submit_for_ocr', value=method_document_version_ocr_submit
        )

        ModelEventType.register(
            model=Document, event_types=(
                event_ocr_document_version_content_deleted,
                event_ocr_document_version_page_content_edited,
                event_ocr_document_version_finished,
                event_ocr_document_version_submitted
            )
        )
        ModelEventType.register(
            model=DocumentVersion, event_types=(
                event_ocr_document_version_content_deleted,
                event_ocr_document_version_page_content_edited,
                event_ocr_document_version_finished,
                event_ocr_document_version_submitted
            )
        )
        ModelEventType.register(
            model=DocumentVersionPage, event_types=(
                event_ocr_document_version_page_content_edited,
            )
        )

        ModelFieldRelated(
            model=Document,
            name='versions__version_pages__ocr_content__content'
        )
        ModelProperty(
            description=_('The OCR content.'), label='OCR content',
            model=DocumentVersionPage, name='ocr_content.content'
        )
        ModelProperty(
            description=_(
                'A generator returning the document\'s pages OCR content.'
            ), label=_('OCR content'), model=Document,
            name='ocr_content'
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_document_version_ocr,
                permission_document_version_ocr_content_edit,
                permission_document_version_ocr_content_view
            )
        )
        ModelPermission.register(
            model=DocumentType, permissions=(
                permission_document_type_ocr_setup,
            )
        )
        ModelPermission.register_inheritance(
            model=DocumentTypeOCRSettings, related='document_type',
        )

        error_log = ErrorLog(app_config=self)
        error_log.register_model(model=DocumentVersion)

        # Document type

        menu_list_facet.bind_links(
            links=(link_document_type_ocr_settings,), sources=(DocumentType,)
        )

        # Document version

        menu_list_facet.bind_links(
            links=(link_document_version_ocr_content_detail,),
            sources=(DocumentVersion,)
        )

        menu_multi_item.bind_links(
            links=(
                link_document_version_ocr_content_multiple_delete,
                link_document_version_ocr_multiple_submit
            ), sources=(DocumentVersion,)
        )

        menu_secondary.bind_links(
            links=(
                link_document_version_ocr_content_single_delete,
                link_document_version_ocr_content_download,
                link_document_version_ocr_single_submit
            ),
            sources=(
                'ocr:document_version_ocr_content_view_delete',
                'ocr:document_version_ocr_content_view',
                'ocr:document_version_ocr_content_download',
                'ocr:document_version_ocr_single_submit'
            )
        )

        # Document version page

        menu_list_facet.bind_links(
            links=(
                link_document_version_page_ocr_content_detail_view,
            ), sources=(DocumentVersionPage,)
        )

        menu_secondary.bind_links(
            links=(
                link_document_version_page_ocr_content_edit_view,
            ), sources=(
                'ocr:document_version_page_ocr_content_detail_view',
                'ocr:document_version_page_ocr_content_edit_view'
            )
        )

        menu_tools.bind_links(
            links=(
                link_document_type_submit,
            )
        )

        post_save.connect(
            dispatch_uid='ocr_handler_initialize_new_ocr_settings',
            receiver=handler_initialize_new_ocr_settings,
            sender=DocumentType
        )
        signal_post_document_version_remap.connect(
            dispatch_uid='ocr_handler_ocr_document_version',
            receiver=handler_ocr_document_version,
            sender=DocumentVersion
        )
