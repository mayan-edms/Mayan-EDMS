from django.db.models.signals import post_delete, post_migrate
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
    menu_facet, menu_list_facet, menu_main, menu_object, menu_related,
    menu_return, menu_secondary, menu_setup, menu_multi_item, menu_tools
)
from mayan.apps.common.signals import signal_post_initial_setup
from mayan.apps.converter.layers import layer_decorations
from mayan.apps.converter.links import link_transformation_list
from mayan.apps.converter.permissions import (
    permission_transformation_create,
    permission_transformation_delete, permission_transformation_edit,
    permission_transformation_view,
)
from mayan.apps.dashboards.dashboards import dashboard_main
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.events.links import (
    link_events_for_object, link_object_event_types_user_subcriptions_list,
)
from mayan.apps.events.permissions import permission_events_view
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.rest_api.fields import DynamicSerializerField
from mayan.apps.templating.classes import AJAXTemplate
from mayan.apps.views.html_widgets import TwoStateWidget

from .classes import *
from .dashboard_widgets import (
    DashboardWidgetDocumentFilePagesTotal, DashboardWidgetDocumentsInTrash,
    DashboardWidgetDocumentsNewThisMonth,
    DashboardWidgetDocumentsPagesNewThisMonth, DashboardWidgetDocumentsTotal,
    DashboardWidgetDocumentsTypesTotal,
)
from .events import (
    event_document_create, event_document_download,
    event_document_properties_edit, event_document_type_changed,
    event_document_type_created, event_document_type_edited,
    event_document_file_deleted, event_document_file_new,
    event_document_version_created, event_document_version_deleted,
    event_document_version_edited, event_document_viewed
)
from .handlers import (
    handler_create_default_document_type,
    handler_create_document_file_page_image_cache,
    handler_create_document_version_page_image_cache,
    handler_remove_empty_duplicates_lists, handler_scan_duplicates_for
)
from .links.document_links import (
    link_document_type_change, link_document_properties_edit,
    link_document_list, link_document_list_recent_access,
    link_document_list_recent_added, link_document_multiple_type_change,
    link_document_preview, link_document_properties
)
from .links.document_file_links import (
    link_document_file_cache_purge, link_document_file_delete,
    link_document_file_download, link_document_file_multiple_download,
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
    link_document_version_active, link_document_version_cache_purge,
    link_document_version_create, link_document_version_delete,
    link_document_version_edit, link_document_version_export,
    link_document_version_list, link_document_version_multiple_delete,
    link_document_version_return_list,
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
from .links.duplicated_document_links import (
    link_document_duplicates_list, link_duplicated_document_list,
    link_duplicated_document_scan
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

from .signals import signal_post_document_file_upload
from .statistics import *  # NOQA
from .widgets import (
    DocumentFilePageThumbnailWidget, DocumentVersionPageThumbnailWidget,
    widget_document_file_page_number, widget_document_page_number,
    widget_document_version_page_number
)


class DocumentsApp(MayanAppConfig):
    app_namespace = 'documents'
    app_url = 'documents'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.documents'
    verbose_name = _('Documents')

    def ready(self):
        super().ready()

        DeletedDocument = self.get_model(model_name='DeletedDocument')
        Document = self.get_model(model_name='Document')
        DocumentFile = self.get_model(model_name='DocumentFile')
        DocumentFilePage = self.get_model(model_name='DocumentFilePage')
        DocumentFilePageResult = self.get_model(model_name='DocumentFilePageResult')
        DocumentType = self.get_model(model_name='DocumentType')
        DocumentTypeFilename = self.get_model(model_name='DocumentTypeFilename')
        DocumentVersion = self.get_model(model_name='DocumentVersion')
        DocumentVersionPage = self.get_model(model_name='DocumentVersionPage')
        DuplicatedDocument = self.get_model(model_name='DuplicatedDocument')

        AJAXTemplate(
            name='invalid_document',
            template_name='documents/invalid_document.html'
        )

        link_decorations_list = link_transformation_list.copy(
            layer=layer_decorations
        )
        link_decorations_list.text = _('Decorations')

        DynamicSerializerField.add_serializer(
            klass=Document,
            serializer_class='mayan.apps.documents.serializers.document_serializers.DocumentSerializer'
        )

        EventModelRegistry.register(model=DeletedDocument)
        EventModelRegistry.register(model=Document)
        EventModelRegistry.register(model=DocumentFile)
        EventModelRegistry.register(model=DocumentType)
        EventModelRegistry.register(model=DocumentVersion)
        EventModelRegistry.register(model=DocumentVersionPage)

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
                event_document_download, event_document_properties_edit,
                event_document_type_changed, event_document_file_deleted,
                event_document_file_new, event_document_version_deleted,
                event_document_version_created, event_document_viewed
            )
        )
        ModelEventType.register(
            model=DocumentFile, event_types=(
                event_document_file_new,
            )
        )
        ModelEventType.register(
            model=DocumentType, event_types=(
                event_document_create,
                event_document_type_created,
                event_document_type_edited,
            )
        )
        ModelEventType.register(
            model=DocumentVersion, event_types=(
                event_document_version_deleted, event_document_version_edited
            )
        )
        ModelEventType.register(
            model=DocumentVersionPage, event_types=(
                event_document_version_edited,
            )
        )

        ModelField(model=Document, name='description')
        ModelField(model=Document, name='date_added')
        ModelField(model=Document, name='deleted_date_time')
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
            model=Document, label=_('Files comment'),
            name='files__comment'
        )
        ModelFieldRelated(
            model=Document, label=_('Files encoding'),
            name='files__encoding'
        )
        ModelFieldRelated(
            model=Document, label=_('Files mime type'),
            name='files__mimetype'
        )
        ModelFieldRelated(
            model=Document, label=_('Files timestamp'),
            name='files__timestamp'
        )

        ModelField(
            model=DocumentFilePage, label=_('Document file'),
            name='document_file'
        )
        ModelField(
            model=DocumentFilePage, label=_('Page number'), name='page_number'
        )

        ModelProperty(
            description=_('Return the lastest file of the document.'),
            model=Document, label=_('Latest file'), name='latest_file'
        )
        ModelProperty(
            description=_('Return the document instance.'),
            model=DocumentFilePage, label=_('Document'), name='document'
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_trashed_document_delete, permission_document_edit,
                permission_document_file_new,
                permission_document_properties_edit,
                permission_trashed_document_restore, permission_document_tools,
                permission_document_trash, permission_document_view,
                permission_document_version_create, permission_events_view,
            )
        )
        ModelPermission.register(
            model=DocumentFile, permissions=(
                permission_acl_edit, permission_acl_view,
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
            model=DocumentFilePage, related='document_file__document',
        )
        ModelPermission.register_inheritance(
            model=DocumentFilePageResult, related='document_file__document',
        )
        ModelPermission.register_inheritance(
            model=DocumentVersion, related='document',
        )
        ModelPermission.register_inheritance(
            model=DocumentVersionPage, related='document_version__document',
        )
        ModelPermission.register_inheritance(
            model=DocumentTypeFilename, related='document_type',
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

        # Document file and document file page thumbnail widget

        document_file_page_thumbnail_widget = DocumentFilePageThumbnailWidget()

        # Document version and document version page thumbnail widget

        document_version_page_thumbnail_widget = DocumentVersionPageThumbnailWidget()

        # Document

        SourceColumn(
            attribute='label', is_object_absolute_url=True, is_identifier=True,
            is_sortable=True, source=Document
        )
        SourceColumn(
            func=lambda context: document_file_page_thumbnail_widget.render(
                instance=context['object']
            ), html_extra_classes='text-center document-thumbnail-list',
            label=_('Thumbnail'), source=Document
        )
        ##TEMP
        SourceColumn(
            func=lambda context: 'Files: {}'.format(context['object'].files.count()),
            label=_('Files'), source=Document
        )
        SourceColumn(
            func=lambda context: 'Versions: {}'.format(context['object'].versions.count()),
            label=_('Versions'), source=Document
        )
        SourceColumn(
            func=lambda context: context['object'].is_stub,
            label=_('Is stub'), source=Document
        )
        ##TEMP
        SourceColumn(
            attribute='document_type', is_sortable=True, source=Document,
        )
        SourceColumn(
            func=lambda context: widget_document_page_number(
                document=context['object']
            ), label=_('Pages'), source=Document
        )
        SourceColumn(
            attribute='date_added', include_label=True, is_sortable=True,
            source=Document, views=('documents:document_list_recent_added',)
        )
        SourceColumn(
            func=lambda context: DuplicatedDocument.objects.get(
                document=context['object']
            ).documents.count(), include_label=True, label=_('Duplicates'),
            source=Document, views=('documents:duplicated_document_list',)
        )

        # DocumentFile

        SourceColumn(
            source=DocumentFile, attribute='filename', is_identifier=True,
            is_object_absolute_url=True
        )
        SourceColumn(
            func=lambda context: document_file_page_thumbnail_widget.render(
                instance=context['object']
            ), html_extra_classes='text-center document-thumbnail-list',
            label=_('Thumbnail'), source=DocumentFile
        )
        SourceColumn(
            func=lambda context: widget_document_file_page_number(
                document_file=context['object']
            ), label=_('Pages'), source=DocumentFile
        )
        SourceColumn(
            attribute='mimetype', is_sortable=True, source=DocumentFile
        )
        SourceColumn(
            attribute='encoding', is_sortable=True, source=DocumentFile
        )
        SourceColumn(
            attribute='comment', is_sortable=True, source=DocumentFile
        )

        # DocumentFilePage

        SourceColumn(
            attribute='get_page_number_display', is_identifier=True,
            is_object_absolute_url=True, source=DocumentFilePage,
        )
        SourceColumn(
            func=lambda context: document_file_page_thumbnail_widget.render(
                instance=context['object']
            ), html_extra_classes='text-center document-thumbnail-list',
            label=_('Thumbnail'), source=DocumentFilePage
        )

        SourceColumn(
            attribute='get_label', is_identifier=True,
            is_object_absolute_url=True, source=DocumentFilePageResult
        )
        SourceColumn(
            func=lambda context: document_file_page_thumbnail_widget.render(
                instance=context['object']
            ), html_extra_classes='text-center document-thumbnail-list',
            label=_('Thumbnail'), source=DocumentFilePageResult
        )
        SourceColumn(
            attribute='document_file.document.document_type',
            label=_('Type'), source=DocumentFilePageResult
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
            source=DocumentVersion, attribute='timestamp', is_identifier=True,
            is_object_absolute_url=True
        )
        SourceColumn(
            func=lambda context: document_version_page_thumbnail_widget.render(
                instance=context['object']
            ), html_extra_classes='text-center document-thumbnail-list',
            label=_('Thumbnail'), source=DocumentVersion
        )
        SourceColumn(
            func=lambda context: widget_document_version_page_number(
                document_version=context['object']
            ), label=_('Pages'), source=DocumentVersion
        )
        SourceColumn(
            attribute='active', include_label=True, is_sortable=True,
            source=DocumentVersion
        )
        SourceColumn(
            attribute='comment', include_label=True, is_sortable=True,
            source=DocumentVersion
        )

        # DocumentVersionPage

        SourceColumn(
            attribute='get_page_number_display', is_identifier=True,
            is_object_absolute_url=True, source=DocumentVersionPage,
        )
        SourceColumn(
            func=lambda context: document_version_page_thumbnail_widget.render(
                instance=context['object']
            ), html_extra_classes='text-center document-thumbnail-list',
            label=_('Thumbnail'), source=DocumentVersionPage
        )

        #SourceColumn(
        #    attribute='get_label', is_identifier=True,
        #    is_object_absolute_url=True, source=DocumentVersionPageResult
        #)
        #SourceColumn(
        #    func=lambda context: document_version_page_thumbnail_widget.render(
        #        instance=context['object']
        #    ), html_extra_classes='text-center document-thumbnail-list',
        #    label=_('Thumbnail'), source=DocumentVersionPageResult
        #)
        #SourceColumn(
        #    attribute='document_version.document.document_type',
        #    label=_('Type'), source=DocumentVersionPageResult
        #)

        # DeletedDocument

        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=DeletedDocument
        )
        SourceColumn(
            attribute='deleted_date_time', include_label=True, order=99,
            source=DeletedDocument
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
                link_document_list_recent_access,
                link_document_list_recent_added, link_document_list_favorites,
                link_document_list, link_document_list_deleted,
                link_duplicated_document_list,
            )
        )

        menu_main.bind_links(links=(menu_documents,), position=0)

        menu_setup.bind_links(links=(link_document_type_setup,))
        menu_tools.bind_links(
            links=(link_duplicated_document_scan,)
        )

        # Document

        menu_facet.bind_links(
            links=(link_document_duplicates_list, link_acl_list,),
            sources=(Document,)
        )
        menu_facet.bind_links(
            links=(link_document_preview,), sources=(Document,), position=0
        )
        menu_facet.bind_links(
            links=(link_document_properties,), sources=(Document,), position=2
        )
        menu_facet.bind_links(
            links=(
                link_events_for_object,
                link_object_event_types_user_subcriptions_list,
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
                link_document_file_preview,
                link_acl_list, link_object_event_types_user_subcriptions_list,
                link_events_for_object
            ), sources=(DocumentFile,)
        )
        menu_multi_item.bind_links(
            links=(
                #link_document_file_multiple_download,
                link_document_file_multiple_page_count_update,
                link_document_file_multiple_transformations_clear,
            ), sources=(DocumentFile,)
        )
        menu_object.bind_links(
            links=(
                link_document_file_cache_purge,
                link_document_file_delete,
                #link_document_file_download,
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
                link_document_type_filename_generator,
                link_acl_list, link_object_event_types_user_subcriptions_list,
                link_events_for_object,
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
                link_document_version_page_list, link_document_version_preview,
                link_acl_list, link_object_event_types_user_subcriptions_list,
                link_events_for_object
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
                link_document_version_cache_purge,
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
            ), sources=(DocumentVersionPage,)
        )
        menu_object.bind_links(
            links=(
                link_document_version_page_delete,
            ), sources=(DocumentVersionPage,)
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
            sources=(DeletedDocument,)
        )
        menu_multi_item.add_proxy_exclusion(source=DeletedDocument)
        menu_multi_item.bind_links(
            links=(
                link_document_multiple_restore, link_document_multiple_delete
            ), sources=(DeletedDocument,)
        )

        post_delete.connect(
            dispatch_uid='documents_handler_remove_empty_duplicates_lists',
            receiver=handler_remove_empty_duplicates_lists,
            sender=Document
        )
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
        signal_post_document_file_upload.connect(
            dispatch_uid='documents_handler_scan_duplicates_for',
            receiver=handler_scan_duplicates_for
        )
