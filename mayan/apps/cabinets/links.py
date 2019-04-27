from __future__ import absolute_import, unicode_literals

import copy

from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.links import link_acl_list
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.navigation.classes import Link
from mayan.apps.navigation.utils import get_cascade_condition

from .permissions import (
    permission_cabinet_add_document, permission_cabinet_create,
    permission_cabinet_delete, permission_cabinet_edit,
    permission_cabinet_view, permission_cabinet_remove_document
)

# Document links

link_document_cabinet_list = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.cabinets.icons.icon_cabinet_list',
    permissions=(permission_document_view,),
    text=_('Cabinets'), view='cabinets:document_cabinet_list',
)
link_document_cabinet_remove = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.cabinets.icons.icon_document_cabinet_remove',
    permissions=(permission_cabinet_remove_document,),
    text=_('Remove from cabinets'), view='cabinets:document_cabinet_remove'
)
link_document_cabinet_add = Link(
    args='object.pk',
    icon_class_path='mayan.apps.cabinets.icons.icon_document_cabinet_add',
    permissions=(permission_cabinet_add_document,), text=_('Add to cabinets'),
    view='cabinets:document_cabinet_add',
)
link_document_multiple_cabinet_add = Link(
    icon_class_path='mayan.apps.cabinets.icons.icon_document_multiple_cabinet_remove',
    text=_('Add to cabinets'), view='cabinets:document_multiple_cabinet_add'
)
link_multiple_document_cabinet_remove = Link(
    icon_class_path='mayan.apps.cabinets.icons.icon_document_cabinet_remove',
    text=_('Remove from cabinets'),
    view='cabinets:multiple_document_cabinet_remove'
)

# Cabinet links


def cabinet_is_root(context):
    return context[
        'resolved_object'
    ].is_root_node()


link_custom_acl_list = copy.copy(link_acl_list)
link_custom_acl_list.condition = cabinet_is_root

link_cabinet_child_add = Link(
    args='object.pk',
    icon_class_path='mayan.apps.cabinets.icons.icon_cabinet_child_add',
    permissions=(permission_cabinet_create,), text=_('Add new level'),
    view='cabinets:cabinet_child_add'
)
link_cabinet_create = Link(
    icon_class_path='mayan.apps.cabinets.icons.icon_cabinet_create',
    permissions=(permission_cabinet_create,),
    text=_('Create cabinet'), view='cabinets:cabinet_create'
)
link_cabinet_delete = Link(
    args='object.pk',
    icon_class_path='mayan.apps.cabinets.icons.icon_cabinet_delete',
    permissions=(permission_cabinet_delete,),
    tags='dangerous', text=_('Delete'), view='cabinets:cabinet_delete'
)
link_cabinet_edit = Link(
    args='object.pk',
    icon_class_path='mayan.apps.cabinets.icons.icon_cabinet_edit',
    permissions=(permission_cabinet_edit,), text=_('Edit'),
    view='cabinets:cabinet_edit'
)
link_cabinet_list = Link(
    condition=get_cascade_condition(
        app_label='cabinets', model_name='Cabinet',
        object_permission=permission_cabinet_view,
    ), icon_class_path='mayan.apps.cabinets.icons.icon_cabinet_list',
    text=_('All'), view='cabinets:cabinet_list'
)
link_cabinet_view = Link(
    args='object.pk', icon_class_path='mayan.apps.cabinets.icons.icon_cabinet_view',
    permissions=(permission_cabinet_view,), text=_('Details'),
    view='cabinets:cabinet_view'
)
