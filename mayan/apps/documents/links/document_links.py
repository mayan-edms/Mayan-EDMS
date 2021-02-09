from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from ..icons import (
    icon_document_edit, icon_document_recently_accessed_list, icon_document_list,
    icon_document_preview, icon_document_properties,
    icon_document_type_change, icon_document_recently_created_list
)
from ..permissions import (
    permission_document_properties_edit, permission_document_view
)


link_document_type_change = Link(
    args='resolved_object.id', icon=icon_document_type_change,
    permissions=(permission_document_properties_edit,), text=_('Change type'),
    view='documents:document_type_change'
)
link_document_list = Link(
    icon=icon_document_list,
    text=_('All documents'), view='documents:document_list'
)
link_document_recently_accessed_list = Link(
    icon=icon_document_recently_accessed_list, text=_('Recently accessed'),
    view='documents:document_recently_accessed_list'
)
link_document_recently_created_list = Link(
    icon=icon_document_recently_created_list, text=_('Recently created'),
    view='documents:document_recently_created_list'
)
link_document_multiple_type_change = Link(
    text=_('Change type'), icon=icon_document_type_change,
    view='documents:document_multiple_type_change'
)
link_document_preview = Link(
    args='resolved_object.id', icon=icon_document_preview,
    permissions=(permission_document_view,), text=_('Preview'),
    view='documents:document_preview'
)
link_document_properties = Link(
    args='resolved_object.id', icon=icon_document_properties,
    permissions=(permission_document_view,), text=_('Properties'),
    view='documents:document_properties'
)
link_document_properties_edit = Link(
    args='resolved_object.id',
    icon=icon_document_edit,
    permissions=(permission_document_properties_edit,),
    text=_('Edit properties'), view='documents:document_properties_edit'
)
