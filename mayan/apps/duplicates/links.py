from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.permissions import (
    permission_document_tools, permission_document_view
)
from mayan.apps.navigation.classes import Link

from .icons import (
    icon_duplicated_document_list, icon_duplicated_document_scan
)

link_document_duplicates_list = Link(
    args='resolved_object.id', icon=icon_duplicated_document_list,
    permissions=(permission_document_view,), text=_('Duplicates'),
    view='duplicates:document_duplicates_list',
)
link_duplicated_document_list = Link(
    icon=icon_duplicated_document_list, text=_('Duplicated documents'),
    view='duplicates:duplicated_document_list'
)
link_duplicated_document_scan = Link(
    icon=icon_duplicated_document_scan,
    permissions=(permission_document_tools,),
    text=_('Duplicated document scan'),
    view='duplicates:duplicated_document_scan'
)
