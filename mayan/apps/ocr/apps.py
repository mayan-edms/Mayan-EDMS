import logging

from django.apps import apps
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.classes import ModelFieldRelated, ModelProperty
from mayan.apps.common.menus import (
    menu_list_facet, menu_multi_item, menu_secondary, menu_tools
)
from mayan.apps.documents.signals import signal_post_document_version_remap
from mayan.apps.events.classes import ModelEventType
from mayan.apps.navigation.classes import SourceColumn

from .events import (
    event_ocr_document_version_content_deleted,
    event_ocr_document_version_finished, event_ocr_document_version_submitted
)
from .handlers import (
    handler_index_document_version, handler_initialize_new_ocr_settings,
    handler_ocr_document_version,
)
from .links import (
    link_document_version_page_ocr_content_detail_view,
    link_document_version_ocr_content_view,
    link_document_version_ocr_content_delete,
    link_document_version_multiple_ocr_content_delete,
    link_document_version_ocr_download,
    link_document_version_ocr_errors_list, link_document_version_ocr_submit,
    link_document_version_multiple_ocr_submit,
    link_document_type_ocr_settings,
    link_document_type_submit, link_entry_list
)
from .methods import (
    method_document_ocr_submit, method_document_version_ocr_submit
)
from .permissions import (
    permission_document_type_ocr_setup, permission_document_version_ocr,
    permission_document_version_ocr_content_view
)
from .signals import signal_post_document_version_ocr
from .utils import get_instance_ocr_content

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

        DocumentVersionOCRError = self.get_model(
            model_name='DocumentVersionOCRError'
        )

        Document.add_to_class(
            name='ocr_content', value=get_instance_ocr_content
        )
        Document.add_to_class(
            name='submit_for_ocr', value=method_document_ocr_submit
        )
        DocumentVersion.add_to_class(
            name='ocr_content', value=get_instance_ocr_content
        )
        DocumentVersion.add_to_class(
            name='submit_for_ocr', value=method_document_version_ocr_submit
        )

        ModelEventType.register(
            model=Document, event_types=(
                event_ocr_document_version_content_deleted,
                event_ocr_document_version_finished,
                event_ocr_document_version_submitted
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

        SourceColumn(
            attribute='document_version__document',
            is_attribute_absolute_url=True, is_identifier=True,
            is_sortable=True, source=DocumentVersionOCRError
        )
        SourceColumn(
            attribute='datetime_submitted', is_sortable=True,
            label=_('Date and time'), source=DocumentVersionOCRError
        )
        SourceColumn(
            source=DocumentVersionOCRError, label=_('Result'),
            attribute='result'
        )

        menu_list_facet.bind_links(
            links=(link_document_version_ocr_content_view,),
            sources=(DocumentVersion,)
        )
        menu_list_facet.bind_links(
            links=(link_document_version_page_ocr_content_detail_view,),
            sources=(DocumentVersionPage,)
        )
        menu_list_facet.bind_links(
            links=(link_document_type_ocr_settings,), sources=(DocumentType,)
        )
        menu_multi_item.bind_links(
            links=(
                link_document_version_multiple_ocr_content_delete,
                link_document_version_multiple_ocr_submit,
            ), sources=(DocumentVersion,)
        )
        menu_secondary.bind_links(
            links=(
                link_document_version_ocr_content_delete,
                link_document_version_ocr_errors_list,
                link_document_version_ocr_download,
                link_document_version_ocr_submit
            ),
            sources=(
                'ocr:document_version_ocr_content_view_delete',
                'ocr:document_version_ocr_content_view',
                'ocr:document_version_ocr_download',
                'ocr:document_version_ocr_error_list',
                'ocr:document_version_ocr_submit',
            )
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
                link_document_type_submit, link_entry_list
            )
        )

        post_save.connect(
            dispatch_uid='ocr_handler_initialize_new_ocr_settings',
            receiver=handler_initialize_new_ocr_settings,
            sender=DocumentType
        )
        signal_post_document_version_ocr.connect(
            dispatch_uid='ocr_handler_index_document_version',
            receiver=handler_index_document_version,
            sender=DocumentVersion
        )
        signal_post_document_version_remap.connect(
            dispatch_uid='ocr_handler_ocr_document_version',
            receiver=handler_ocr_document_version,
            sender=DocumentVersion
        )
