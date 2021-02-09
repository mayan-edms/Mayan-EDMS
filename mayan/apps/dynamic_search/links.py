from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import (
    icon_search, icon_search_advanced, icon_search_again,
    icon_search_backend_reindex
)
from .permissions import permission_search_tools

link_search = Link(
    args='search_model.get_full_name', icon=icon_search,
    text=_('Search'), view='search:search'
)
link_search_advanced = Link(
    args='search_model.get_full_name', icon=icon_search_advanced,
    text=_('Advanced search'), view='search:search_advanced'
)
link_search_again = Link(
    args='search_model.get_full_name', icon=icon_search_again,
    keep_query=True, text=_('Search again'), view='search:search_again'
)
link_search_backend_reindex = Link(
    icon=icon_search_backend_reindex, permissions=(permission_search_tools,),
    text=_('Reindex search backend'), view='search:search_backend_reindex'
)
