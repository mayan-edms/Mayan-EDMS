from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from ..icons import (
    icon_document_type_create, icon_document_type_delete,
    icon_document_type_edit, icon_document_type_setup,
)
from ..permissions import (
    permission_document_type_create, permission_document_type_delete,
    permission_document_type_edit, permission_document_type_view,
)


link_document_type_create = Link(
    icon_class=icon_document_type_create,
    permissions=(permission_document_type_create,),
    text=_('Create document type'), view='documents:document_type_create'
)
link_document_type_delete = Link(
    args='resolved_object.id', icon_class=icon_document_type_delete,
    permissions=(permission_document_type_delete,), tags='dangerous',
    text=_('Delete'), view='documents:document_type_delete',
)
link_document_type_policies = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.documents.icons.icon_document_type_policies',
    permissions=(permission_document_type_edit,),
    text=_('Deletion policies'), view='documents:document_type_policies',
)
link_document_type_edit = Link(
    args='resolved_object.id', icon_class=icon_document_type_edit,
    permissions=(permission_document_type_edit,), text=_('Edit'),
    view='documents:document_type_edit',
)
link_document_type_filename_create = Link(
    args='document_type.id',
    icon_class_path='mayan.apps.documents.icons.icon_document_type_filename_create',
    permissions=(permission_document_type_edit,),
    text=_('Add quick label to document type'),
    view='documents:document_type_filename_create',
)
link_document_type_filename_delete = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.documents.icons.icon_document_type_filename_delete',
    permissions=(permission_document_type_edit,),
    tags='dangerous', text=_('Delete'),
    view='documents:document_type_filename_delete',
)
link_document_type_filename_edit = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.documents.icons.icon_document_type_filename_edit',
    permissions=(permission_document_type_edit,),
    text=_('Edit'), view='documents:document_type_filename_edit',
)
link_document_type_filename_list = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.documents.icons.icon_document_type_filename_list',
    permissions=(permission_document_type_view,),
    text=_('Quick labels'), view='documents:document_type_filename_list',
)
link_document_type_filename_generator = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.documents.icons.icon_document_type_filename_generator',
    permissions=(permission_document_type_edit,),
    text=_('Filename generation'), view='documents:document_type_filename_generator',
)
link_document_type_list = Link(
    icon_class_path='mayan.apps.documents.icons.icon_document_type_list',
    permissions=(permission_document_type_view,), text=_('Document types'),
    view='documents:document_type_list'
)
link_document_type_setup = Link(
    icon_class=icon_document_type_setup,
    permissions=(permission_document_type_view,), text=_('Document types'),
    view='documents:document_type_list'
)
