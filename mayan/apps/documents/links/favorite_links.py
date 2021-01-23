from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from ..icons import (
    icon_favorite_document_add, icon_favorite_document_list,
    icon_favorite_document_remove
)
from ..permissions import permission_document_view


link_document_list_favorites = Link(
    icon=icon_favorite_document_list, text=_('Favorites'),
    view='documents:document_favorite_list'
)
link_document_favorites_add = Link(
    args='resolved_object.id', icon=icon_favorite_document_add,
    permissions=(permission_document_view,), text=_('Add to favorites'),
    view='documents:document_favorite_add'
)
link_document_favorites_remove = Link(
    args='resolved_object.id', icon=icon_favorite_document_remove,
    permissions=(permission_document_view,), text=_('Remove from favorites'),
    view='documents:document_favorite_remove'
)
link_document_multiple_favorites_add = Link(
    text=_('Add to favorites'), icon=icon_favorite_document_add,
    view='documents:document_multiple_favorite_add'
)
link_document_multiple_favorites_remove = Link(
    text=_('Remove from favorites'), icon=icon_favorite_document_remove,
    view='documents:document_multiple_favorite_remove'
)
