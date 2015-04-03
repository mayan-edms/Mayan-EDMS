from __future__ import absolute_import, unicode_literals

from django import apps
from django.db.models.signals import post_save, post_delete
from django.utils.translation import ugettext_lazy as _

from common.menus import menu_main
from documents.models import Document
from main.api import register_maintenance_links
from metadata.models import DocumentMetadata
from navigation.api import register_links
from project_setup.api import register_setup
from rest_api.classes import APIEndPoint

from .links import (
    document_index_list, link_index_main_menu, index_parent,
    index_setup, index_setup_create, index_setup_document_types,
    index_setup_delete, index_setup_edit, index_setup_list, index_setup_view,
    link_rebuild_index_instances, template_node_create, template_node_delete,
    template_node_edit
)
from .models import Index, IndexTemplateNode, IndexInstanceNode
from .tasks import task_delete_empty_index_nodes, task_index_document


def document_index_delete(sender, **kwargs):
    task_delete_empty_index_nodes.apply_async(queue='indexing')


def document_metadata_index_update(sender, **kwargs):
    task_index_document.apply_async(kwargs=dict(document_id=kwargs['instance'].document.pk), queue='indexing')


def document_metadata_index_post_delete(sender, **kwargs):
    task_index_document.apply_async(kwargs=dict(document_id=kwargs['instance'].document.pk), queue='indexing')


class DocumentIndexingApp(apps.AppConfig):
    name = 'document_indexing'
    verbose_name = _('Document indexing')

    def ready(self):
        post_delete.connect(document_index_delete, dispatch_uid='document_index_delete', sender=Document)
        post_save.connect(document_metadata_index_update, dispatch_uid='document_metadata_index_update', sender=DocumentMetadata)
        post_delete.connect(document_metadata_index_post_delete, dispatch_uid='document_metadata_index_post_delete', sender=DocumentMetadata)

        register_maintenance_links([link_rebuild_index_instances], namespace='document_indexing', title=_('Indexes'))

        register_links(Document, [document_index_list], menu_name='form_header')
        register_links([Index, 'indexing:index_setup_list', 'indexing:index_setup_create'], [index_setup_list, index_setup_create], menu_name='secondary_menu')
        register_links(Index, [index_setup_edit, index_setup_view, index_setup_document_types, index_setup_delete])
        register_links(IndexInstanceNode, [index_parent])
        register_links(IndexTemplateNode, [template_node_create, template_node_edit, template_node_delete])

        register_setup(index_setup)

        menu_main.bind_links(links=[link_index_main_menu])

        APIEndPoint('indexes', app_name='document_indexing')
