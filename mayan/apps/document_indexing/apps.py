from __future__ import absolute_import, unicode_literals

from django import apps
from django.db.models.signals import post_save, post_delete
from django.utils.translation import ugettext_lazy as _

from common import (
    menu_facet, menu_main, menu_object, menu_secondary, menu_setup
)
from common.api import register_maintenance_links
from documents.models import Document
from metadata.models import DocumentMetadata
from rest_api.classes import APIEndPoint

from .links import (
    link_document_index_list, link_index_main_menu, link_index_parent,
    link_index_setup, link_index_setup_create, link_index_setup_document_types,
    link_index_setup_delete, link_index_setup_edit, link_index_setup_list,
    link_index_setup_view, link_rebuild_index_instances,
    link_template_node_create, link_template_node_delete,
    link_template_node_edit
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
        APIEndPoint('indexes', app_name='document_indexing')

        menu_facet.bind_links(links=[link_document_index_list], sources=[Document])
        menu_object.bind_links(links=[link_index_parent], sources=[IndexInstanceNode])
        menu_object.bind_links(links=[link_index_setup_edit, link_index_setup_view, link_index_setup_document_types, link_index_setup_delete], sources=[Index])
        menu_object.bind_links(links=[link_template_node_create, link_template_node_edit, link_template_node_delete], sources=[IndexTemplateNode])
        menu_main.bind_links(links=[link_index_main_menu])
        menu_secondary.bind_links(links=[link_index_setup_list, link_index_setup_create], sources=[Index, 'indexing:index_setup_list', 'indexing:index_setup_create'])
        menu_setup.bind_links(links=[link_index_setup])

        post_save.connect(document_metadata_index_update, dispatch_uid='document_metadata_index_update', sender=DocumentMetadata)
        post_delete.connect(document_index_delete, dispatch_uid='document_index_delete', sender=Document)
        post_delete.connect(document_metadata_index_post_delete, dispatch_uid='document_metadata_index_post_delete', sender=DocumentMetadata)

        register_maintenance_links([link_rebuild_index_instances], namespace='document_indexing', title=_('Indexes'))
