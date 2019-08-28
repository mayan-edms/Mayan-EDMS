from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.permissions import permission_document_type_edit
from mayan.apps.navigation.classes import Link
from mayan.apps.navigation.utils import get_cascade_condition

from .permissions import (
    permission_document_indexing_create, permission_document_indexing_edit,
    permission_document_indexing_delete,
    permission_document_indexing_instance_view,
    permission_document_indexing_rebuild, permission_document_indexing_view
)


def is_not_root_node(context):
    return not context['resolved_object'].is_root_node()


link_document_index_instance_list = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_indexing.icons.icon_document_index_instance_list',
    text=_('Indexes'), view='indexing:document_index_list',
)

link_document_type_index_templates = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_indexing.icons.icon_document_type_index_templates',
    permissions=(permission_document_type_edit,), text=_('Index templates'),
    view='indexing:document_type_index_templates',
)

link_index_instance_menu = Link(
    condition=get_cascade_condition(
        app_label='document_indexing', model_name='Index',
        object_permission=permission_document_indexing_instance_view,
    ), icon_class_path='mayan.apps.document_indexing.icons.icon_index',
    text=_('Indexes'), view='indexing:index_list'
)
link_index_instances_rebuild = Link(
    condition=get_cascade_condition(
        app_label='document_indexing', model_name='Index',
        object_permission=permission_document_indexing_rebuild,
    ),
    icon_class_path='mayan.apps.document_indexing.icons.icon_index_instances_rebuild',
    description=_(
        'Deletes and creates from scratch all the document indexes.'
    ),
    text=_('Rebuild indexes'), view='indexing:rebuild_index_instances'
)
link_index_instance_rebuild = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_indexing.icons.icon_index_instances_rebuild',
    permissions=(permission_document_indexing_rebuild,),
    text=_('Rebuild index'), view='indexing:index_setup_rebuild'
)

link_index_template_setup = Link(
    condition=get_cascade_condition(
        app_label='document_indexing', model_name='Index',
        object_permission=permission_document_indexing_view,
        view_permission=permission_document_indexing_create,
    ), icon_class_path='mayan.apps.document_indexing.icons.icon_index',
    text=_('Indexes'), view='indexing:index_setup_list'
)
link_index_template_list = Link(
    icon_class_path='mayan.apps.document_indexing.icons.icon_index_template_list',
    text=_('Indexes'), view='indexing:index_setup_list'
)
link_index_template_create = Link(
    icon_class_path='mayan.apps.document_indexing.icons.icon_index_template_create',
    permissions=(permission_document_indexing_create,), text=_('Create index'),
    view='indexing:index_setup_create'
)
link_index_template_delete = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_indexing.icons.icon_index_template_delete',
    permissions=(permission_document_indexing_delete,), tags='dangerous',
    text=_('Delete'), view='indexing:index_setup_delete',
)
link_index_template_document_types = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_indexing.icons.icon_index_template_document_types',
    permissions=(permission_document_indexing_edit,), text=_('Document types'),
    view='indexing:index_setup_document_types',
)
link_index_template_edit = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_indexing.icons.icon_index_template_edit',
    permissions=(permission_document_indexing_edit,), text=_('Edit'),
    view='indexing:index_setup_edit',
)

link_index_template_node_tree_view = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_indexing.icons.icon_index_template_node_tree_view',
    permissions=(permission_document_indexing_edit,), text=_('Tree template'),
    view='indexing:index_setup_view',
)
link_index_template_node_create = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_indexing.icons.icon_index_template_node_create',
    text=_('New child node'),
    view='indexing:template_node_create',
)
link_index_template_node_delete = Link(
    args='resolved_object.pk', condition=is_not_root_node,
    icon_class_path='mayan.apps.document_indexing.icons.icon_index_template_node_delete',
    tags='dangerous', text=_('Delete'), view='indexing:template_node_delete',
)
link_index_template_node_edit = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.document_indexing.icons.icon_index_template_node_edit',
    condition=is_not_root_node, text=_('Edit'),
    view='indexing:template_node_edit',
)
