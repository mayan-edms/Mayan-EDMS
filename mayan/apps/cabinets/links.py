from __future__ import absolute_import, unicode_literals

import copy

from django.utils.translation import ugettext_lazy as _

from acls.links import link_acl_list
from documents.permissions import permission_document_view
from navigation import Link

from .icons import icon_cabinet_create, icon_cabinet_list
from .permissions import (
    permission_cabinet_add_document, permission_cabinet_create,
    permission_cabinet_delete, permission_cabinet_edit,
    permission_cabinet_view, permission_cabinet_remove_document
)

# Document links

link_document_cabinet_list = Link(
    args='resolved_object.pk', icon_class=icon_cabinet_list,
    permissions=(permission_document_view,),
    text=_('Cabinets'), view='cabinets:document_cabinet_list',
)
link_document_cabinet_remove = Link(
    args='resolved_object.pk',
    permissions=(permission_cabinet_remove_document,),
    text=_('Remove from cabinets'), view='cabinets:document_cabinet_remove'
)
link_cabinet_add_document = Link(
    args='object.pk', permissions=(permission_cabinet_add_document,),
    text=_('Add to cabinets'), view='cabinets:cabinet_add_document',
)
link_cabinet_add_multiple_documents = Link(
    text=_('Add to cabinets'), view='cabinets:cabinet_add_multiple_documents'
)
link_multiple_document_cabinet_remove = Link(
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
    args='object.pk', permissions=(permission_cabinet_create,),
    text=_('Add new level'), view='cabinets:cabinet_child_add'
)
link_cabinet_create = Link(
    icon_class=icon_cabinet_create, permissions=(permission_cabinet_create,),
    text=_('Create cabinet'), view='cabinets:cabinet_create'
)
link_cabinet_delete = Link(
    args='object.pk', permissions=(permission_cabinet_delete,),
    tags='dangerous', text=_('Delete'), view='cabinets:cabinet_delete'
)
link_cabinet_edit = Link(
    args='object.pk', permissions=(permission_cabinet_edit,), text=_('Edit'),
    view='cabinets:cabinet_edit'
)
link_cabinet_list = Link(
    icon_class=icon_cabinet_list, text=_('All'), view='cabinets:cabinet_list'
)
link_cabinet_view = Link(
    args='object.pk', permissions=(permission_cabinet_view,), text=_('Details'),
    view='cabinets:cabinet_view'
)
