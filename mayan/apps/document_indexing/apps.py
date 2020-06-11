from django.apps import apps
from django.db.models.signals import post_delete, post_save, pre_delete
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.acls.permissions import permission_acl_edit, permission_acl_view
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import (
    menu_facet, menu_list_facet, menu_main, menu_object, menu_secondary,
    menu_setup, menu_tools
)
from mayan.apps.documents.signals import signal_post_document_created, signal_post_initial_document_type
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.events.links import (
    link_events_for_object, link_object_event_types_user_subcriptions_list
)
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.views.html_widgets import TwoStateWidget

from .events import event_index_template_created, event_index_template_edited
from .handlers import (
    handler_create_default_document_index, handler_delete_empty,
    handler_index_document, handler_remove_document,
    handler_post_save_index_document
)
from .html_widgets import (
    get_instance_link, index_instance_item_link, node_level
)
from .links import (
    link_document_index_instance_list, link_document_type_index_templates,
    link_index_instance_menu, link_index_instance_rebuild,
    link_index_instances_reset, link_index_template_setup,
    link_index_template_create, link_index_template_document_types,
    link_index_template_delete, link_index_template_edit,
    link_index_template_list, link_index_template_node_tree_view,
    link_index_instances_rebuild, link_index_template_node_create,
    link_index_template_node_delete, link_index_template_node_edit
)
from .permissions import (
    permission_document_indexing_delete, permission_document_indexing_edit,
    permission_document_indexing_instance_view,
    permission_document_indexing_rebuild, permission_document_indexing_view
)
from .search import *  # NOQA


