from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import icon_search_backend_reindex
from .permissions import permission_search_tools

link_search = Link(
    text=_('Search'), view='search:search', args='search_model.get_full_name'
)
link_search_advanced = Link(
    text=_('Advanced search'), view='search:search_advanced',
    args='search_model.get_full_name'
)
link_search_again = Link(
    text=_('Search again'), view='search:search_again',
    args='search_model.get_full_name', keep_query=True
)
link_search_backend_reindex = Link(
    icon_class=icon_search_backend_reindex, permissions=(permission_search_tools,),
    text=_('Reindex search backend'), view='search:search_backend_reindex'
)
