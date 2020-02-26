from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.permissions import permission_document_type_edit
from mayan.apps.navigation.classes import Link

from .permissions import (
    permission_metadata_add, permission_metadata_edit,
    permission_metadata_remove, permission_metadata_view,
    permission_metadata_type_create, permission_metadata_type_delete,
    permission_metadata_type_edit, permission_metadata_type_view
)

link_metadata_add = Link(
    args='object.pk',
    icon_class_path='mayan.apps.metadata.icons.icon_document_metadata_add',
    permissions=(permission_metadata_add,), text=_('Add metadata'),
    view='metadata:metadata_add',
)
link_metadata_edit = Link(
    args='object.pk',
    icon_class_path='mayan.apps.metadata.icons.icon_document_metadata_edit',
    permissions=(permission_metadata_edit,),
    text=_('Edit metadata'), view='metadata:metadata_edit'
)
link_metadata_multiple_add = Link(
    icon_class_path='mayan.apps.metadata.icons.icon_document_metadata_add',
    text=_('Add metadata'), view='metadata:metadata_multiple_add'
)
link_metadata_multiple_edit = Link(
    icon_class_path='mayan.apps.metadata.icons.icon_document_metadata_edit',
    text=_('Edit metadata'), view='metadata:metadata_multiple_edit'
)
link_metadata_multiple_remove = Link(
    icon_class_path='mayan.apps.metadata.icons.icon_document_metadata_remove',
    text=_('Remove metadata'), view='metadata:metadata_multiple_remove'
)
link_metadata_remove = Link(
    args='object.pk',
    icon_class_path='mayan.apps.metadata.icons.icon_document_metadata_remove',
    permissions=(permission_metadata_remove,),
    text=_('Remove metadata'), view='metadata:metadata_remove',
)
link_metadata_view = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.metadata.icons.icon_document_metadata_view',
    permissions=(permission_metadata_view,), text=_('Metadata'),
    view='metadata:metadata_view',
)
link_setup_document_type_metadata_types = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.metadata.icons.icon_document_type_metadata_type_list',
    permissions=(permission_document_type_edit,),
    text=_('Metadata types'), view='metadata:setup_document_type_metadata_types',
)
link_setup_metadata_type_document_types = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.metadata.icons.icon_metadata_type_document_type_list',
    permissions=(permission_document_type_edit,),
    text=_('Document types'), view='metadata:setup_metadata_type_document_types',
)
link_setup_metadata_type_create = Link(
    icon_class_path='mayan.apps.metadata.icons.icon_metadata_type_create',
    permissions=(permission_metadata_type_create,), text=_('Create new'),
    view='metadata:setup_metadata_type_create'
)
link_setup_metadata_type_delete = Link(
    args='object.pk',
    icon_class_path='mayan.apps.metadata.icons.icon_metadata_type_delete',
    permissions=(permission_metadata_type_delete,),
    tags='dangerous', text=_('Delete'), view='metadata:setup_metadata_type_delete',
)
link_setup_metadata_type_edit = Link(
    args='object.pk',
    icon_class_path='mayan.apps.metadata.icons.icon_metadata_type_edit',
    permissions=(permission_metadata_type_edit,),
    text=_('Edit'), view='metadata:setup_metadata_type_edit'
)
link_setup_metadata_type_list = Link(
    icon_class_path='mayan.apps.metadata.icons.icon_metadata_type_list',
    permissions=(permission_metadata_type_view,),
    text=_('Metadata types'), view='metadata:setup_metadata_type_list'
)
