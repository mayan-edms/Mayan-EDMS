from __future__ import unicode_literals

from django.apps import apps
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.classes import ModelAttribute, ModelField
from mayan.apps.common.menus import (
    menu_facet, menu_list_facet, menu_multi_item, menu_object, menu_secondary,
    menu_tools
)
from mayan.apps.document_indexing.handlers import handler_index_document
from mayan.apps.documents.search import document_page_search, document_search
from mayan.apps.documents.signals import post_version_upload
from mayan.apps.events.classes import ModelEventType
from mayan.apps.navigation.classes import SourceColumn

from .classes import FileMetadataHelper
from .dependencies import *  # NOQA
from .drivers import *  # NOQA
from .events import (
    event_file_metadata_document_version_finish,
    event_file_metadata_document_version_submit
)
from .handlers import (
    handler_initialize_new_document_type_settings,
    handler_process_document_version
)
from .links import (
    link_document_driver_list, link_document_file_metadata_list,
    link_document_submit, link_document_multiple_submit,
    link_document_type_file_metadata_settings, link_document_type_submit
)
from .methods import (
    method_document_submit, method_document_version_submit,
    method_get_document_file_metadata,
    method_get_document_version_file_metadata
)
from .permissions import (
    permission_document_type_file_metadata_setup,
    permission_file_metadata_submit, permission_file_metadata_view
)
from .signals import post_document_version_file_metadata_processing


class FileMetadataApp(MayanAppConfig):
    app_namespace = 'file_metadata'
    app_url = 'file_metadata'
    has_tests = True
    name = 'mayan.apps.file_metadata'
    verbose_name = _('File metadata')

    def ready(self):
        super(FileMetadataApp, self).ready()

        FileMetadataEntry = self.get_model(model_name='FileMetadataEntry')
        DocumentVersionDriverEntry = self.get_model(
            model_name='DocumentVersionDriverEntry'
        )
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        DocumentTypeSettings = self.get_model(
            model_name='DocumentTypeSettings'
        )
        DocumentType = apps.get_model(
            app_label='documents', model_name='DocumentType'
        )
        DocumentVersion = apps.get_model(
            app_label='documents', model_name='DocumentVersion'
        )

        Document.add_to_class(
            name='file_metadata_value_of', value=FileMetadataHelper.constructor
        )
        Document.add_to_class(
            name='get_file_metadata',
            value=method_get_document_file_metadata
        )
        Document.add_to_class(
            name='submit_for_file_metadata_processing',
            value=method_document_submit
        )
        DocumentVersion.add_to_class(
            name='get_file_metadata',
            value=method_get_document_version_file_metadata
        )
        DocumentVersion.add_to_class(
            name='submit_for_file_metadata_processing',
            value=method_document_version_submit
        )

        ModelAttribute(
            model=Document, name='file_metadata_value_of',
            description=_(
                'Return the value of a specific file metadata.'
            )
        )

        ModelEventType.register(
            model=Document, event_types=(
                event_file_metadata_document_version_finish,
                event_file_metadata_document_version_submit
            )
        )

        ModelField(
            label=_('File metadata key'), model=Document,
            name='versions__file_metadata_drivers__entries__key',
        )
        ModelField(
            label=_('File metadata key'), model=Document,
            name='versions__file_metadata_drivers__entries__value',
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_file_metadata_submit, permission_file_metadata_view,
            )
        )
        ModelPermission.register(
            model=DocumentType, permissions=(
                permission_document_type_file_metadata_setup,
                permission_file_metadata_submit,
                permission_file_metadata_view
            )
        )
        ModelPermission.register_inheritance(
            model=DocumentTypeSettings, related='document_type',
        )
        ModelPermission.register_inheritance(
            model=DocumentVersionDriverEntry, related='document_version',
        )

        SourceColumn(attribute='key', source=FileMetadataEntry)
        SourceColumn(attribute='value', source=FileMetadataEntry)
        SourceColumn(
            attribute='driver', source=DocumentVersionDriverEntry
        )
        SourceColumn(
            attribute='driver__internal_name',
            source=DocumentVersionDriverEntry
        )
        SourceColumn(
            attribute='get_attribute_count', source=DocumentVersionDriverEntry
        )

        document_search.add_model_field(
            field='versions__file_metadata_drivers__entries__key',
            label=_('File metadata key')
        )
        document_search.add_model_field(
            field='versions__file_metadata_drivers__entries__value',
            label=_('File metadata value')
        )

        document_page_search.add_model_field(
            field='document_version__file_metadata_drivers__entries__key',
            label=_('File metadata key')
        )
        document_page_search.add_model_field(
            field='document_version__file_metadata_drivers__entries__value',
            label=_('File metadata value')
        )

        menu_facet.bind_links(
            links=(link_document_driver_list,), sources=(Document,)
        )
        menu_list_facet.bind_links(
            links=(link_document_type_file_metadata_settings,),
            sources=(DocumentType,)
        )
        menu_object.bind_links(
            links=(link_document_file_metadata_list,),
            sources=(DocumentVersionDriverEntry,)
        )
        menu_multi_item.bind_links(
            links=(link_document_multiple_submit,), sources=(Document,)
        )
        menu_secondary.bind_links(
            links=(link_document_submit,), sources=(
                'file_metadata:document_driver_list',
                'file_metadata:document_version_driver_file_metadata_list'
            )
        )
        menu_tools.bind_links(
            links=(link_document_type_submit,),
        )
        post_save.connect(
            dispatch_uid='file_metadata_handler_initialize_new_document_type_settings',
            receiver=handler_initialize_new_document_type_settings,
            sender=DocumentType
        )
        post_version_upload.connect(
            dispatch_uid='file_metadata_handler_process_document_version',
            receiver=handler_process_document_version, sender=DocumentVersion
        )
        post_document_version_file_metadata_processing.connect(
            dispatch_uid='file_metadata_handler_index_document',
            receiver=handler_index_document,
            sender=DocumentVersion
        )
