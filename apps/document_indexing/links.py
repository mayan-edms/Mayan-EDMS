from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link
from documents.permissions import PERMISSION_DOCUMENT_VIEW

from .permissions import (PERMISSION_DOCUMENT_INDEXING_VIEW,
    PERMISSION_DOCUMENT_INDEXING_REBUILD_INDEXES,
    PERMISSION_DOCUMENT_INDEXING_SETUP,
    PERMISSION_DOCUMENT_INDEXING_CREATE,
    PERMISSION_DOCUMENT_INDEXING_EDIT,
    PERMISSION_DOCUMENT_INDEXING_DELETE
)


def is_root_node(context):
    return context['node'].parent is None


def is_not_instance_root_node(context):
    return context['object'].parent is not None

index_setup = Link(text=_(u'indexes'), view='index_setup_list', icon='tab.png', permissions=[PERMISSION_DOCUMENT_INDEXING_SETUP])  # children_view_regex=[r'^index_setup', r'^template_node'])
index_setup_list = Link(text=_(u'index list'), view='index_setup_list', sprite='tab', permissions=[PERMISSION_DOCUMENT_INDEXING_SETUP])
index_setup_create = Link(text=_(u'create index'), view='index_setup_create', sprite='tab_add', permissions=[PERMISSION_DOCUMENT_INDEXING_CREATE])
index_setup_edit = Link(text=_(u'edit'), view='index_setup_edit', args='index.pk', sprite='tab_edit', permissions=[PERMISSION_DOCUMENT_INDEXING_EDIT])
index_setup_delete = Link(text=_(u'delete'), view='index_setup_delete', args='index.pk', sprite='tab_delete', permissions=[PERMISSION_DOCUMENT_INDEXING_DELETE])
index_setup_view = Link(text=_(u'tree template'), view='index_setup_view', args='index.pk', sprite='textfield', permissions=[PERMISSION_DOCUMENT_INDEXING_SETUP])
index_setup_document_types = Link(text=_(u'document types'), view='index_setup_document_types', args='index.pk', sprite='layout', permissions=[PERMISSION_DOCUMENT_INDEXING_EDIT])  # children_view_regex=[r'^index_setup', r'^template_node'])

template_node_create = Link(text=_(u'new child node'), view='template_node_create', args='node.pk', sprite='textfield_add', permissions=[PERMISSION_DOCUMENT_INDEXING_EDIT])
template_node_edit = Link(text=_(u'edit'), view='template_node_edit', args='node.pk', sprite='textfield', permissions=[PERMISSION_DOCUMENT_INDEXING_EDIT], conditional_disable=is_root_node)
template_node_delete = Link(text=_(u'delete'), view='template_node_delete', args='node.pk', sprite='textfield_delete', permissions=[PERMISSION_DOCUMENT_INDEXING_EDIT], conditional_disable=is_root_node)

index_list = Link(text=_(u'index list'), view='index_list', sprite='tab', permissions=[PERMISSION_DOCUMENT_INDEXING_VIEW])

index_parent = Link(text=_(u'go up one level'), view='index_instance_node_view', args='object.parent.pk', sprite='arrow_up', permissions=[PERMISSION_DOCUMENT_INDEXING_VIEW], dont_mark_active=True, condition=is_not_instance_root_node)
document_index_list = Link(text=_(u'indexes'), view='document_index_list', args='object.pk', sprite='folder_page', permissions=[PERMISSION_DOCUMENT_INDEXING_VIEW, PERMISSION_DOCUMENT_VIEW])

rebuild_index_instances = Link(text=_('rebuild indexes'), view='rebuild_index_instances', sprite='folder_page', permissions=[PERMISSION_DOCUMENT_INDEXING_REBUILD_INDEXES], description=_(u'Deletes and creates from scratch all the document indexes.'))
