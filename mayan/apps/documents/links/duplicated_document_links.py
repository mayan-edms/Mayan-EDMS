from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.converter.permissions import (
    permission_transformation_delete, permission_transformation_edit
)
from mayan.apps.navigation.classes import Link

from ..icons import (
    icon_document_list_recent_access, icon_recent_added_document_list,
    icon_duplicated_document_list, icon_duplicated_document_scan
)
from ..permissions import (
    permission_document_download, permission_document_properties_edit,
    permission_document_print, permission_document_tools,
    permission_document_view
)

link_document_duplicates_list = Link(
    args='resolved_object.id', icon_class=icon_duplicated_document_list,
    permissions=(permission_document_view,), text=_('Duplicates'),
    view='documents:document_duplicates_list',
)
link_duplicated_document_list = Link(
    icon_class=icon_duplicated_document_list, text=_('Duplicated documents'),
    view='documents:duplicated_document_list'
)
link_duplicated_document_scan = Link(
    icon_class=icon_duplicated_document_scan,
    permissions=(permission_document_tools,),
    text=_('Duplicated document scan'),
    view='documents:duplicated_document_scan'
)
