from __future__ import absolute_import

from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from documents.models import Document
from main.api import register_maintenance_links
from metadata.models import DocumentMetadata
from navigation.api import (register_top_menu, register_sidebar_template,
    register_links)
from project_setup.api import register_setup

from .api import update_indexes, delete_indexes
from .links import (index_setup, index_setup_list, index_setup_create, index_setup_edit,
    index_setup_delete, index_setup_view, index_setup_document_types, template_node_create,
    template_node_edit, template_node_delete, index_parent, document_index_list,
    rebuild_index_instances, document_index_main_menu_link)
from .models import Index, IndexTemplateNode, IndexInstanceNode


@receiver(pre_delete, dispatch_uid='document_index_delete', sender=Document)
def document_index_delete(sender, **kwargs):
    delete_indexes(kwargs['instance'])


@receiver(post_save, dispatch_uid='document_metadata_index_update', sender=DocumentMetadata)
def document_metadata_index_update(sender, **kwargs):
    delete_indexes(kwargs['instance'].document)
    update_indexes(kwargs['instance'].document)


@receiver(pre_delete, dispatch_uid='document_metadata_index_delete', sender=DocumentMetadata)
def document_metadata_index_delete(sender, **kwargs):
    delete_indexes(kwargs['instance'].document)


@receiver(post_delete, dispatch_uid='document_metadata_index_post_delete', sender=DocumentMetadata)
def document_metadata_index_post_delete(sender, **kwargs):
    update_indexes(kwargs['instance'].document)


register_top_menu('indexes', document_index_main_menu_link)

register_maintenance_links([rebuild_index_instances], namespace='document_indexing', title=_(u'Indexes'))

register_sidebar_template(['index_instance_list'], 'indexing_help.html')

register_links(IndexInstanceNode, [index_parent])

register_links(Document, [document_index_list], menu_name='form_header')

register_setup(index_setup)

register_links([Index, 'index_setup_list', 'index_setup_create', 'template_node_edit', 'template_node_delete'], [index_setup_list, index_setup_create], menu_name='secondary_menu')

register_links(Index, [index_setup_edit, index_setup_delete, index_setup_view, index_setup_document_types])

register_links(IndexTemplateNode, [template_node_create, template_node_edit, template_node_delete])
