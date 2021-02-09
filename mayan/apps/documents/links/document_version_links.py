from django.utils.translation import ugettext_lazy as _

from mayan.apps.converter.permissions import (
    permission_transformation_delete, permission_transformation_edit
)
from mayan.apps.navigation.classes import Link

from ..icons import (
    icon_document_version_active, icon_document_version_create,
    icon_document_version_delete, icon_document_version_edit,
    icon_document_version_export, icon_document_version_list,
    icon_document_version_print, icon_document_version_return_document,
    icon_document_version_return_list, icon_document_version_preview,
    icon_document_version_transformations_clear,
    icon_document_version_transformations_clone
)
from ..permissions import (
    permission_document_version_create, permission_document_version_delete,
    permission_document_version_edit, permission_document_version_export,
    permission_document_version_print, permission_document_version_view,
    permission_document_view
)


link_document_version_active = Link(
    args='resolved_object.pk',
    icon=icon_document_version_active,
    permissions=(permission_document_version_edit,),
    text=_('Make active'), view='documents:document_version_active'
)
link_document_version_create = Link(
    args='resolved_object.pk', icon=icon_document_version_create,
    permissions=(permission_document_version_create,),
    text=_('Create document version'),
    view='documents:document_version_create'
)
link_document_version_delete = Link(
    args='resolved_object.pk',
    icon=icon_document_version_delete,
    permissions=(permission_document_version_delete,), tags='dangerous',
    text=_('Delete'), view='documents:document_version_delete'
)
link_document_version_edit = Link(
    args='resolved_object.pk', icon=icon_document_version_edit,
    permissions=(permission_document_version_edit,),
    text=_('Edit'), view='documents:document_version_edit'
)
link_document_version_export = Link(
    args='resolved_object.pk', icon=icon_document_version_export,
    permissions=(permission_document_version_export,),
    text=_('Export'), view='documents:document_version_export'
)
link_document_version_multiple_delete = Link(
    icon=icon_document_version_delete, tags='dangerous',
    text=_('Delete'), view='documents:document_version_multiple_delete'
)
link_document_version_list = Link(
    args='resolved_object.pk', icon=icon_document_version_list,
    permissions=(permission_document_version_view,), text=_('Versions'),
    view='documents:document_version_list'
)
link_document_version_preview = Link(
    args='resolved_object.pk', icon=icon_document_version_preview,
    permissions=(permission_document_version_view,),
    text=_('Preview'), view='documents:document_version_preview'
)
link_document_version_print_form = Link(
    args='resolved_object.id', icon=icon_document_version_print,
    permissions=(permission_document_version_print,), text=_('Print'),
    view='documents:document_version_print_form'
)
link_document_version_return_to_document = Link(
    args='resolved_object.document.pk',
    icon=icon_document_version_return_document,
    permissions=(permission_document_view,), text=_('Document'),
    view='documents:document_preview'
)
link_document_version_return_list = Link(
    args='resolved_object.document.pk',
    icon=icon_document_version_return_list,
    permissions=(permission_document_version_view,), text=_('Versions'),
    view='documents:document_version_list'
)
link_document_version_transformations_clear = Link(
    args='resolved_object.id',
    icon=icon_document_version_transformations_clear,
    permissions=(permission_transformation_delete,),
    text=_('Clear transformations'),
    view='documents:document_version_transformations_clear'
)
link_document_version_multiple_transformations_clear = Link(
    icon=icon_document_version_transformations_clear,
    permissions=(permission_transformation_delete,),
    text=_('Clear transformations'),
    view='documents:document_version_multiple_transformations_clear'
)
link_document_version_transformations_clone = Link(
    args='resolved_object.id',
    icon=icon_document_version_transformations_clone,
    permissions=(permission_transformation_edit,),
    text=_('Clone transformations'),
    view='documents:document_version_transformations_clone'
)
