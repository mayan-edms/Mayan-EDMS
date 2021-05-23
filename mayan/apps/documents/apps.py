from django.apps import apps
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.acls.permissions import permission_acl_edit, permission_acl_view
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.classes import (
    MissingItem, ModelCopy, ModelField, ModelFieldRelated, ModelProperty,
    ModelQueryFields
)
from mayan.apps.common.menus import (
    menu_facet, menu_list_facet, menu_main, menu_object, menu_return,
    menu_secondary, menu_setup, menu_multi_item
)
from mayan.apps.common.signals import signal_post_initial_setup
from mayan.apps.converter.classes import AppImageErrorImage
from mayan.apps.converter.layers import layer_decorations
from mayan.apps.converter.links import link_transformation_list
from mayan.apps.converter.permissions import (
    permission_transformation_create,
    permission_transformation_delete, permission_transformation_edit,
    permission_transformation_view,
)
from mayan.apps.dashboards.dashboards import dashboard_main
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.events.permissions import permission_events_view
from mayan.apps.file_caching.links import link_cache_partition_purge
from mayan.apps.file_caching.permissions import permission_cache_partition_purge
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.rest_api.fields import DynamicSerializerField
from mayan.apps.templating.classes import AJAXTemplate
from mayan.apps.views.html_widgets import TwoStateWidget

from .dashboard_widgets import (
    DashboardWidgetDocumentFilePagesTotal, DashboardWidgetDocumentsInTrash,
    DashboardWidgetDocumentsNewThisMonth,
    DashboardWidgetDocumentsPagesNewThisMonth, DashboardWidgetDocumentsTotal,
    DashboardWidgetDocumentsTypesTotal,
)

# Documents

from .events import (
    event_document_created, event_document_edited, event_document_viewed,
    event_trashed_document_deleted, event_trashed_document_restored
)

# Document files

from .events import (
    event_document_file_created, event_document_file_deleted,
    event_document_file_downloaded, event_document_file_edited
)

# Document types

from .events import (
    event_document_type_changed, event_document_type_edited,
    event_document_type_quick_label_created,
    event_document_type_quick_label_deleted,
    event_document_type_quick_label_edited
)

# Document versions

from .events import (
    event_document_version_created, event_document_version_deleted,
    event_document_version_edited, event_document_version_exported,
    event_document_version_page_created, event_document_version_page_deleted,
    event_document_version_page_edited,
)

from .handlers import (
    handler_create_default_document_type,
    handler_create_document_file_page_image_cache,
    handler_create_document_version_page_image_cache
)
from .html_widgets import ThumbnailWidget
from .links.document_links import (
    link_document_type_change, link_document_properties_edit,
    link_document_list, link_document_recently_accessed_list,
    link_document_recently_created_list, link_document_multiple_type_change,
    link_document_preview, link_document_properties
)
from .links.document_file_links import (
    link_document_file_delete, link_document_file_delete_multiple,
    link_document_file_download_quick, link_document_file_edit,
    link_document_file_list, link_document_file_preview,
    link_document_file_print_form, link_document_file_properties,
    link_document_file_return_to_document, link_document_file_return_list,
    link_document_file_transformations_clear,
    link_document_file_multiple_transformations_clear,
    link_document_file_transformations_clone
)
from .links.document_file_page_links import (
    link_document_file_multiple_page_count_update,
    link_document_file_page_count_update, link_document_file_page_list,
    link_document_file_page_navigation_first,
    link_document_file_page_navigation_last,
    link_document_file_page_navigation_next,
    link_document_file_page_navigation_previous,
    link_document_file_page_return_to_document,
    link_document_file_page_return_to_document_file,
    link_document_file_page_return_to_document_file_page_list,
    link_document_file_page_rotate_left, link_document_file_page_rotate_right,
    link_document_file_page_view, link_document_file_page_view_reset,
    link_document_file_page_zoom_in, link_document_file_page_zoom_out
)
from .links.document_type_links import (
    link_document_type_create, link_document_type_delete,
    link_document_type_edit, link_document_type_filename_create,
    link_document_type_filename_delete, link_document_type_filename_edit,
    link_document_type_filename_list, link_document_type_filename_generator,
    link_document_type_list, link_document_type_policies,
    link_document_type_setup
)
from .links.document_version_links import (
    link_document_version_active, link_document_version_create,
    link_document_version_delete, link_document_version_edit,
    link_document_version_export, link_document_version_list,
    link_document_version_multiple_delete, link_document_version_return_list,
    link_document_version_return_to_document, link_document_version_preview,
    link_document_version_print_form,
    link_document_version_transformations_clear,
    link_document_version_multiple_transformations_clear,
    link_document_version_transformations_clone
)
from .links.document_version_page_links import (
    link_document_version_page_delete, link_document_version_page_list,
    link_document_version_page_list_remap,
    link_document_version_page_list_reset,
    link_document_version_page_navigation_first,
    link_document_version_page_navigation_last,
    link_document_version_page_navigation_next,
    link_document_version_page_navigation_previous,
    link_document_version_page_return_to_document,
    link_document_version_page_return_to_document_version,
    link_document_version_page_return_to_document_version_page_list,
    link_document_version_page_rotate_left,
    link_document_version_page_rotate_right, link_document_version_page_view,
    link_document_version_page_view_reset,
    link_document_version_page_zoom_in, link_document_version_page_zoom_out
)
from .links.favorite_links import (
    link_document_favorites_add, link_document_favorites_remove,
    link_document_list_favorites, link_document_multiple_favorites_add,
    link_document_multiple_favorites_remove
)
from .links.trashed_document_links import (
    link_document_delete, link_document_list_deleted,
    link_document_multiple_delete, link_document_multiple_restore,
    link_document_multiple_trash, link_document_restore, link_document_trash,
    link_trash_can_empty
)
from .literals import (
    IMAGE_ERROR_NO_ACTIVE_VERSION, IMAGE_ERROR_NO_VERSION_PAGES
)
from .menus import menu_documents

