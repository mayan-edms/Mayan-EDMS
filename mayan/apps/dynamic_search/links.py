from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import (
    icon_search, icon_search_advanced, icon_search_again,
)

link_search = Link(
    args='search_model.get_full_name', icon_class=icon_search,
    text=_('Search'), view='search:search'
)
link_search_advanced = Link(
    args='search_model.get_full_name', icon_class=icon_search_advanced,
    text=_('Advanced search'), view='search:search_advanced'
)
link_search_again = Link(
    args='search_model.get_full_name', icon_class=icon_search_again,
    keep_query=True, text=_('Search again'), view='search:search_again'
)
