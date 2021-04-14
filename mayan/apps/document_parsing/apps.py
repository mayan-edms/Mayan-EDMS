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
from mayan.apps.documents.signals import signal_post_document_file_upload
from mayan.apps.events.classes import ModelEventType
from mayan.apps.navigation.classes import SourceColumn

from .events import (
    event_parsing_document_file_content_deleted,
    event_parsing_document_file_submit,
    event_parsing_document_file_finish
)
from .handlers import (
    handler_index_document, handler_initialize_new_parsing_settings,
    handler_parse_document_file
)
from .links import (
    link_document_file_content, link_document_file_content_delete,
    link_document_file_multiple_content_delete, link_document_file_page_content,
    link_document_file_content_download, link_document_file_parsing_errors_list,
    link_document_file_multiple_submit, link_document_file_submit,
    link_document_type_parsing_settings, link_document_type_submit,
    link_error_list
)
from .methods import (
    method_document_parsing_submit, method_document_file_parsing_submit
)
from .permissions import (
    permission_document_file_content_view, permission_document_type_parsing_setup,
    permission_document_file_parse
)
from .signals import signal_post_document_file_parsing
from .utils import get_document_file_content

logger = logging.getLogger(name=__name__)


class DocumentParsingApp(MayanAppConfig):
    app_namespace = 'document_parsing'
    app_url = 'parsing'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.document_parsing'
    verbose_name = _('Document parsing')

    def ready(self):
        super().ready()

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        DocumentFile = apps.get_model(
            app_label='documents', model_name='DocumentFile'
        )
        DocumentFileParseError = self.get_model(
            model_name='DocumentFileParseError'
        )
        DocumentFilePage = apps.get_model(
            app_label='documents', model_name='DocumentFilePage'
        )
        DocumentType = apps.get_model(
            app_label='documents', model_name='DocumentType'
        )
        DocumentTypeSettings = self.get_model(
            model_name='DocumentTypeSettings'
        )

        Document.add_to_class(
            name='content', value=get_document_file_content
        )
        Document.add_to_class(
            name='submit_for_parsing', value=method_document_parsing_submit
        )
        DocumentFile.add_to_class(
            name='content', value=get_document_file_content
        )
        DocumentFile.add_to_class(
            name='submit_for_parsing',
            value=method_document_file_parsing_submit
        )

        ModelEventType.register(
            model=DocumentFile, event_types=(
                event_parsing_document_file_content_deleted,
                event_parsing_document_file_submit,
                event_parsing_document_file_finish
            )
        )

        ModelFieldRelated(
            model=Document, name='files__file_pages__content__content'
        )

        ModelProperty(
            description=_(
                'A generator returning the document file\'s pages parsed content.'
            ), label=_('Content'), model=Document,
            name='content'
        )

        ModelPermission.register(
            model=DocumentFile, permissions=(
                permission_document_file_content_view,
                permission_document_file_parse
            )
        )
        ModelPermission.register(
            model=DocumentType, permissions=(
                permission_document_type_parsing_setup,
            )
        )
        ModelPermission.register_inheritance(
            model=DocumentTypeSettings, related='document_type',
        )

        SourceColumn(
            attribute='document_file__document',
            is_attribute_absolute_url=True, is_identifier=True,
            is_sortable=True, source=DocumentFileParseError
        )
        SourceColumn(
            attribute='datetime_submitted', is_sortable=True,
            source=DocumentFileParseError
        )
        SourceColumn(
            source=DocumentFileParseError, label=_('Result'),
            attribute='result'
        )

        menu_list_facet.bind_links(
            links=(link_document_file_content,), sources=(DocumentFile,)
        )
        menu_list_facet.bind_links(
            links=(link_document_file_page_content,),
            sources=(DocumentFilePage,)
        )
        menu_list_facet.bind_links(
            links=(link_document_type_parsing_settings,),
            sources=(DocumentType,)
        )
        menu_multi_item.bind_links(
            links=(
                link_document_file_multiple_content_delete,
                link_document_file_multiple_submit,
            ), sources=(DocumentFile,)
        )
        menu_secondary.bind_links(
            links=(
                link_document_file_content_delete,
                link_document_file_content_download,
                link_document_file_parsing_errors_list,
                link_document_file_submit
            ),
            sources=(
                'document_parsing:document_file_content_view',
                'document_parsing:document_file_content_delete',
                'document_parsing:document_file_content_download',
                'document_parsing:document_file_parsing_error_list',
                'document_parsing:document_file_submit',
            )
        )
        menu_tools.bind_links(
            links=(
                link_document_type_submit, link_error_list,
            )
        )

        post_save.connect(
            dispatch_uid='document_parsing_handler_initialize_new_parsing_settings',
            receiver=handler_initialize_new_parsing_settings,
            sender=DocumentType
        )
        signal_post_document_file_parsing.connect(
            dispatch_uid='document_parsing_handler_index_document',
            receiver=handler_index_document,
            sender=DocumentFile
        )
        signal_post_document_file_upload.connect(
            dispatch_uid='document_parsing_handler_parse_document_file',
            receiver=handler_parse_document_file,
            sender=DocumentFile
        )
