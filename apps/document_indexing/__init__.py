from __future__ import absolute_import

import logging

from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver

from navigation.api import (register_top_menu, register_sidebar_template,
    bind_links, Link)

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

index_setup = Link(text=_(u'indexes'), view='index_setup_list', icon='tab.png', permissions=[PERMISSION_DOCUMENT_INDEXING_SETUP])#, children_view_regex=[r'^index_setup', r'^template_node'])
index_setup_list = Link(text=_(u'index list'), view='index_setup_list', sprite='tab', permissions=[PERMISSION_DOCUMENT_INDEXING_SETUP])
index_setup_create = Link(text=_(u'create index'), view='index_setup_create', sprite='tab_add', permissions=[PERMISSION_DOCUMENT_INDEXING_CREATE])
index_setup_edit = Link(text=_(u'edit'), view='index_setup_edit', args='index.pk', sprite='tab_edit', permissions=[PERMISSION_DOCUMENT_INDEXING_EDIT])
index_setup_delete = Link(text=_(u'delete'), view='index_setup_delete', args='index.pk', sprite='tab_delete', permissions=[PERMISSION_DOCUMENT_INDEXING_DELETE])
index_setup_view = Link(text=_(u'tree template'), view='index_setup_view', args='index.pk', sprite='textfield', permissions=[PERMISSION_DOCUMENT_INDEXING_SETUP])

template_node_create = Link(text=_(u'new child node'), view='template_node_create', args='node.pk', sprite='textfield_add', permissions=[PERMISSION_DOCUMENT_INDEXING_SETUP])
template_node_edit = Link(text=_(u'edit'), view='template_node_edit', args='node.pk', sprite='textfield', permissions=[PERMISSION_DOCUMENT_INDEXING_SETUP], conditional_disable=is_root_node)
template_node_delete = Link(text=_(u'delete'), view='template_node_delete', args='node.pk', sprite='textfield_delete', permissions=[PERMISSION_DOCUMENT_INDEXING_SETUP], conditional_disable=is_root_node)

index_list = Link(text=_(u'index list'), view='index_list', sprite='tab', permissions=[PERMISSION_DOCUMENT_INDEXING_VIEW])

index_parent = Link(text=_(u'go up one level'), view='index_instance_node_view', args='object.parent.pk', sprite='arrow_up', permissions=[PERMISSION_DOCUMENT_INDEXING_VIEW], dont_mark_active=True, condition=is_not_instance_root_node)
document_index_list = Link(text= _(u'indexes'), view='document_index_list', args='object.pk', sprite='folder_page', permissions=[PERMISSION_DOCUMENT_INDEXING_VIEW, PERMISSION_DOCUMENT_VIEW])

rebuild_index_instances = Link(text=_('rebuild indexes'), view='rebuild_index_instances', sprite='folder_page', permissions=[PERMISSION_DOCUMENT_INDEXING_REBUILD_INDEXES], description=_(u'Deletes and creates from scratch all the document indexes.'))

register_top_menu('indexes', link={'text': _('indexes'), 'sprite': 'tab', 'view': 'index_list', 'children_view_regex': [r'^index_[i,l]']})
register_maintenance_links([rebuild_index_instances], namespace='document_indexing', title=_(u'Indexes'))
register_sidebar_template(['index_instance_list'], 'indexing_help.html')

bind_links([IndexInstanceNode], [index_parent])
bind_links([Document], [document_index_list], menu_name='form_header')
bind_links([Index, 'index_setup_list', 'index_setup_create', 'template_node_edit', 'template_node_delete'], [index_setup_list, index_setup_create], menu_name='secondary_menu')
bind_links([Index], [index_setup_edit, index_setup_delete, index_setup_view])
bind_links([IndexTemplateNode], [template_node_create, template_node_edit, template_node_delete])

register_setup(index_setup)


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
