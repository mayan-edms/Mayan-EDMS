from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from ..icons import (
    icon_document_trash_send, icon_trash_can_empty,
    icon_trashed_document_delete, icon_trashed_document_list,
    icon_trashed_document_restore
)
from ..permissions import (
    permission_trashed_document_delete, permission_trashed_document_restore,
    permission_document_trash, permission_trash_empty
)


link_document_delete = Link(
    args='resolved_object.id', icon=icon_trashed_document_delete,
    permissions=(permission_trashed_document_delete,),
    tags='dangerous', text=_('Delete'), view='documents:document_delete'
)
link_document_trash = Link(
    args='resolved_object.id', icon=icon_document_trash_send,
    permissions=(permission_document_trash,), tags='dangerous',
    text=_('Move to trash'), view='documents:document_trash'
)
link_document_list_deleted = Link(
    icon=icon_trashed_document_list, text=_('Trash can'),
    view='documents:document_list_deleted'
)
link_document_restore = Link(
    args='object.pk', icon=icon_trashed_document_restore,
    permissions=(permission_trashed_document_restore,), text=_('Restore'),
    view='documents:document_restore'
)
link_document_multiple_trash = Link(
    icon=icon_document_trash_send, tags='dangerous',
    text=_('Move to trash'), view='documents:document_multiple_trash'
)
link_document_multiple_delete = Link(
    icon=icon_trashed_document_delete, tags='dangerous',
    text=_('Delete'), view='documents:document_multiple_delete'
)
link_document_multiple_restore = Link(
    icon=icon_trashed_document_restore, text=_('Restore'),
    view='documents:document_multiple_restore'
)
link_trash_can_empty = Link(
    icon=icon_trash_can_empty, permissions=(permission_trash_empty,),
    text=_('Empty trash'), view='documents:trash_can_empty'
)
