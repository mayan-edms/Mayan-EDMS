from __future__ import absolute_import, unicode_literals

from django import apps
from django.db.models.signals import post_save, post_delete
from django.utils.translation import ugettext_lazy as _

from common import menu_main, menu_setup
from documents.models import Document
from main.api import register_maintenance_links
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

        # TODO: convert
        #register_links(Document, [document_index_list], menu_name='form_header')
        #register_links([Index, 'indexing:index_setup_list', 'indexing:index_setup_create'], [index_setup_list, index_setup_create], menu_name='secondary_menu')
        #register_links(Index, [index_setup_edit, index_setup_view, index_setup_document_types, index_setup_delete])
        #register_links(IndexInstanceNode, [index_parent])
        #register_links(IndexTemplateNode, [template_node_create, template_node_edit, template_node_delete])

        menu_setup.bind_links(links=[link_index_setup])

        menu_main.bind_links(links=[link_index_main_menu])

        post_delete.connect(document_index_delete, dispatch_uid='document_index_delete', sender=Document)
        post_save.connect(document_metadata_index_update, dispatch_uid='document_metadata_index_update', sender=DocumentMetadata)
        post_delete.connect(document_metadata_index_post_delete, dispatch_uid='document_metadata_index_post_delete', sender=DocumentMetadata)

        register_maintenance_links([link_rebuild_index_instances], namespace='document_indexing', title=_('Indexes'))
