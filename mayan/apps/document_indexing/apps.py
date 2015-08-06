from __future__ import absolute_import, unicode_literals

from kombu import Exchange, Queue

from django.db.models.signals import post_save, post_delete
from django.utils.translation import ugettext_lazy as _

from common import (
    MayanAppConfig, menu_facet, menu_main, menu_object, menu_secondary,
    menu_setup, menu_tools
)
from documents.models import Document
from documents.signals import post_document_created
from mayan.celery import app
from metadata.models import DocumentMetadata
from rest_api.classes import APIEndPoint

from .handlers import (
    document_created_index_update, document_index_delete,
    document_metadata_index_update, document_metadata_index_post_delete
)
from .links import (
    link_document_index_list, link_index_main_menu, link_index_setup,
    link_index_setup_create, link_index_setup_document_types,
    link_index_setup_delete, link_index_setup_edit, link_index_setup_list,
    link_index_setup_view, link_rebuild_index_instances,
    link_template_node_create, link_template_node_delete,
    link_template_node_edit
)
from .models import Index, IndexTemplateNode


class DocumentIndexingApp(MayanAppConfig):
    app_namespace = 'indexing'
    app_url = 'indexing'
    name = 'document_indexing'
    verbose_name = _('Document indexing')

    def ready(self):
        super(DocumentIndexingApp, self).ready()

        APIEndPoint(app=self, version_string='1')

        app.conf.CELERY_QUEUES.append(
            Queue('indexing', Exchange('indexing'), routing_key='indexing'),
        )

        app.conf.CELERY_ROUTES.update(
            {
                'document_indexing.tasks.task_delete_empty_index_nodes': {
                    'queue': 'indexing'
                },
                'document_indexing.tasks.task_index_document': {
                    'queue': 'indexing'
                },
                'document_indexing.tasks.task_do_rebuild_all_indexes': {
                    'queue': 'tools'
                },
            }
        )

        menu_facet.bind_links(
            links=(link_document_index_list,), sources=(Document,)
        )
        menu_object.bind_links(
            links=(
                link_index_setup_edit, link_index_setup_view,
                link_index_setup_document_types, link_index_setup_delete
            ), sources=(Index,)
        )
        menu_object.bind_links(
            links=(
                link_template_node_create, link_template_node_edit,
                link_template_node_delete
            ), sources=(IndexTemplateNode,)
        )
        menu_main.bind_links(links=(link_index_main_menu,))
        menu_secondary.bind_links(
            links=(link_index_setup_list, link_index_setup_create),
            sources=(
                Index, 'indexing:index_setup_list',
                'indexing:index_setup_create'
            )
        )
        menu_setup.bind_links(links=(link_index_setup,))
        menu_tools.bind_links(links=(link_rebuild_index_instances,))

        post_delete.connect(
            document_index_delete, dispatch_uid='document_index_delete',
            sender=Document
        )
        post_delete.connect(
            document_metadata_index_post_delete,
            dispatch_uid='document_metadata_index_post_delete',
            sender=DocumentMetadata
        )
        post_document_created.connect(
            document_created_index_update,
            dispatch_uid='document_created_index_update', sender=Document
        )
        post_save.connect(
            document_metadata_index_update,
            dispatch_uid='document_metadata_index_update',
            sender=DocumentMetadata
        )
