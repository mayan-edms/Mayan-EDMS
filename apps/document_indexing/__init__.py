from __future__ import absolute_import

import logging

from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from app_registry.models import App
from documents.models import Document
from maintenance.api import MaintenanceNamespace
from metadata.models import DocumentMetadata
from navigation.api import (register_top_menu, register_sidebar_template,
    bind_links, Link)
from project_setup.api import register_setup

from .api import update_indexes, delete_indexes
from .links import (index_setup, index_setup_list, index_setup_create,
    index_setup_edit, index_setup_delete, index_setup_view,
    template_node_create, template_node_edit, template_node_delete,
    index_parent, document_index_list, rebuild_index_instances,
    index_setup_document_types)
from .models import (Index, IndexTemplateNode, IndexInstanceNode)

logger = logging.getLogger(__name__)

register_top_menu('indexes', link=Link(text=_('indexes'), sprite='tab', view='index_list', children_view_regex=[r'^index_[i,l]']))

namespace = MaintenanceNamespace(_(u'indexes'))
namespace.create_tool(rebuild_index_instances)

register_sidebar_template(['index_instance_list'], 'indexing_help.html')

bind_links([IndexInstanceNode], [index_parent])
bind_links([Document], [document_index_list], menu_name='form_header')
bind_links([Index, 'index_setup_list', 'index_setup_create', 'template_node_edit', 'template_node_delete'], [index_setup_list, index_setup_create], menu_name='secondary_menu')
bind_links([Index], [index_setup_edit, index_setup_delete, index_setup_view, index_setup_document_types])
bind_links([IndexTemplateNode], [template_node_create, template_node_edit, template_node_delete])

register_setup(index_setup)


@receiver(post_save, dispatch_uid='document_index_update', sender=Document)
def document_index_update(sender, **kwargs):
    # TODO: save result in index log
    delete_indexes(kwargs['instance'])
    update_indexes(kwargs['instance'])


@receiver(pre_delete, dispatch_uid='document_index_delete', sender=Document)
def document_index_delete(sender, **kwargs):
    # TODO: save result in index log
    delete_indexes(kwargs['instance'])


@receiver(post_save, dispatch_uid='document_metadata_index_update', sender=DocumentMetadata)
def document_metadata_index_update(sender, **kwargs):
    # TODO: save result in index log
    delete_indexes(kwargs['instance'].document)
    update_indexes(kwargs['instance'].document)


@receiver(pre_delete, dispatch_uid='document_metadata_index_delete', sender=DocumentMetadata)
def document_metadata_index_delete(sender, **kwargs):
    # TODO: save result in index log
    delete_indexes(kwargs['instance'].document)


@receiver(post_delete, dispatch_uid='document_metadata_index_post_delete', sender=DocumentMetadata)
def document_metadata_index_post_delete(sender, **kwargs):
    # TODO: save result in index log
    update_indexes(kwargs['instance'].document)

try:
    app = App.register('document_indexing', _(u'Document indexing'))
except App.UnableToRegister:
    pass
else:
    app.set_dependencies(['app_registry', 'documents'])
#aelse:
#    AppBackup(app, [ModelBackup()])
