from django.utils.translation import ugettext_lazy as _

from mayan.apps.converter.permissions import (
    permission_transformation_delete, permission_transformation_edit
)
from mayan.apps.navigation.classes import Link

from ..icons import (
    icon_document_file_delete, icon_document_file_download_quick,
    icon_document_file_edit, icon_document_file_list,
    icon_document_file_print, icon_document_file_properties,
    icon_document_file_return_to_document, icon_document_file_return_list,
    icon_document_file_preview, icon_document_file_transformations_clear,
    icon_document_file_transformations_clone
)
from ..permissions import (
    permission_document_file_delete, permission_document_file_download,
    permission_document_file_edit, permission_document_file_print,
    permission_document_file_view, permission_document_view
)

link_document_file_delete = Link(
    args='object.pk',
    icon=icon_document_file_delete,
    permissions=(permission_document_file_delete,), tags='dangerous',
    text=_('Delete'), view='documents:document_file_delete',
)
link_document_file_delete_multiple = Link(
    icon=icon_document_file_delete,
    permissions=(permission_document_file_delete,), tags='dangerous',
    text=_('Delete'), view='documents:document_file_delete_multiple',
)
link_document_file_edit = Link(
    args='object.pk', icon=icon_document_file_edit,
    permissions=(permission_document_file_edit,),
    text=_('Edit'), view='documents:document_file_edit',
)
link_document_file_download_quick = Link(
    args='resolved_object.id', icon=icon_document_file_download_quick,
    permissions=(permission_document_file_download,),
    text=_('Quick download'), view='documents:document_file_download'
)
link_document_file_list = Link(
    args='resolved_object.pk',
    icon=icon_document_file_list,
    permissions=(permission_document_file_view,),
    text=_('Files'), view='documents:document_file_list',
)
link_document_file_print_form = Link(
    args='resolved_object.id', icon=icon_document_file_print,
    permissions=(permission_document_file_print,), text=_('Print'),
    view='documents:document_file_print_form'
)
link_document_file_properties = Link(
    args='resolved_object.id',
    icon=icon_document_file_properties,
    permissions=(permission_document_file_view,),
    text=_('Properties'), view='documents:document_file_properties',
)
link_document_file_return_to_document = Link(
    args='resolved_object.document.pk',
    icon=icon_document_file_return_to_document,
    permissions=(permission_document_view,), text=_('Document'),
    view='documents:document_preview',
)
link_document_file_return_list = Link(
    args='resolved_object.document.pk',
    icon=icon_document_file_return_list,
    permissions=(permission_document_file_view,), text=_('Files'),
    view='documents:document_file_list',
)
link_document_file_preview = Link(
    args='resolved_object.pk',
    icon=icon_document_file_preview,
    permissions=(permission_document_file_view,),
    text=_('Preview'), view='documents:document_file_preview'
)
link_document_file_transformations_clear = Link(
    args='resolved_object.id',
    icon=icon_document_file_transformations_clear,
    permissions=(permission_transformation_delete,),
    text=_('Clear transformations'),
    view='documents:document_file_transformations_clear'
)
link_document_file_multiple_transformations_clear = Link(
    icon=icon_document_file_transformations_clear,
    permissions=(permission_transformation_delete,),
    text=_('Clear transformations'),
    view='documents:document_file_multiple_transformations_clear'
)
link_document_file_transformations_clone = Link(
    args='resolved_object.id',
    icon=icon_document_file_transformations_clone,
    permissions=(permission_transformation_edit,),
    text=_('Clone transformations'),
    view='documents:document_file_transformations_clone'
)
