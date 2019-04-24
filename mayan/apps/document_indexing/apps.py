from __future__ import absolute_import, unicode_literals

from kombu import Exchange, Queue

from django.apps import apps
from django.db.models.signals import post_delete, post_save, pre_delete
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.acls.permissions import permission_acl_edit, permission_acl_view
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.html_widgets import TwoStateWidget
from mayan.apps.common.menus import (
    menu_facet, menu_list_facet, menu_main, menu_object, menu_secondary,
    menu_setup, menu_tools
)
from mayan.apps.documents.signals import post_document_created, post_initial_document_type
from mayan.apps.navigation import SourceColumn
from mayan.celery import app

from .handlers import (
    create_default_document_index, handler_delete_empty,
    handler_index_document, handler_remove_document,
    handler_post_save_index_document
)
from .html_widgets import (
    get_instance_link, index_instance_item_link, node_level
)
from .links import (
    link_document_index_instance_list, link_index_instance_menu, link_index_template_setup,
    link_index_template_create, link_index_template_document_types,
    link_index_template_delete, link_index_template_edit, link_index_template_list,
    link_index_template_node_tree_view, link_index_instances_rebuild,
    link_index_template_node_create, link_index_template_node_delete,
    link_index_template_node_edit
)
from .licenses import *  # NOQA
from .permissions import (
    permission_document_indexing_create, permission_document_indexing_delete,
    permission_document_indexing_edit,
    permission_document_indexing_instance_view,
    permission_document_indexing_rebuild, permission_document_indexing_view
)
from .queues import *  # NOQA


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

        DocumentIndexInstanceNode = self.get_model('DocumentIndexInstanceNode')

        Index = self.get_model('Index')
        IndexInstance = self.get_model('IndexInstance')
        IndexInstanceNode = self.get_model('IndexInstanceNode')
        IndexTemplateNode = self.get_model('IndexTemplateNode')

        ModelPermission.register(
            model=Index, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_document_indexing_create,
                permission_document_indexing_delete,
                permission_document_indexing_edit,
                permission_document_indexing_instance_view,
                permission_document_indexing_rebuild,
                permission_document_indexing_view,
            )
        )

        SourceColumn(source=Index, label=_('Label'), attribute='label')
        SourceColumn(source=Index, label=_('Slug'), attribute='slug')
        SourceColumn(
            attribute='enabled', label=_('Enabled'), source=Index,
            widget=TwoStateWidget
        )

        SourceColumn(
            source=IndexInstance, label=_('Total levels'),
            func=lambda context: context[
                'object'
            ].instance_root.get_descendants_count()
        )
        SourceColumn(
            source=IndexInstance, label=_('Total documents'),
            func=lambda context: context[
                'object'
            ].instance_root.get_descendants_document_count(
                user=context['request'].user
            )
        )

        SourceColumn(
            source=IndexTemplateNode, label=_('Level'),
            func=lambda context: node_level(context['object'])
        )
        SourceColumn(
            attribute='enabled', label=_('Enabled'), source=IndexTemplateNode,
            widget=TwoStateWidget
        )
        SourceColumn(
            attribute='enabled', label=_('Has document links?'),
            source=IndexTemplateNode, widget=TwoStateWidget
        )
        SourceColumn(
            source=IndexInstanceNode, label=_('Level'),
            func=lambda context: index_instance_item_link(context['object'])
        )
        SourceColumn(
            source=IndexInstanceNode, label=_('Levels'),
            func=lambda context: context['object'].get_descendants_count()
        )
        SourceColumn(
            source=IndexInstanceNode, label=_('Documents'),
            func=lambda context: context[
                'object'
            ].get_descendants_document_count(
                user=context['request'].user
            )
        )

        SourceColumn(
            source=DocumentIndexInstanceNode, label=_('Level'),
            func=lambda context: get_instance_link(
                index_instance_node=context['object'],
            )
        )
        SourceColumn(
            source=DocumentIndexInstanceNode, label=_('Levels'),
            func=lambda context: context['object'].get_descendants_count()
        )
        SourceColumn(
            source=DocumentIndexInstanceNode, label=_('Documents'),
            func=lambda context: context[
                'object'
            ].get_descendants_document_count(
                user=context['request'].user
            )
        )

        app.conf.CELERY_QUEUES.append(
            Queue('indexing', Exchange('indexing'), routing_key='indexing'),
        )

        app.conf.CELERY_ROUTES.update(
            {
                'mayan.apps.document_indexing.tasks.task_delete_empty': {
                    'queue': 'indexing'
                },
                'mayan.apps.document_indexing.tasks.task_remove_document': {
                    'queue': 'indexing'
                },
                'mayan.apps.document_indexing.tasks.task_index_document': {
                    'queue': 'indexing'
                },
                'mayan.apps.document_indexing.tasks.task_rebuild_index': {
                    'queue': 'tools'
                },
            }
        )

        menu_facet.bind_links(
            links=(link_document_index_instance_list,), sources=(Document,)
        )
        menu_list_facet.bind_links(
            links=(
                link_acl_list, link_index_template_document_types,
                link_index_template_node_tree_view,
            ), sources=(Index,)
        )
        menu_object.bind_links(
            links=(
                link_index_template_delete, link_index_template_edit,
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
        menu_tools.bind_links(links=(link_index_instances_rebuild,))

        post_delete.connect(
            dispatch_uid='document_indexing_handler_delete_empty',
            receiver=handler_delete_empty,
            sender=Document
        )
        post_document_created.connect(
            dispatch_uid='document_indexing_handler_index_document',
            receiver=handler_index_document,
            sender=Document
        )
        post_initial_document_type.connect(
            dispatch_uid='document_indexing_create_default_document_index',
            receiver=create_default_document_index,
            sender=DocumentType
        )
        post_save.connect(
            dispatch_uid='document_indexing_handler_post_save_index_document',
            receiver=handler_post_save_index_document,
            sender=Document
        )
        pre_delete.connect(
            dispatch_uid='document_indexing_handler_remove_document',
            receiver=handler_remove_document,
            sender=Document
        )
