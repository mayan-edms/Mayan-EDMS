from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from ..icons import (
    icon_favorite_document_add, icon_favorite_document_list,
    icon_favorite_document_remove
)
from ..permissions import permission_document_view


def condition_is_in_favorites(context, resolved_object):
    return resolved_object.favorites.exists()


def condition_not_is_in_favorites(context, resolved_object):
    return not resolved_object.favorites.exists()


link_document_favorites_list = Link(
    icon=icon_favorite_document_list, text=_('Favorites'),
    view='documents:document_favorite_list'
)
link_document_favorites_add = Link(
    condition=condition_not_is_in_favorites,
    args='resolved_object.id', icon=icon_favorite_document_add,
    permissions=(permission_document_view,), text=_('Add to favorites'),
    view='documents:document_favorite_add'
)
link_document_favorites_remove = Link(
    condition=condition_is_in_favorites,
    args='resolved_object.id', icon=icon_favorite_document_remove,
    permissions=(permission_document_view,), text=_('Remove from favorites'),
    view='documents:document_favorite_remove'
)
link_document_favorites_add_multiple = Link(
    text=_('Add to favorites'), icon=icon_favorite_document_add,
    view='documents:document_favorite_add_multiple'
)
link_document_favorites_remove_multiple = Link(
    text=_('Remove from favorites'), icon=icon_favorite_document_remove,
    view='documents:document_favorite_remove_multiple'
)
