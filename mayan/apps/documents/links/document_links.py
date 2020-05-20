from django.utils.translation import ugettext_lazy as _

from mayan.apps.converter.permissions import (
    permission_transformation_delete, permission_transformation_edit
)
from mayan.apps.navigation.classes import Link

from ..icons import (
    icon_document_list_recent_access, icon_recent_added_document_list
)
from ..permissions import (
    permission_document_download, permission_document_properties_edit,
    permission_document_print, permission_document_view
)


link_document_clear_transformations = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.documents.icons.icon_document_transformations_clear',
    permissions=(permission_transformation_delete,),
    text=_('Clear transformations'),
    view='documents:document_clear_transformations',
)
link_document_clone_transformations = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.documents.icons.icon_document_transformations_clone',
    permissions=(permission_transformation_edit,),
    text=_('Clone transformations'),
    view='documents:document_clone_transformations',
)
link_document_document_type_edit = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.documents.icons.icon_document_type_change',
    permissions=(permission_document_properties_edit,), text=_('Change type'),
    view='documents:document_document_type_edit',
)
link_document_download = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.documents.icons.icon_document_download',
    permissions=(permission_document_download,), text=_('Advanced download'),
    view='documents:document_download_form',
)
link_document_edit = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.documents.icons.icon_document_edit',
    permissions=(permission_document_properties_edit,),
    text=_('Edit properties'), view='documents:document_edit',
)
link_document_list = Link(
    icon_class_path='mayan.apps.documents.icons.icon_document_list',
    text=_('All documents'),
    view='documents:document_list'
)
link_document_list_recent_access = Link(
    icon_class=icon_document_list_recent_access, text=_('Recently accessed'),
    view='documents:document_list_recent_access'
)
link_document_list_recent_added = Link(
    icon_class=icon_recent_added_document_list, text=_('Recently added'),
    view='documents:document_list_recent_added'
)
link_document_multiple_clear_transformations = Link(
    icon_class_path='mayan.apps.documents.icons.icon_document_transformations_clear',
    permissions=(permission_transformation_delete,),
    text=_('Clear transformations'),
    view='documents:document_multiple_clear_transformations'
)
link_document_multiple_document_type_edit = Link(
    text=_('Change type'),
    icon_class_path='mayan.apps.documents.icons.icon_document_type_change',
    view='documents:document_multiple_document_type_edit'
)
link_document_multiple_download = Link(
    icon_class_path='mayan.apps.documents.icons.icon_document_download',
    text=_('Advanced download'),
    view='documents:document_multiple_download_form'
)
link_document_preview = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.documents.icons.icon_document_preview',
    permissions=(permission_document_view,),
    text=_('Preview'), view='documents:document_preview',
)
link_document_properties = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.documents.icons.icon_document_properties',
    permissions=(permission_document_view,),
    text=_('Properties'), view='documents:document_properties',
)
link_document_print = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.documents.icons.icon_document_print',
    permissions=(permission_document_print,),
    text=_('Print'), view='documents:document_print',
)
link_document_quick_download = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.documents.icons.icon_document_quick_download',
    permissions=(permission_document_download,), text=_('Quick download'),
    view='documents:document_download',
)