# Documents

from .permissions import (
    permission_document_create, permission_document_edit,
    permission_document_properties_edit, permission_document_tools,
    permission_document_trash, permission_document_view
)

# DocumentFile

from .permissions import (
    permission_document_file_delete, permission_document_file_download,
    permission_document_file_edit, permission_document_file_new,
    permission_document_file_print, permission_document_file_tools,
    permission_document_file_view
)

# DocumentType

from .permissions import (
    permission_document_type_delete, permission_document_type_edit,
    permission_document_type_view
)

# DocumentVersion

from .permissions import (
    permission_document_version_create, permission_document_version_delete,
    permission_document_version_edit, permission_document_version_export,
    permission_document_version_print, permission_document_version_view
)

# TrashedDocument

from .permissions import (
    permission_trashed_document_delete, permission_trashed_document_restore
)

from .statistics import *  # NOQA


class DocumentsApp(MayanAppConfig):
    app_namespace = 'documents'
    app_url = 'documents'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.documents'
    verbose_name = _('Documents')

    def ready(self):
        super().ready()

        Document = self.get_model(model_name='Document')
        DocumentSearchResult = self.get_model(
            model_name='DocumentSearchResult'
        )
        DocumentFile = self.get_model(model_name='DocumentFile')
        DocumentFilePage = self.get_model(model_name='DocumentFilePage')
        DocumentFileSearchResult = self.get_model(
            model_name='DocumentFileSearchResult'
        )
        DocumentFilePageSearchResult = self.get_model(
            model_name='DocumentFilePageSearchResult'
        )
        DocumentType = self.get_model(model_name='DocumentType')
        DocumentTypeFilename = self.get_model(
            model_name='DocumentTypeFilename'
        )
        DocumentVersion = self.get_model(model_name='DocumentVersion')
        DocumentVersionSearchResult = self.get_model(
            model_name='DocumentVersionSearchResult'
        )
        DocumentVersionPage = self.get_model(model_name='DocumentVersionPage')
        DocumentVersionPageSearchResult = self.get_model(
            model_name='DocumentVersionPageSearchResult'
        )
        DownloadFile = apps.get_model(
            app_label='storage', model_name='DownloadFile'
        )
        FavoriteDocument = self.get_model(
            model_name='FavoriteDocument'
        )
        RecentlyAccessedDocument = self.get_model(
            model_name='RecentlyAccessedDocument'
        )
        RecentlyCreatedDocument = self.get_model(
            model_name='RecentlyCreatedDocument'
        )
        TrashedDocument = self.get_model(model_name='TrashedDocument')

        AppImageErrorImage(
            name=IMAGE_ERROR_NO_ACTIVE_VERSION,
            template_name='documents/errors/no_valid_version.html'
        )
        AppImageErrorImage(
            name=IMAGE_ERROR_NO_VERSION_PAGES,
            template_name='documents/errors/no_version_pages.html'
        )

        AJAXTemplate(
            name='invalid_document',
            template_name='documents/invalid_document.html'
        )

        link_decorations_list = link_transformation_list.copy(
            layer=layer_decorations
        )
        link_decorations_list.text = _('Decorations')

        DownloadFile.objects.register_content_object(model=Document)

        DynamicSerializerField.add_serializer(
            klass=Document,
            serializer_class='mayan.apps.documents.serializers.document_serializers.DocumentSerializer'
        )

        EventModelRegistry.register(model=Document)
        EventModelRegistry.register(model=DocumentFile)
        EventModelRegistry.register(model=DocumentFilePage)
        EventModelRegistry.register(model=DocumentType)
        EventModelRegistry.register(model=DocumentTypeFilename)
        EventModelRegistry.register(model=DocumentVersion)
        EventModelRegistry.register(model=DocumentVersionPage)
        EventModelRegistry.register(model=TrashedDocument)

        MissingItem(
            label=_('Create a document type'),
            description=_(
                'Every uploaded document must be assigned a document type, '
                'it is the basic way Mayan EDMS categorizes documents.'
            ), condition=lambda: not DocumentType.objects.exists(),
            view='documents:document_type_list'
        )

        ModelCopy(model=DocumentTypeFilename).add_fields(
            field_names=(
                'document_type', 'filename', 'enabled'
            )
        )
        ModelCopy(
            model=DocumentType, bind_link=True, register_permission=True
        ).add_fields(
            field_names=(
                'label', 'trash_time_period', 'trash_time_unit',
                'delete_time_period', 'delete_time_unit', 'filenames'
            )
        )
        ModelCopy(
            model=DocumentVersion, bind_link=True, register_permission=True
        ).add_fields(
            field_names=(
                'document', 'timestamp', 'comment', 'version_pages',
            )
        )
        ModelCopy(
            model=DocumentVersionPage, bind_link=True, register_permission=True
        ).add_fields(
            field_names=(
                'document_version', 'page_number', 'content_type', 'object_id',
            )
        )

        ModelEventType.register(
            model=Document, event_types=(
                event_document_edited, event_document_type_changed,
                event_document_file_deleted, event_document_version_deleted,
                event_document_viewed, event_trashed_document_restored
            )
        )
        ModelEventType.register(
            model=DocumentFile, event_types=(
                event_document_file_created, event_document_file_downloaded,
                event_document_file_edited
            )
        )
        ModelEventType.register(
            model=DocumentType, event_types=(
                event_document_created,
                event_document_type_edited,
                event_document_type_quick_label_created,
                event_trashed_document_deleted
            )
        )
        ModelEventType.register(
            model=DocumentTypeFilename, event_types=(
                event_document_type_quick_label_deleted,
                event_document_type_quick_label_edited
            )
        )
        ModelEventType.register(
            model=DocumentVersion, event_types=(
                event_document_version_created,
                event_document_version_edited,
                event_document_version_exported,
                event_document_version_page_created
            )
        )
        ModelEventType.register(
            model=DocumentVersionPage, event_types=(
                event_document_version_page_deleted,
                event_document_version_page_edited
            )
        )

        ModelField(model=Document, name='description')
        ModelField(model=Document, name='datetime_created')
        ModelField(model=Document, name='trashed_date_time')
        ModelField(
            model=Document, name='document_type'
        )
        ModelField(model=Document, name='in_trash')
        ModelField(model=Document, name='is_stub')
        ModelField(model=Document, name='label')
        ModelField(model=Document, name='language')
        ModelField(model=Document, name='uuid')

        ModelFieldRelated(model=Document, name='document_type__label')
        ModelFieldRelated(
            model=Document,
            name='files__checksum'
        )
        ModelFieldRelated(
            model=Document, label=_('File comments'),
            name='files__comment'
        )
        ModelFieldRelated(
            model=Document, label=_('File encodings'),
            name='files__encoding'
        )
        ModelFieldRelated(
            model=Document, label=_('File MIME types'),
            name='files__mimetype'
        )
        ModelFieldRelated(
            model=Document, label=_('File timestamps'),
            name='files__timestamp'
        )

        ModelField(
            model=DocumentFilePage, label=_('Document file'),
            name='document_file'
        )
        ModelField(
            model=DocumentFilePage, label=_('Page number'),
            name='page_number'
        )

        ModelProperty(
            description=_('Return the latest file of the document.'),
            model=Document, label=_('Latest file'), name='latest_file'
        )
        ModelProperty(
            description=_('Return the document instance.'),
            model=DocumentFilePage, label=_('Document'), name='document'
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_document_edit, permission_document_file_new,
                permission_document_properties_edit,
                permission_document_tools,
                permission_document_trash, permission_document_view,
                permission_document_version_create, permission_events_view,
                permission_trashed_document_delete,
                permission_trashed_document_restore,
            )
        )
        ModelPermission.register(
            model=DocumentFile, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_cache_partition_purge,
                permission_document_file_delete,
                permission_document_file_download,
                permission_document_file_edit,
                permission_document_file_print,
                permission_document_file_tools,
                permission_document_file_view,
                permission_events_view, permission_transformation_create,
                permission_transformation_delete,
                permission_transformation_edit,
                permission_transformation_view
            )
        )
        ModelPermission.register(
            model=DocumentType, permissions=(
                permission_document_create, permission_document_type_delete,
                permission_document_type_edit, permission_document_type_view,
                permission_acl_edit, permission_acl_view,
                permission_events_view,
            )
        )
        ModelPermission.register(
            model=DocumentVersion, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_cache_partition_purge,
                permission_document_version_delete,
                permission_document_version_edit,
                permission_document_version_export,
                permission_document_version_print,
                permission_document_version_view,
                permission_events_view, permission_transformation_create,
                permission_transformation_delete,
                permission_transformation_edit,
                permission_transformation_view
            )
        )

        ModelPermission.register_inheritance(
            model=Document, related='document_type',
        )
        ModelPermission.register_inheritance(
            model=DocumentFile, related='document',
        )
        ModelPermission.register_inheritance(
            model=DocumentFile, related='document__document_type',
        )
        ModelPermission.register_inheritance(
            model=DocumentFilePage, related='document_file',
        )
        ModelPermission.register_inheritance(
            model=DocumentVersion, related='document',
        )
        ModelPermission.register_inheritance(
            model=DocumentVersion, related='document__document_type',
        )
        ModelPermission.register_inheritance(
            model=RecentlyAccessedDocument, related='document',
        )
        ModelPermission.register_inheritance(
            model=DocumentVersionPage, related='document_version',
        )
        ModelPermission.register_inheritance(
            model=DocumentTypeFilename, related='document_type',
        )
        ModelPermission.register_inheritance(
            model=FavoriteDocument, related='document',
        )

        model_query_fields_document = ModelQueryFields(model=Document)
        model_query_fields_document.add_prefetch_related_field(
            field_name='files'
        )
        model_query_fields_document.add_prefetch_related_field(
            field_name='files__file_pages'
        )
        model_query_fields_document.add_select_related_field(
            field_name='document_type'
        )

        model_query_fields_document_file = ModelQueryFields(model=DocumentFile)
        model_query_fields_document_file.add_prefetch_related_field(
            field_name='file_pages'
        )
        model_query_fields_document_file.add_select_related_field(
            field_name='document'
        )

        model_query_fields_document_file_page = ModelQueryFields(
            model=DocumentFilePage
        )
        model_query_fields_document_file_page.add_select_related_field(
            field_name='document_file'
        )

        model_query_fields_document_version = ModelQueryFields(
            model=DocumentVersion
        )
        model_query_fields_document_version.add_prefetch_related_field(
            field_name='version_pages'
        )
        model_query_fields_document_version.add_select_related_field(
            field_name='document'
        )

        # Document

        SourceColumn(
            attribute='get_label', is_object_absolute_url=True,
            is_identifier=True, is_sortable=True, sort_field='label',
            source=Document
        )
        SourceColumn(
            html_extra_classes='text-center document-thumbnail-list',
            label=_('Thumbnail'), order=-99, source=Document,
            widget=ThumbnailWidget
        )

        SourceColumn(
            attribute='document_type', include_label=True, is_sortable=True,
            label=_('Type'), order=-9, source=Document
        )
        SourceColumn(
            func=lambda context: context['object'].pages.count(),
            label=_('Pages'), include_label=True, order=-8, source=Document
        )

        # RecentlyCreatedDocument

        SourceColumn(
            attribute='datetime_created', include_label=True,
            is_sortable=True, source=RecentlyCreatedDocument
        )

        # DocumentFile

        SourceColumn(
            source=DocumentFile, attribute='filename', is_identifier=True,
            is_object_absolute_url=True
        )
        SourceColumn(
            html_extra_classes='text-center document-thumbnail-list',
            label=_('Thumbnail'), order=-99, source=DocumentFile,
            widget=ThumbnailWidget
        )
        SourceColumn(
            func=lambda context: context['object'].pages.count(),
            include_label=True, label=_('Pages'), order=-6,
            source=DocumentFile
        )
        SourceColumn(
            attribute='comment', is_sortable=True, order=-7,
            source=DocumentFile
        )
        SourceColumn(
            attribute='encoding', include_label=True, is_sortable=True,
            order=-8, source=DocumentFile
        )
        SourceColumn(
            attribute='mimetype', include_label=True, is_sortable=True,
            order=-9, source=DocumentFile
        )

        # DocumentFilePage

        SourceColumn(
            attribute='get_label', is_identifier=True,
            is_object_absolute_url=True, source=DocumentFilePage,
        )
        SourceColumn(
            html_extra_classes='text-center document-thumbnail-list',
            label=_('Thumbnail'), order=-99, source=DocumentFilePage,
            widget=ThumbnailWidget
        )

        # DocumentType

        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=DocumentType
        )

        SourceColumn(
            func=lambda context: context['object'].get_document_count(
                user=context['request'].user
            ), include_label=True, label=_('Documents'), source=DocumentType
        )

        SourceColumn(
            attribute='filename', is_identifier=True, is_sortable=True,
            source=DocumentTypeFilename
        )
        SourceColumn(
            attribute='enabled', include_label=True, is_sortable=True,
            source=DocumentTypeFilename, widget=TwoStateWidget
        )

        # DocumentVersion

        SourceColumn(
            source=DocumentVersion, attribute='get_label', is_identifier=True,
            is_object_absolute_url=True
        )
        SourceColumn(
            html_extra_classes='text-center document-thumbnail-list',
            label=_('Thumbnail'), order=-99, source=DocumentVersion,
            widget=ThumbnailWidget
        )
        SourceColumn(
            func=lambda context: context['object'].pages.count(),
            include_label=True, label=_('Pages'), order=-8,
            source=DocumentVersion
        )
        SourceColumn(
            attribute='active', include_label=True, is_sortable=True,
            order=-9, source=DocumentVersion, widget=TwoStateWidget
        )
        SourceColumn(
            attribute='comment', include_label=True, is_sortable=True,
            order=-7, source=DocumentVersion
        )

        # DocumentVersionPage

        SourceColumn(
            attribute='get_label', is_identifier=True,
            is_object_absolute_url=True, source=DocumentVersionPage,
        )
        SourceColumn(
            html_extra_classes='text-center document-thumbnail-list',
            label=_('Thumbnail'), order=-99, source=DocumentVersionPage,
            widget=ThumbnailWidget
        )

        # TrashedDocument

        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=TrashedDocument
        )
        SourceColumn(
            attribute='trashed_date_time', include_label=True, order=99,
            source=TrashedDocument
        )

        dashboard_main.add_widget(
            widget=DashboardWidgetDocumentsTotal, order=0
        )
        dashboard_main.add_widget(
            widget=DashboardWidgetDocumentFilePagesTotal, order=1
        )
        dashboard_main.add_widget(
            widget=DashboardWidgetDocumentsInTrash, order=2
        )
        dashboard_main.add_widget(
            widget=DashboardWidgetDocumentsTypesTotal, order=3
        )
        dashboard_main.add_widget(
            widget=DashboardWidgetDocumentsNewThisMonth, order=4
        )
        dashboard_main.add_widget(
            widget=DashboardWidgetDocumentsPagesNewThisMonth, order=5
        )

        menu_documents.bind_links(
            links=(
                link_document_recently_accessed_list,
                link_document_recently_created_list, link_document_list_favorites,
                link_document_list, link_document_list_deleted
            )
        )

        menu_main.bind_links(links=(menu_documents,), position=0)

        menu_setup.bind_links(links=(link_document_type_setup,))

        # Document

        menu_facet.bind_links(
            links=(link_acl_list,), sources=(Document,)
        )
        menu_facet.bind_links(
            links=(link_document_preview,), sources=(Document,), position=0
        )
        menu_facet.bind_links(
            links=(link_document_properties,), sources=(Document,), position=2
        )
        menu_facet.bind_links(
            links=(
                link_document_file_list, link_document_version_list
            ), sources=(Document,), position=2
        )

        menu_object.bind_links(
            links=(
                link_document_favorites_add, link_document_favorites_remove,
                link_document_properties_edit, link_document_type_change,
                link_document_trash
            ), sources=(Document,)
        )

        menu_multi_item.bind_links(
            links=(
                link_document_multiple_favorites_add,
                link_document_multiple_favorites_remove,
                link_document_multiple_trash,
                link_document_multiple_type_change
            ), sources=(Document,)
        )

        menu_secondary.bind_links(
            links=(link_document_version_create,),
            sources=(
                'documents:document_version_create',
                'documents:document_version_list'
            )
        )

        # DocumentFile

        menu_list_facet.bind_links(
            links=(
                link_document_file_page_list, link_document_file_properties,
                link_document_file_preview, link_acl_list
            ), sources=(DocumentFile,)
        )
        menu_multi_item.bind_links(
            links=(
                link_document_file_delete_multiple,
                link_document_file_multiple_page_count_update,
                link_document_file_multiple_transformations_clear,
            ), sources=(DocumentFile,)
        )
        menu_object.bind_links(
            links=(
                link_cache_partition_purge,
                link_document_file_delete,
                link_document_file_download_quick,
                link_document_file_edit,
                link_document_file_page_count_update,
                link_document_file_print_form,
                link_document_file_transformations_clear,
                link_document_file_transformations_clone
            ),
            sources=(DocumentFile,)
        )
        menu_return.bind_links(
            links=(
                link_document_file_return_list,
                link_document_file_return_to_document,
            ), sources=(DocumentFile,)
        )

        # DocumentFilePages

        menu_facet.add_unsorted_source(source=DocumentFilePage)
        menu_facet.bind_links(
            links=(
                link_document_file_page_rotate_left,
                link_document_file_page_rotate_right, link_document_file_page_zoom_in,
                link_document_file_page_zoom_out, link_document_file_page_view_reset
            ), sources=('documents:document_file_page_view',)
        )
        menu_facet.bind_links(
            links=(
                link_document_file_page_view,
                link_document_file_page_navigation_first,
                link_document_file_page_navigation_previous,
                link_document_file_page_navigation_next,
                link_document_file_page_navigation_last
            ), sources=(DocumentFilePage,)
        )
        menu_list_facet.bind_links(
            links=(link_decorations_list, link_transformation_list),
            sources=(DocumentFilePage,)
        )
        menu_return.bind_links(
            links=(
                link_document_file_page_return_to_document,
                link_document_file_page_return_to_document_file,
                link_document_file_page_return_to_document_file_page_list
            ),
            sources=(DocumentFilePage,)
        )

        # DocumentType

        menu_list_facet.bind_links(
            links=(
                link_document_type_filename_list,
                link_document_type_policies,
                link_document_type_filename_generator, link_acl_list
            ), sources=(DocumentType,)
        )

        menu_object.bind_links(
            links=(
                link_document_type_delete, link_document_type_edit
            ), sources=(DocumentType,)
        )
        menu_object.bind_links(
            links=(
                link_document_type_filename_edit,
                link_document_type_filename_delete
            ), sources=(DocumentTypeFilename,)
        )
        menu_secondary.bind_links(
            links=(link_document_type_list, link_document_type_create),
            sources=(
                DocumentType, 'documents:document_type_create',
                'documents:document_type_list'
            )
        )
        menu_secondary.bind_links(
            links=(link_document_type_filename_create,),
            sources=(
                DocumentTypeFilename, 'documents:document_type_filename_list',
                'documents:document_type_filename_create'
            )
        )
        menu_secondary.bind_links(
            links=(link_trash_can_empty,),
            sources=(
                'documents:document_list_deleted', 'documents:trash_can_empty'
            )
        )

        # DocumentVersion

        menu_list_facet.bind_links(
            links=(
                link_document_version_page_list,
                link_document_version_preview, link_acl_list
            ),
            sources=(DocumentVersion,)
        )
        menu_multi_item.bind_links(
            links=(
                link_document_version_multiple_delete,
                link_document_version_multiple_transformations_clear,
            ), sources=(DocumentVersion,)
        )
        menu_object.bind_links(
            links=(
                link_document_version_active,
                link_cache_partition_purge,
                link_document_version_delete, link_document_version_edit,
                link_document_version_export,
                link_document_version_page_list_remap,
                link_document_version_page_list_reset,
                link_document_version_print_form,
                link_document_version_transformations_clear,
                link_document_version_transformations_clone
            ),
            sources=(DocumentVersion,)
        )
        menu_return.bind_links(
            links=(
                link_document_version_return_list,
                link_document_version_return_to_document,
            ), sources=(DocumentVersion,)
        )

        # DocumentVersionPage

        menu_facet.add_unsorted_source(source=DocumentVersionPage)
        menu_facet.bind_links(
            links=(
                link_document_version_page_rotate_left,
                link_document_version_page_rotate_right, link_document_version_page_zoom_in,
                link_document_version_page_zoom_out, link_document_version_page_view_reset
            ), sources=('documents:document_version_page_view',)
        )
        menu_facet.bind_links(
            links=(link_document_version_page_view,),
            sources=(DocumentVersionPage,)
        )
        menu_facet.bind_links(
            links=(
                link_document_version_page_navigation_first,
                link_document_version_page_navigation_previous,
                link_document_version_page_navigation_next,
                link_document_version_page_navigation_last
            ), sources=(DocumentVersionPage,)
        )
        menu_list_facet.bind_links(
            links=(
                link_decorations_list, link_transformation_list,
            ), sources=(DocumentVersionPage, DocumentVersionPageSearchResult)
        )
        menu_object.bind_links(
            links=(
                link_document_version_page_delete,
            ), sources=(DocumentVersionPage, DocumentVersionPageSearchResult)
        )
        menu_return.bind_links(
            links=(
                link_document_version_page_return_to_document,
                link_document_version_page_return_to_document_version,
                link_document_version_page_return_to_document_version_page_list
            ), sources=(DocumentVersionPage,)
        )

        # Trashed documents

        menu_object.bind_links(
            links=(link_document_restore, link_document_delete),
            sources=(TrashedDocument,)
        )
        menu_multi_item.bind_links(
            links=(
                link_document_multiple_restore, link_document_multiple_delete
            ), sources=(TrashedDocument,)
        )

        # RecentlyAccessedDocument

        menu_multi_item.add_proxy_inclusions(source=RecentlyAccessedDocument)

        # RecentlyCreatedDocument

        menu_multi_item.add_proxy_inclusions(source=RecentlyCreatedDocument)

        # Search proxies

        menu_multi_item.add_proxy_inclusions(source=DocumentSearchResult)
        menu_multi_item.add_proxy_inclusions(source=DocumentFileSearchResult)
        menu_multi_item.add_proxy_inclusions(source=DocumentFilePageSearchResult)
        menu_multi_item.add_proxy_inclusions(source=DocumentVersionSearchResult)
        menu_multi_item.add_proxy_inclusions(source=DocumentVersionPageSearchResult)

        post_migrate.connect(
            dispatch_uid='documents_handler_create_document_file_page_image_cache',
            receiver=handler_create_document_file_page_image_cache,
        )
        post_migrate.connect(
            dispatch_uid='documents_handler_create_document_version_page_image_cache',
            receiver=handler_create_document_version_page_image_cache,
        )
        signal_post_initial_setup.connect(
            dispatch_uid='documents_handler_create_default_document_type',
            receiver=handler_create_default_document_type
        )
