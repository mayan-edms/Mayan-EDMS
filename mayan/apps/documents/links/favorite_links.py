from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from ..icons import (
    icon_favorite_document_add, icon_favorite_document_add_multiple,
    icon_favorite_document_list, icon_favorite_document_remove,
    icon_favorite_document_remove_multiple
)
from ..permissions import permission_document_view


def condition_is_in_favorites(context):
    return context['resolved_object'].favorites.exists()


def condition_not_is_in_favorites(context):
    return not context['resolved_object'].favorites.exists()


link_document_list_favorites = Link(
    icon=icon_favorite_document_list, text=_('Favorites'),
    view='documents:document_favorite_list'
)
link_document_favorites_add = Link(
    args='resolved_object.id', condition=condition_not_is_in_favorites,
    icon=icon_favorite_document_add, permissions=(permission_document_view,),
    text=_('Favorites: add'), view='documents:document_favorite_add'
)
link_document_favorites_remove = Link(
    args='resolved_object.id', condition=condition_is_in_favorites,
    icon=icon_favorite_document_remove,
    permissions=(permission_document_view,), text=_('Favorites: remove'),
    view='documents:document_favorite_remove'
)
link_document_favorites_add_multiple = Link(
    text=_('Favorites: add'), icon=icon_favorite_document_add_multiple,
    view='documents:document_multiple_favorite_add'
)
link_document_favorites_remove_multiple = Link(
    text=_('Favorites: remove'), icon=icon_favorite_document_remove_multiple,
    view='documents:document_multiple_favorite_remove'
)
