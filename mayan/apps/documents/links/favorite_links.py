from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from ..permissions import permission_document_view


link_document_list_favorites = Link(
    icon_class_path='mayan.apps.documents.icons.icon_favorite_document_list',
    text=_('Favorites'),
    view='documents:document_list_favorites'
)
link_document_favorites_add = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.documents.icons.icon_favorite_document_add',
    permissions=(permission_document_view,), text=_('Add to favorites'),
    view='documents:document_add_to_favorites',
)
link_document_favorites_remove = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.documents.icons.icon_favorite_document_remove',
    permissions=(permission_document_view,), text=_('Remove from favorites'),
    view='documents:document_remove_from_favorites',
)
link_document_multiple_favorites_add = Link(
    text=_('Add to favorites'),
    icon_class_path='mayan.apps.documents.icons.icon_favorite_document_add',
    view='documents:document_multiple_add_to_favorites',
)
link_document_multiple_favorites_remove = Link(
    text=_('Remove from favorites'),
    icon_class_path='mayan.apps.documents.icons.icon_favorite_document_remove',
    view='documents:document_multiple_remove_from_favorites',
)
