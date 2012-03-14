from __future__ import absolute_import

import logging

from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver

from navigation.api import (register_top_menu, register_sidebar_template,
    register_links)

from main.api import register_maintenance_links
from documents.permissions import PERMISSION_DOCUMENT_VIEW
from documents.models import Document, DocumentVersion
from metadata.models import DocumentMetadata
from project_setup.api import register_setup

from .models import (Index, IndexTemplateNode, IndexInstanceNode)
from .permissions import (PERMISSION_DOCUMENT_INDEXING_VIEW,
    PERMISSION_DOCUMENT_INDEXING_REBUILD_INDEXES,
    PERMISSION_DOCUMENT_INDEXING_SETUP,
    PERMISSION_DOCUMENT_INDEXING_CREATE,
    PERMISSION_DOCUMENT_INDEXING_EDIT,
    PERMISSION_DOCUMENT_INDEXING_DELETE
)
from .api import update_indexes, delete_indexes

def is_root_node(context):
    return context['node'].parent is None


def is_not_instance_root_node(context):
    return context['object'].parent is not None

logger = logging.getLogger(__name__)

index_setup = {'text': _(u'indexes'), 'view': 'index_setup_list', 'icon': 'tab.png', 'permissions': [PERMISSION_DOCUMENT_INDEXING_SETUP], 'children_view_regex': [r'^index_setup', r'^template_node']}
index_setup_list = {'text': _(u'index list'), 'view': 'index_setup_list', 'famfam': 'tab', 'permissions': [PERMISSION_DOCUMENT_INDEXING_SETUP]}
index_setup_create = {'text': _(u'create index'), 'view': 'index_setup_create', 'famfam': 'tab_add', 'permissions': [PERMISSION_DOCUMENT_INDEXING_CREATE]}
index_setup_edit = {'text': _(u'edit'), 'view': 'index_setup_edit', 'args': 'index.pk', 'famfam': 'tab_edit', 'permissions': [PERMISSION_DOCUMENT_INDEXING_EDIT]}
index_setup_delete = {'text': _(u'delete'), 'view': 'index_setup_delete', 'args': 'index.pk', 'famfam': 'tab_delete', 'permissions': [PERMISSION_DOCUMENT_INDEXING_DELETE]}
index_setup_view = {'text': _(u'tree template'), 'view': 'index_setup_view', 'args': 'index.pk', 'famfam': 'textfield', 'permissions': [PERMISSION_DOCUMENT_INDEXING_SETUP]}

template_node_create = {'text': _(u'new child node'), 'view': 'template_node_create', 'args': 'node.pk', 'famfam': 'textfield_add', 'permissions': [PERMISSION_DOCUMENT_INDEXING_SETUP]}
template_node_edit = {'text': _(u'edit'), 'view': 'template_node_edit', 'args': 'node.pk', 'famfam': 'textfield', 'permissions': [PERMISSION_DOCUMENT_INDEXING_SETUP], 'conditional_disable': is_root_node}
template_node_delete = {'text': _(u'delete'), 'view': 'template_node_delete', 'args': 'node.pk', 'famfam': 'textfield_delete', 'permissions': [PERMISSION_DOCUMENT_INDEXING_SETUP], 'conditional_disable': is_root_node}

index_list = {'text': _(u'index list'), 'view': 'index_list', 'famfam': 'tab', 'permissions': [PERMISSION_DOCUMENT_INDEXING_VIEW]}

index_parent = {'text': _(u'go up one level'), 'view': 'index_instance_node_view', 'args': 'object.parent.pk', 'famfam': 'arrow_up', 'permissions': [PERMISSION_DOCUMENT_INDEXING_VIEW], 'dont_mark_active': True, 'condition': is_not_instance_root_node}
document_index_list = {'text': _(u'indexes'), 'view': 'document_index_list', 'args': 'object.pk', 'famfam': 'folder_page', 'permissions': [PERMISSION_DOCUMENT_INDEXING_VIEW, PERMISSION_DOCUMENT_VIEW]}

register_top_menu('indexes', link={'text': _('indexes'), 'famfam': 'tab', 'view': 'index_list', 'children_view_regex': [r'^index_[i,l]']})

rebuild_index_instances = {'text': _('rebuild indexes'), 'view': 'rebuild_index_instances', 'famfam': 'folder_page', 'permissions': [PERMISSION_DOCUMENT_INDEXING_REBUILD_INDEXES], 'description': _(u'Deletes and creates from scratch all the document indexes.')}

register_maintenance_links([rebuild_index_instances], namespace='document_indexing', title=_(u'Indexes'))

register_sidebar_template(['index_instance_list'], 'indexing_help.html')

register_links(IndexInstanceNode, [index_parent])

register_links(Document, [document_index_list], menu_name='form_header')

register_setup(index_setup)

register_links([Index, 'index_setup_list', 'index_setup_create', 'template_node_edit', 'template_node_delete'], [index_setup_list, index_setup_create], menu_name='secondary_menu')

register_links(Index, [index_setup_edit, index_setup_delete, index_setup_view])

register_links(IndexTemplateNode, [template_node_create, template_node_edit, template_node_delete])


def delete_indexes_handler(sender, instance, **kwargs):
    if isinstance(instance, DocumentVersion):
        logger.debug('received pre save signal - document version')
        logger.debug('instance: %s' % instance)
        delete_indexes(instance.document)
    elif isinstance(instance, DocumentMetadata):
        logger.debug('received pre save signal - document metadata')
        logger.debug('instance: %s' % instance)
        delete_indexes(instance.document)


@receiver(post_save, dispatch_uid='update_indexes_handler')
def update_indexes_handler(sender, instance, **kwargs):
    if isinstance(instance, DocumentVersion):
        logger.debug('received post save signal - document version')
        logger.debug('instance: %s' % instance)
        update_indexes(instance.document)
    elif isinstance(instance, DocumentMetadata):
        logger.debug('received post save signal - document metadata')
        logger.debug('instance: %s' % instance)
        update_indexes(instance.document)
        
pre_save.connect(delete_indexes_handler, dispatch_uid='delete_indexes_handler_on_update')
pre_delete.connect(delete_indexes_handler, dispatch_uid='delete_indexes_handler_on_delete')
