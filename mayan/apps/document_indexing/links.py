from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link, get_cascade_condition

from .icons import (
    icon_document_index_list, icon_index, icon_index_create,
    icon_rebuild_index_instances,
)
from .permissions import (
    permission_document_indexing_create, permission_document_indexing_edit,
    permission_document_indexing_delete,
    permission_document_indexing_instance_view,
    permission_document_indexing_rebuild, permission_document_indexing_view
)


def is_not_root_node(context):
    return not context['resolved_object'].is_root_node()


link_document_index_list = Link(
    args='resolved_object.pk', icon_class=icon_document_index_list,
    text=_('Indexes'), view='indexing:document_index_list',
)
link_index_main_menu = Link(
    condition=get_cascade_condition(
        app_label='document_indexing', model_name='Index',
        object_permission=permission_document_indexing_instance_view,
    ), icon_class=icon_index, text=_('Indexes'),
    view='indexing:index_list'
)
link_index_setup = Link(
    condition=get_cascade_condition(
        app_label='document_indexing', model_name='Index',
        object_permission=permission_document_indexing_view,
        view_permission=permission_document_indexing_create,
    ), icon_class=icon_index, text=_('Indexes'),
    view='indexing:index_setup_list'
)
link_index_setup_list = Link(
    text=_('Indexes'), view='indexing:index_setup_list'
)
link_index_setup_create = Link(
    icon_class=icon_index_create,
    permissions=(permission_document_indexing_create,), text=_('Create index'),
    view='indexing:index_setup_create'
)
link_index_setup_edit = Link(
    args='resolved_object.pk',
    permissions=(permission_document_indexing_edit,), text=_('Edit'),
    view='indexing:index_setup_edit',
)
link_index_setup_delete = Link(
    args='resolved_object.pk',
    permissions=(permission_document_indexing_delete,), tags='dangerous',
    text=_('Delete'), view='indexing:index_setup_delete',
)
link_index_setup_view = Link(
    args='resolved_object.pk',
    permissions=(permission_document_indexing_edit,), text=_('Tree template'),
    view='indexing:index_setup_view',
)
link_index_setup_document_types = Link(
    args='resolved_object.pk',
    permissions=(permission_document_indexing_edit,), text=_('Document types'),
    view='indexing:index_setup_document_types',
)
link_rebuild_index_instances = Link(
    condition=get_cascade_condition(
        app_label='document_indexing', model_name='Index',
        object_permission=permission_document_indexing_rebuild,
    ), icon_class=icon_rebuild_index_instances,
    description=_(
        'Deletes and creates from scratch all the document indexes.'
    ),
    text=_('Rebuild indexes'), view='indexing:rebuild_index_instances'
)
link_template_node_create = Link(
    args='resolved_object.pk', text=_('New child node'),
    view='indexing:template_node_create',
)
link_template_node_edit = Link(
    args='resolved_object.pk', condition=is_not_root_node, text=_('Edit'),
    view='indexing:template_node_edit',
)
link_template_node_delete = Link(
    args='resolved_object.pk', condition=is_not_root_node, tags='dangerous',
    text=_('Delete'), view='indexing:template_node_delete',
)
