import logging

from django.apps import apps
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.classes import ModelFieldRelated, ModelProperty
from mayan.apps.common.menus import (
    menu_facet, menu_list_facet, menu_multi_item, menu_secondary, menu_tools
)
from mayan.apps.documents.search import document_search, document_page_search
from mayan.apps.documents.signals import post_version_upload
from mayan.apps.events.classes import ModelEventType
from mayan.apps.navigation.classes import SourceColumn

from .events import (
    event_parsing_document_content_deleted,
    event_parsing_document_version_submit,
    event_parsing_document_version_finish
)
from .handlers import (
    handler_index_document, handler_initialize_new_parsing_settings,
    handler_parse_document_version
)
from .links import (
    link_document_content, link_document_content_delete,
    link_document_content_delete_multiple, link_document_page_content,
    link_document_content_download, link_document_parsing_errors_list,
    link_document_submit_multiple, link_document_submit,
    link_document_type_parsing_settings, link_document_type_submit,
    link_error_list
)
from .methods import (
    method_document_parsing_submit, method_document_version_parsing_submit
)
from .permissions import (
    permission_content_view, permission_document_type_parsing_setup,
    permission_parse_document
)
from .signals import post_document_version_parsing
from .utils import get_instance_content

logger = logging.getLogger(name=__name__)


class DocumentParsingApp(MayanAppConfig):
    app_namespace = 'document_parsing'
    app_url = 'parsing'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.document_parsing'
    verbose_name = _('Document parsing')

    def ready(self):
        super(DocumentParsingApp, self).ready()

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        DocumentPage = apps.get_model(
            app_label='documents', model_name='DocumentPage'
        )
        DocumentType = apps.get_model(
            app_label='documents', model_name='DocumentType'
        )
        DocumentTypeSettings = self.get_model(
            model_name='DocumentTypeSettings'
        )
        DocumentVersion = apps.get_model(
            app_label='documents', model_name='DocumentVersion'
        )
        DocumentVersionParseError = self.get_model(
            model_name='DocumentVersionParseError'
        )

        Document.add_to_class(
            name='content', value=get_instance_content
        )
        Document.add_to_class(
            name='submit_for_parsing', value=method_document_parsing_submit
        )
        DocumentVersion.add_to_class(
            name='content', value=get_instance_content
        )
        DocumentVersion.add_to_class(
            name='submit_for_parsing',
            value=method_document_version_parsing_submit
        )

        ModelEventType.register(
            model=Document, event_types=(
                event_parsing_document_content_deleted,
                event_parsing_document_version_submit,
                event_parsing_document_version_finish
            )
        )

        ModelFieldRelated(
            model=Document, name='versions__version_pages__content__content'
        )

        ModelProperty(
            description=_(
                'A generator returning the document\'s pages parsed content.'
            ), label=_('Content'), model=Document,
            name='content'
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_content_view, permission_parse_document
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
            attribute='document_version__document',
            is_attribute_absolute_url=True, is_identifier=True,
            is_sortable=True, source=DocumentVersionParseError
        )
        SourceColumn(
            attribute='datetime_submitted', is_sortable=True,
            source=DocumentVersionParseError
        )
        SourceColumn(
            source=DocumentVersionParseError, label=_('Result'),
            attribute='result'
        )

        document_search.add_model_field(
            field='versions__version_pages__content__content', label=_('Content')
        )

        document_page_search.add_model_field(
            field='content__content', label=_('Content')
        )

        menu_facet.bind_links(
            links=(link_document_content,), sources=(Document,)
        )
        menu_facet.bind_links(
            links=(link_document_page_content,), sources=(DocumentPage,)
        )
        menu_list_facet.bind_links(
            links=(link_document_type_parsing_settings,),
            sources=(DocumentType,)
        )
        menu_multi_item.bind_links(
            links=(
                link_document_content_delete_multiple,
                link_document_submit_multiple,
            ), sources=(Document,)
        )
        menu_secondary.bind_links(
            links=(
                link_document_content_delete,
                link_document_content_download,
                link_document_parsing_errors_list,
                link_document_submit
            ),
            sources=(
                'document_parsing:document_content',
                'document_parsing:document_content_delete',
                'document_parsing:document_content_download',
                'document_parsing:document_parsing_error_list',
                'document_parsing:document_submit',
            )
        )
        menu_tools.bind_links(
            links=(
                link_document_type_submit, link_error_list,
            )
        )

        post_document_version_parsing.connect(
            dispatch_uid='document_parsing_handler_index_document',
            receiver=handler_index_document,
            sender=DocumentVersion
        )
        post_save.connect(
            dispatch_uid='document_parsing_handler_initialize_new_parsing_settings',
            receiver=handler_initialize_new_parsing_settings,
            sender=DocumentType
        )
        post_version_upload.connect(
            dispatch_uid='document_parsing_handler_parse_document_version',
            receiver=handler_parse_document_version,
            sender=DocumentVersion
        )
