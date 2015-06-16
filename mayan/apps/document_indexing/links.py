from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from documents.permissions import PERMISSION_DOCUMENT_VIEW
from navigation import Link

from .permissions import (
    PERMISSION_DOCUMENT_INDEXING_CREATE, PERMISSION_DOCUMENT_INDEXING_EDIT,
    PERMISSION_DOCUMENT_INDEXING_DELETE,
    PERMISSION_DOCUMENT_INDEXING_REBUILD_INDEXES,
    PERMISSION_DOCUMENT_INDEXING_SETUP, PERMISSION_DOCUMENT_INDEXING_VIEW
)


def is_not_instance_root_node(context):
    return not context['object'].is_root_node()


def is_not_root_node(context):
    return not context['resolved_object'].is_root_node()


link_document_index_list = Link(permissions=[PERMISSION_DOCUMENT_INDEXING_VIEW, PERMISSION_DOCUMENT_VIEW], text=_('Indexes'), view='indexing:document_index_list', args='object.pk')
link_index_list = Link(permissions=[PERMISSION_DOCUMENT_INDEXING_VIEW], text=_('Index list'), view='indexing:index_list')
link_index_main_menu = Link(icon='fa fa-list-ul', text=_('Indexes'), view='indexing:index_list')
link_index_parent = Link(condition=is_not_instance_root_node, permissions=[PERMISSION_DOCUMENT_INDEXING_VIEW], text=_('Go up one level'), view='indexing:index_instance_node_view', args='object.parent.pk')
link_index_setup = Link(icon='fa fa-list-ul', permissions=[PERMISSION_DOCUMENT_INDEXING_SETUP], text=_('Indexes'), view='indexing:index_setup_list')
link_index_setup_list = Link(permissions=[PERMISSION_DOCUMENT_INDEXING_SETUP], text=_('Indexes'), view='indexing:index_setup_list')
link_index_setup_create = Link(permissions=[PERMISSION_DOCUMENT_INDEXING_CREATE], text=_('Create index'), view='indexing:index_setup_create')
link_index_setup_edit = Link(permissions=[PERMISSION_DOCUMENT_INDEXING_EDIT], text=_('Edit'), view='indexing:index_setup_edit', args='resolved_object.pk')
link_index_setup_delete = Link(permissions=[PERMISSION_DOCUMENT_INDEXING_DELETE], tags='dangerous', text=_('Delete'), view='indexing:index_setup_delete', args='resolved_object.pk')
link_index_setup_view = Link(permissions=[PERMISSION_DOCUMENT_INDEXING_SETUP], text=_('Tree template'), view='indexing:index_setup_view', args='resolved_object.pk')
link_index_setup_document_types = Link(permissions=[PERMISSION_DOCUMENT_INDEXING_EDIT], text=_('Document types'), view='indexing:index_setup_document_types', args='resolved_object.pk')
link_rebuild_index_instances = Link(
    description=_('Deletes and creates from scratch all the document indexes.'),
    permissions=[PERMISSION_DOCUMENT_INDEXING_REBUILD_INDEXES],
    text=_('Rebuild indexes'), view='indexing:rebuild_index_instances'
)
link_template_node_create = Link(permissions=[PERMISSION_DOCUMENT_INDEXING_SETUP], text=_('New child node'), view='indexing:template_node_create', args='resolved_object.pk')
link_template_node_edit = Link(condition=is_not_root_node, permissions=[PERMISSION_DOCUMENT_INDEXING_SETUP], text=_('Edit'), view='indexing:template_node_edit', args='resolved_object.pk')
link_template_node_delete = Link(condition=is_not_root_node, permissions=[PERMISSION_DOCUMENT_INDEXING_SETUP], tags='dangerous', text=_('Delete'), view='indexing:template_node_delete', args='resolved_object.pk')