class DocumentIndexingApp(MayanAppConfig):
    app_namespace = 'indexing'
    app_url = 'indexing'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.document_indexing'
    verbose_name = _('Document indexing')

    def ready(self):
        super(DocumentIndexingApp, self).ready()

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        DocumentType = apps.get_model(
            app_label='documents', model_name='DocumentType'
        )

        DocumentIndexInstanceNode = self.get_model(
            model_name='DocumentIndexInstanceNode'
        )

        Index = self.get_model(model_name='Index')
        IndexInstance = self.get_model(model_name='IndexInstance')
        IndexInstanceNode = self.get_model(model_name='IndexInstanceNode')
        IndexInstanceNodeSearchResult = self.get_model(
            model_name='IndexInstanceNodeSearchResult'
        )
        IndexTemplateNode = self.get_model(model_name='IndexTemplateNode')

        EventModelRegistry.register(model=Index)

        ModelEventType.register(
            event_types=(
                event_index_template_created, event_index_template_edited
            ), model=Index
        )

        ModelPermission.register(
            model=Index, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_document_indexing_delete,
                permission_document_indexing_edit,
                permission_document_indexing_instance_view,
                permission_document_indexing_rebuild,
                permission_document_indexing_view,
            )
        )
        ModelPermission.register_inheritance(
            model=IndexTemplateNode, related='index'
        )

        ModelPermission.register_inheritance(
            model=IndexInstanceNode, related='index_template_node__index'
        )

        column_index_label = SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=Index
        )
        column_index_label.add_exclude(source=IndexInstance)
        SourceColumn(
            attribute='label', is_object_absolute_url=True,
            is_identifier=True, is_sortable=True, source=IndexInstance
        )
        column_index_slug = SourceColumn(
            attribute='slug', include_label=True, is_sortable=True,
            source=Index
        )
        column_index_slug.add_exclude(IndexInstance)
        column_index_enabled = SourceColumn(
            attribute='enabled', include_label=True, is_sortable=True,
            source=Index, widget=TwoStateWidget
        )
        column_index_enabled.add_exclude(source=IndexInstance)

        SourceColumn(
            func=lambda context: context[
                'object'
            ].instance_root.get_descendants_count(), include_label=True,
            label=_('Total levels'), source=IndexInstance
        )
        SourceColumn(
            func=lambda context: context[
                'object'
            ].instance_root.get_descendants_document_count(
                user=context['request'].user
            ), include_label=True, label=_('Total documents'),
            source=IndexInstance
        )

        SourceColumn(
            func=lambda context: node_level(context['object']),
            include_label=True, is_identifier=True, label=_('Level'),
            source=IndexTemplateNode
        )
        SourceColumn(
            attribute='enabled', include_label=True, is_sortable=True,
            source=IndexTemplateNode, widget=TwoStateWidget
        )
        SourceColumn(
            attribute='link_documents', include_label=True, is_sortable=True,
            source=IndexTemplateNode, widget=TwoStateWidget
        )

        SourceColumn(
            func=lambda context: index_instance_item_link(context['object']),
            is_identifier=True, is_sortable=True, label=_('Level'),
            sort_field='value', source=IndexInstanceNode
        )
        SourceColumn(
            func=lambda context: context['object'].get_descendants_count(),
            include_label=True, label=_('Levels'), source=IndexInstanceNode
        )
        SourceColumn(
            func=lambda context: context[
                'object'
            ].get_descendants_document_count(
                user=context['request'].user
            ), include_label=True, label=_('Documents'),
            source=IndexInstanceNode
        )
        SourceColumn(
            func=lambda context: context[
                'object'
            ].get_descendants_document_count(
                user=context['request'].user
            ), include_label=True, label=_('Documents'),
            source=IndexInstanceNode
        )
        SourceColumn(
            func=lambda context: index_instance_item_link(context['object']),
            is_identifier=True, is_sortable=True, label=_('Level'),
            sort_field='value', source=IndexInstanceNodeSearchResult
        )
        SourceColumn(
            attribute='get_full_path', source=IndexInstanceNodeSearchResult
        )

        SourceColumn(
            func=lambda context: get_instance_link(
                index_instance_node=context['object'],
            ), include_label=True, is_sortable=True, label=_('Level'),
            sort_field='value', source=DocumentIndexInstanceNode
        )
        SourceColumn(
            func=lambda context: context['object'].get_descendants_count(),
            include_label=True, label=_('Levels'),
            source=DocumentIndexInstanceNode
        )
        SourceColumn(
            func=lambda context: context[
                'object'
            ].get_descendants_document_count(
                user=context['request'].user
            ), include_label=True, label=_('Documents'),
            source=DocumentIndexInstanceNode
        )

        menu_facet.bind_links(
            links=(
                link_document_index_instance_list,
            ), sources=(Document,)
        )
        menu_list_facet.bind_links(
            links=(link_document_type_index_templates,),
            sources=(DocumentType,)
        )
        menu_list_facet.bind_links(
            links=(
                link_acl_list, link_events_for_object,
                link_index_template_document_types,
                link_index_template_node_tree_view,
                link_object_event_types_user_subcriptions_list
            ), sources=(Index,)
        )
        menu_object.bind_links(
            links=(
                link_index_template_delete, link_index_template_edit,
                link_index_instance_rebuild
            ), sources=(Index,)
        )
        menu_object.bind_links(
            links=(
                link_index_template_node_create, link_index_template_node_edit,
                link_index_template_node_delete
            ), sources=(IndexTemplateNode,)
        )
        menu_main.bind_links(links=(link_index_instance_menu,), position=98)
        menu_secondary.bind_links(
            links=(link_index_template_list, link_index_template_create),
            sources=(
                Index, 'indexing:index_setup_list',
                'indexing:index_setup_create'
            )
        )
        menu_setup.bind_links(links=(link_index_template_setup,))
        menu_tools.bind_links(
            links=(link_index_instances_rebuild, link_index_instances_reset)
        )

        post_save.connect(
            dispatch_uid='document_indexing_handler_post_save_index_document',
            receiver=handler_post_save_index_document,
            sender=Document
        )
        post_delete.connect(
            dispatch_uid='document_indexing_handler_delete_empty',
            receiver=handler_delete_empty,
            sender=Document
        )
        pre_delete.connect(
            dispatch_uid='document_indexing_handler_remove_document',
            receiver=handler_remove_document,
            sender=Document
        )
        signal_post_document_created.connect(
            dispatch_uid='document_indexing_handler_index_document',
            receiver=handler_index_document,
            sender=Document
        )
        signal_post_initial_document_type.connect(
            dispatch_uid='document_indexing_handler_create_default_document_index',
            receiver=handler_create_default_document_index,
            sender=DocumentType
        )
