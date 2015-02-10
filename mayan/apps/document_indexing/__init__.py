from __future__ import absolute_import, unicode_literals

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from documents.models import Document
from main.api import register_maintenance_links
from metadata.models import DocumentMetadata
from navigation.api import register_links, register_top_menu
from project_setup.api import register_setup
from rest_api.classes import APIEndPoint

from .links import (
    document_index_list, document_index_main_menu_link, index_parent,
    index_setup, index_setup_create, index_setup_document_types,
    index_setup_delete, index_setup_edit, index_setup_list, index_setup_view,
    rebuild_index_instances, template_node_create, template_node_delete,
    template_node_edit
)
from .models import Index, IndexTemplateNode, IndexInstanceNode
from .tasks import task_delete_empty_index_nodes, task_index_document


@receiver(post_delete, dispatch_uid='document_index_delete', sender=Document)
def document_index_delete(sender, **kwargs):
    task_delete_empty_index_nodes.apply_async(queue='indexing')


@receiver(post_save, dispatch_uid='document_metadata_index_update', sender=DocumentMetadata)
def document_metadata_index_update(sender, **kwargs):
    task_index_document.apply_async(kwargs=dict(document_id=kwargs['instance'].document.pk), queue='indexing')


@receiver(post_delete, dispatch_uid='document_metadata_index_post_delete', sender=DocumentMetadata)
def document_metadata_index_post_delete(sender, **kwargs):
    task_index_document.apply_async(kwargs=dict(document_id=kwargs['instance'].document.pk), queue='indexing')


register_maintenance_links([rebuild_index_instances], namespace='document_indexing', title=_('Indexes'))

register_links(Document, [document_index_list], menu_name='form_header')
register_links([Index, 'indexing:index_setup_list', 'indexing:index_setup_create'], [index_setup_list, index_setup_create], menu_name='secondary_menu')
register_links(Index, [index_setup_edit, index_setup_view, index_setup_document_types, index_setup_delete])
register_links(IndexInstanceNode, [index_parent])
register_links(IndexTemplateNode, [template_node_create, template_node_edit, template_node_delete])

register_setup(index_setup)

register_top_menu('indexes', document_index_main_menu_link)

APIEndPoint('indexes', app_name='document_indexing')
