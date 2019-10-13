from __future__ import absolute_import, unicode_literals

from django.db.models.signals import post_delete, post_migrate
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.acls.permissions import permission_acl_edit, permission_acl_view
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.classes import MissingItem, ModelField, Template
from mayan.apps.common.html_widgets import TwoStateWidget
from mayan.apps.common.menus import (
    menu_facet, menu_list_facet, menu_main, menu_object, menu_secondary,
    menu_setup, menu_multi_item, menu_tools
)
from mayan.apps.common.signals import post_initial_setup
from mayan.apps.dashboards.dashboards import dashboard_main
from mayan.apps.converter.links import link_transformation_list
from mayan.apps.converter.permissions import (
    permission_transformation_create,
    permission_transformation_delete, permission_transformation_edit,
    permission_transformation_view,
)
from mayan.apps.events.classes import ModelEventType
from mayan.apps.events.links import (
    link_events_for_object, link_object_event_types_user_subcriptions_list,
)
from mayan.apps.events.permissions import permission_events_view
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.rest_api.fields import DynamicSerializerField

from .dashboard_widgets import (
    DashboardWidgetDocumentPagesTotal, DashboardWidgetDocumentsInTrash,
    DashboardWidgetDocumentsNewThisMonth,
    DashboardWidgetDocumentsPagesNewThisMonth, DashboardWidgetDocumentsTotal,
    DashboardWidgetDocumentsTypesTotal,
)
from .events import (
    event_document_create, event_document_download,
    event_document_properties_edit, event_document_type_change,
    event_document_type_created, event_document_type_edited,
    event_document_new_version, event_document_version_revert,
    event_document_view
)
from .handlers import (
    handler_create_default_document_type, handler_create_document_cache,
    handler_remove_empty_duplicates_lists, handler_scan_duplicates_for
)
from .links import (
    link_document_clear_transformations,
    link_document_clone_transformations, link_document_delete,
    link_document_document_type_edit, link_document_download,
    link_document_duplicates_list, link_document_edit,
    link_document_favorites_add, link_document_favorites_remove,
    link_document_list, link_document_list_deleted,
    link_document_list_favorites, link_document_list_recent_access,
    link_document_list_recent_added,
    link_document_multiple_clear_transformations,
    link_document_multiple_delete, link_document_multiple_document_type_edit,
    link_document_multiple_download, link_document_multiple_favorites_add,
    link_document_multiple_favorites_remove, link_document_multiple_restore,
    link_document_multiple_trash, link_document_multiple_update_page_count,
    link_document_page_disable, link_document_page_multiple_disable,
    link_document_page_enable, link_document_page_multiple_enable,
    link_document_page_navigation_first, link_document_page_navigation_last,
    link_document_page_navigation_next, link_document_page_navigation_previous,
    link_document_page_return, link_document_page_rotate_left,
    link_document_page_rotate_right, link_document_page_view,
    link_document_page_view_reset, link_document_page_zoom_in,
    link_document_page_zoom_out, link_document_pages, link_document_preview,
    link_document_print, link_document_properties, link_document_quick_download,
    link_document_restore, link_document_trash, link_document_type_create,
    link_document_type_delete, link_document_type_edit,
    link_document_type_filename_create, link_document_type_filename_delete,
    link_document_type_filename_edit, link_document_type_filename_list,
    link_document_type_list, link_document_type_policies,
    link_document_type_setup, link_document_update_page_count,
    link_document_version_download, link_document_version_list,
    link_document_version_return_document, link_document_version_return_list,
    link_document_version_revert, link_document_version_view,
    link_duplicated_document_list, link_duplicated_document_scan,
    link_trash_can_empty
)
from .menus import menu_documents
from .permissions import (
    permission_document_create, permission_document_delete,
    permission_document_download, permission_document_edit,
    permission_document_new_version, permission_document_print,
    permission_document_properties_edit, permission_document_restore,
    permission_document_tools, permission_document_trash,
    permission_document_type_delete, permission_document_type_edit,
    permission_document_type_view, permission_document_version_revert,
    permission_document_version_view, permission_document_view
)
# Just import to initialize the search models
from .search import document_search, document_page_search  # NOQA
from .signals import post_version_upload
from .statistics import *  # NOQA
from .widgets import (
    DocumentPageThumbnailWidget, widget_document_page_number,
    widget_document_version_page_number
)


