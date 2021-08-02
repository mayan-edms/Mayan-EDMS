from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link
from mayan.apps.navigation.utils import get_cascade_condition

from .icons import (
    icon_document_index_instance_list, icon_document_type_index_templates,
    icon_index, icon_index_instances_rebuild, icon_index_instances_reset,
    icon_index_template_create, icon_index_template_delete,
    icon_index_template_document_types, icon_index_template_edit,
    icon_index_template_list, icon_index_template_node_tree_view,
    icon_index_template_node_create, icon_index_template_node_delete,
    icon_index_template_node_edit
)
from .permissions import (
    permission_index_template_create, permission_index_template_edit,
    permission_index_template_delete,
    permission_index_instance_view,
    permission_index_template_rebuild, permission_index_template_view
)


def is_not_root_node(context):
    return not context['resolved_object'].is_root_node()


link_document_index_instance_list = Link(
    args='resolved_object.pk', icon=icon_document_index_instance_list,
    permissions=(permission_index_instance_view,),
    text=_('Indexes'), view='indexing:document_index_list'
)

link_document_type_index_templates = Link(
    args='resolved_object.pk', icon=icon_document_type_index_templates,
    permissions=(permission_index_template_create,),
    text=_('Index templates'), view='indexing:document_type_index_templates'
)

link_index_instance_menu = Link(
    condition=get_cascade_condition(
        app_label='document_indexing', model_name='IndexTemplate',
        object_permission=permission_index_instance_view,
    ), icon=icon_index,
    text=_('Indexes'), view='indexing:index_list'
)
link_index_instance_rebuild = Link(
    args='resolved_object.pk', icon=icon_index_instances_rebuild,
    permissions=(permission_index_template_rebuild,),
    text=_('Rebuild index'), view='indexing:index_template_rebuild'
)
link_index_instances_rebuild = Link(
    condition=get_cascade_condition(
        app_label='document_indexing', model_name='IndexTemplate',
        object_permission=permission_index_template_rebuild,
    ), description=_(
        'Deletes and creates from scratch all the document indexes.'
    ), icon=icon_index_instances_rebuild, text=_('Rebuild indexes'),
    view='indexing:rebuild_index_instances'
)
link_index_instances_reset = Link(
    condition=get_cascade_condition(
        app_label='document_indexing', model_name='IndexTemplate',
        object_permission=permission_index_template_rebuild,
    ), description=_(
        'Deletes and creates from scratch all the document indexes.'
    ), icon=icon_index_instances_reset, text=_('Reset indexes'),
    view='indexing:index_instances_reset'
)

link_index_template_setup = Link(
    condition=get_cascade_condition(
        app_label='document_indexing', model_name='IndexTemplate',
        object_permission=permission_index_template_view,
        view_permission=permission_index_template_create,
    ), icon=icon_index, text=_('Indexes'),
    view='indexing:index_template_list'
)
link_index_template_list = Link(
    icon=icon_index_template_list, text=_('Indexes'),
    view='indexing:index_template_list'
)
link_index_template_create = Link(
    icon=icon_index_template_create,
    permissions=(permission_index_template_create,),
    text=_('Create index'), view='indexing:index_template_create'
)
link_index_template_delete = Link(
    args='resolved_object.pk', icon=icon_index_template_delete,
    permissions=(permission_index_template_delete,), tags='dangerous',
    text=_('Delete'), view='indexing:index_template_delete',
)
link_index_template_document_types = Link(
    args='resolved_object.pk', icon=icon_index_template_document_types,
    permissions=(permission_index_template_edit,),
    text=_('Document types'), view='indexing:index_template_document_types'
)
link_index_template_edit = Link(
    args='resolved_object.pk', icon=icon_index_template_edit,
    permissions=(permission_index_template_edit,), text=_('Edit'),
    view='indexing:index_template_edit'
)

link_index_template_node_tree_view = Link(
    args='resolved_object.pk', icon=icon_index_template_node_tree_view,
    permissions=(permission_index_template_edit,), text=_('Tree template'),
    view='indexing:index_template_view'
)
link_index_template_node_create = Link(
    args='resolved_object.pk', icon=icon_index_template_node_create,
    text=_('New child node'), view='indexing:template_node_create'
)
link_index_template_node_delete = Link(
    args='resolved_object.pk', condition=is_not_root_node,
    icon=icon_index_template_node_delete, tags='dangerous',
    text=_('Delete'), view='indexing:template_node_delete'
)
link_index_template_node_edit = Link(
    args='resolved_object.pk', icon=icon_index_template_node_edit,
    condition=is_not_root_node, text=_('Edit'),
    view='indexing:template_node_edit'
)
