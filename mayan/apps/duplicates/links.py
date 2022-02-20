from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.permissions import (
    permission_document_tools, permission_document_view
)
from mayan.apps.navigation.classes import Link

from .icons import (
    icon_duplicate_backend_list, icon_duplicated_document_list,
    icon_duplicated_document_scan
)

link_document_duplicate_backend_list = Link(
    args='resolved_object.id', icon=icon_duplicate_backend_list,
    permissions=(permission_document_view,), text=_('Duplicates'),
    view='duplicates:document_backend_list',
)
link_document_duplicate_backend_detail = Link(
    kwargs={
        'backend_id': 'resolved_object.id', 'document_id': 'document.id'
    },
    icon=icon_duplicated_document_list,
    permissions=(permission_document_view,), text=_('Documents'),
    view='duplicates:document_backend_detail',
)


link_duplicate_backend_list = Link(
    icon=icon_duplicate_backend_list, text=_('Duplicated documents'),
    view='duplicates:backend_list'
)

link_duplicate_backend_detail = Link(
    kwargs={'backend_id': 'resolved_object.id'},
    icon=icon_duplicated_document_list,
    text=_('Documents'),
    view='duplicates:backend_detail',
)
link_duplicate_document_scan = Link(
    icon=icon_duplicated_document_scan,
    permissions=(permission_document_tools,),
    text=_('Duplicated document scan'),
    view='duplicates:duplicated_document_scan'
)