def is_document_page_enabled(context):
    return context['object'].enabled


class DocumentsApp(MayanAppConfig):
    app_namespace = 'documents'
    app_url = 'documents'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.documents'
    verbose_name = _('Documents')

    def ready(self):
        super(DocumentsApp, self).ready()
        from actstream import registry

        DeletedDocument = self.get_model(model_name='DeletedDocument')
        Document = self.get_model(model_name='Document')
        DocumentPage = self.get_model(model_name='DocumentPage')
        DocumentPageResult = self.get_model(model_name='DocumentPageResult')
        DocumentType = self.get_model(model_name='DocumentType')
        DocumentTypeFilename = self.get_model(model_name='DocumentTypeFilename')
        DocumentVersion = self.get_model(model_name='DocumentVersion')
        DuplicatedDocument = self.get_model(model_name='DuplicatedDocument')

        DynamicSerializerField.add_serializer(
            klass=Document,
            serializer_class='mayan.apps.documents.serializers.DocumentSerializer'
        )

        MissingItem(
            label=_('Create a document type'),
            description=_(
                'Every uploaded document must be assigned a document type, '
                'it is the basic way Mayan EDMS categorizes documents.'
            ), condition=lambda: not DocumentType.objects.exists(),
            view='documents:document_type_list'
        )

        ModelField(model=Document, name='description')
        ModelField(model=Document, name='date_added')
        ModelField(model=Document, name='deleted_date_time')
        ModelField(model=Document, name='document_type__label')
        ModelField(model=Document, name='in_trash')
        ModelField(model=Document, name='is_stub')
        ModelField(model=Document, name='label')
        ModelField(model=Document, name='language')
        ModelField(model=Document, name='uuid')
        ModelField(
            model=Document, name='versions__checksum'
        )
        ModelField(
            model=Document, label=_('Versions comment'),
            name='versions__comment'
        )
        ModelField(
            model=Document, label=_('Versions encoding'),
            name='versions__encoding'
        )
        ModelField(
            model=Document, label=_('Versions mime type'),
            name='versions__mimetype'
        )
        ModelField(
            model=Document, label=_('Versions timestamp'),
            name='versions__timestamp'
        )

        ModelEventType.register(
            model=DocumentType, event_types=(
                event_document_create,
                event_document_type_created,
                event_document_type_edited,
            )
        )
        ModelEventType.register(
            model=Document, event_types=(
                event_document_download, event_document_properties_edit,
                event_document_type_change, event_document_new_version,
                event_document_version_revert, event_document_view
            )
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_document_delete, permission_document_download,
                permission_document_edit, permission_document_new_version,
                permission_document_print, permission_document_properties_edit,
                permission_document_restore, permission_document_tools,
                permission_document_trash, permission_document_version_revert,
                permission_document_version_view, permission_document_view,
                permission_events_view, permission_transformation_create,
                permission_transformation_delete,
                permission_transformation_edit, permission_transformation_view,
            )
        )

        ModelPermission.register(
            model=DocumentType, permissions=(
                permission_document_create, permission_document_type_delete,
                permission_document_type_edit, permission_document_type_view,
                permission_acl_edit, permission_acl_view,
                permission_document_delete, permission_document_download,
                permission_document_edit, permission_document_new_version,
                permission_document_print, permission_document_properties_edit,
                permission_document_restore, permission_document_trash,
                permission_document_version_revert,
                permission_document_version_view, permission_document_view,
                permission_events_view, permission_transformation_create,
                permission_transformation_delete,
                permission_transformation_edit, permission_transformation_view,
            )
        )

        ModelPermission.register_inheritance(
            model=Document, related='document_type',
        )
        ModelPermission.register_manager(
            model=Document, manager_name='passthrough'
        )
        ModelPermission.register_inheritance(
            model=DocumentPage, related='document_version__document',
        )
        ModelPermission.register_manager(
            model=DocumentPage, manager_name='passthrough'
        )
        ModelPermission.register_inheritance(
            model=DocumentPageResult, related='document_version__document',
        )
        ModelPermission.register_manager(
            model=DocumentPageResult, manager_name='passthrough'
        )
        ModelPermission.register_inheritance(
            model=DocumentTypeFilename, related='document_type',
        )
        ModelPermission.register_inheritance(
            model=DocumentVersion, related='document',
        )

        # Document and document page thumbnail widget
        document_page_thumbnail_widget = DocumentPageThumbnailWidget()

        # Document
        SourceColumn(
            attribute='label', is_object_absolute_url=True, is_identifier=True,
            is_sortable=True, source=Document
        )
        SourceColumn(
            func=lambda context: document_page_thumbnail_widget.render(
                instance=context['object']
            ), label=_('Thumbnail'), source=Document
        )
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

        # DocumentPage
        SourceColumn(
            attribute='get_label', is_identifier=True,
            is_object_absolute_url=True, source=DocumentPage,
            widget_condition=is_document_page_enabled
        )
        SourceColumn(
            func=lambda context: document_page_thumbnail_widget.render(
                instance=context['object']
            ), label=_('Thumbnail'), source=DocumentPage
        )
        SourceColumn(
            attribute='enabled', include_label=True, source=DocumentPage,
            widget=TwoStateWidget
        )
        SourceColumn(
            attribute='page_number', include_label=True, source=DocumentPage
        )

        SourceColumn(
            attribute='get_label', is_identifier=True,
            is_object_absolute_url=True, source=DocumentPageResult
        )
        SourceColumn(
            func=lambda context: document_page_thumbnail_widget.render(
                instance=context['object']
            ), label=_('Thumbnail'), source=DocumentPageResult
        )
        SourceColumn(
            attribute='document_version.document.document_type',
            label=_('Type'), source=DocumentPageResult
        )

        # DocumentType
        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=DocumentType
        )

        SourceColumn(
            func=lambda context: context['object'].get_document_count(
                user=context['request'].user
            ), label=_('Documents'), source=DocumentType
        )

        SourceColumn(
            attribute='filename', is_identifier=True, is_sortable=True,
            source=DocumentTypeFilename
        )
        SourceColumn(
            attribute='enabled', is_sortable=True, source=DocumentTypeFilename,
            widget=TwoStateWidget
        )

        # DeletedDocument
        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=DeletedDocument
        )
        SourceColumn(
            attribute='deleted_date_time', include_label=True, order=99,
            source=DeletedDocument
        )

        # DocumentVersion
        SourceColumn(
            source=DocumentVersion, attribute='timestamp', is_identifier=True,
            is_object_absolute_url=True
        )
        SourceColumn(
            func=lambda context: document_page_thumbnail_widget.render(
                instance=context['object']
            ), label=_('Thumbnail'), source=DocumentVersion
        )
        SourceColumn(
            func=lambda context: widget_document_version_page_number(
                document_version=context['object']
            ), label=_('Pages'), source=DocumentVersion
        )
        SourceColumn(
            attribute='mimetype', is_sortable=True, source=DocumentVersion
        )
        SourceColumn(
            attribute='encoding', is_sortable=True, source=DocumentVersion
        )
        SourceColumn(
            attribute='comment', is_sortable=True, source=DocumentVersion
        )

        Template(
            name='invalid_document',
            template_name='documents/invalid_document.html'
        )

        dashboard_main.add_widget(
            widget=DashboardWidgetDocumentsTotal, order=0
        )
        dashboard_main.add_widget(
            widget=DashboardWidgetDocumentPagesTotal, order=1
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

        # Document type links
        menu_list_facet.bind_links(
            links=(
                link_document_type_filename_list,
                link_document_type_policies,
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

        # Document object links
        menu_object.bind_links(
            links=(
                link_document_favorites_add, link_document_favorites_remove,
                link_document_edit, link_document_document_type_edit,
                link_document_print, link_document_trash,
                link_document_quick_download, link_document_download,
                link_document_clear_transformations,
                link_document_clone_transformations,
                link_document_update_page_count,
            ), sources=(Document,)
        )
        menu_object.bind_links(
            links=(link_document_restore, link_document_delete),
            sources=(DeletedDocument,)
        )

        # Document facet links
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
                link_document_version_list,
            ), sources=(Document,), position=2
        )
        menu_facet.bind_links(links=(link_document_pages,), sources=(Document,))

        # Document actions
        menu_object.bind_links(
            links=(
                link_document_version_revert, link_document_version_download
            ),
            sources=(DocumentVersion,)
        )
        menu_multi_item.bind_links(
            links=(
                link_document_multiple_favorites_add,
                link_document_multiple_favorites_remove,
                link_document_multiple_clear_transformations,
                link_document_multiple_trash, link_document_multiple_download,
                link_document_multiple_update_page_count,
                link_document_multiple_document_type_edit,
            ), sources=(Document,)
        )
        menu_multi_item.bind_links(
            links=(
                link_document_multiple_restore, link_document_multiple_delete
            ), sources=(DeletedDocument,)
        )

        # Document pages
        menu_facet.add_unsorted_source(source=DocumentPage)
        menu_facet.bind_links(
            links=(
                link_document_page_rotate_left,
                link_document_page_rotate_right, link_document_page_zoom_in,
                link_document_page_zoom_out, link_document_page_view_reset
            ), sources=('documents:document_page_view',)
        )
        menu_facet.bind_links(
            links=(link_document_page_return, link_document_page_view),
            sources=(DocumentPage,)
        )
        menu_facet.bind_links(
            links=(
                link_document_page_navigation_first,
                link_document_page_navigation_previous,
                link_document_page_navigation_next,
                link_document_page_navigation_last
            ), sources=(DocumentPage,)
        )
        menu_multi_item.bind_links(
            links=(
                link_document_page_multiple_disable,
                link_document_page_multiple_enable
            ), sources=(DocumentPage,)
        )
        menu_object.bind_links(
            links=(link_document_page_disable, link_document_page_enable),
            sources=(DocumentPage,)
        )
        menu_list_facet.bind_links(
            links=(link_transformation_list,), sources=(DocumentPage,)
        )

        # Document versions
        menu_facet.bind_links(
            links=(
                link_document_version_return_document,
                link_document_version_return_list
            ), sources=(DocumentVersion,)
        )
        menu_list_facet.bind_links(
            links=(link_document_version_view,), sources=(DocumentVersion,)
        )

        post_delete.connect(
            dispatch_uid='handler_remove_empty_duplicates_lists',
            receiver=handler_remove_empty_duplicates_lists,
            sender=Document
        )
        post_initial_setup.connect(
            dispatch_uid='handler_create_default_document_type',
            receiver=handler_create_default_document_type
        )
        post_migrate.connect(
            dispatch_uid='documents_handler_create_document_cache',
            receiver=handler_create_document_cache,
        )
        post_version_upload.connect(
            dispatch_uid='handler_scan_duplicates_for',
            receiver=handler_scan_duplicates_for
        )

        registry.register(DeletedDocument)
        registry.register(Document)
        registry.register(DocumentType)
        registry.register(DocumentVersion)
