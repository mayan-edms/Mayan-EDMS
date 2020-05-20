from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from ..permissions import (
    permission_document_delete, permission_document_restore,
    permission_document_trash, permission_empty_trash
)


link_document_delete = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.documents.icons.icon_trashed_document_delete',
    permissions=(permission_document_delete,),
    tags='dangerous', text=_('Delete'), view='documents:document_delete',

)
link_document_trash = Link(
    args='resolved_object.id', permissions=(permission_document_trash,),
    icon_class_path='mayan.apps.documents.icons.icon_document_trash_send',
    tags='dangerous', text=_('Move to trash'),
    view='documents:document_trash',
)
link_document_list_deleted = Link(
    icon_class_path='mayan.apps.documents.icons.icon_trashed_document_list',
    text=_('Trash can'), view='documents:document_list_deleted'
)
link_document_restore = Link(
    permissions=(permission_document_restore,),
    icon_class_path='mayan.apps.documents.icons.icon_trashed_document_restore',
    text=_('Restore'),
    view='documents:document_restore', args='object.pk'
)
link_document_multiple_trash = Link(
    icon_class_path='mayan.apps.documents.icons.icon_document_trash_send',
    tags='dangerous', text=_('Move to trash'),
    view='documents:document_multiple_trash'
)
link_document_multiple_delete = Link(
    icon_class_path='mayan.apps.documents.icons.icon_trashed_document_delete',
    tags='dangerous', text=_('Delete'),
    view='documents:document_multiple_delete'
)
link_document_multiple_restore = Link(
    icon_class_path='mayan.apps.documents.icons.icon_trashed_document_restore',
    text=_('Restore'), view='documents:document_multiple_restore'
)
link_trash_can_empty = Link(
    permissions=(permission_empty_trash,), text=_('Empty trash'),
    view='documents:trash_can_empty'
)
