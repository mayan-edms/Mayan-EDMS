from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import icon_cache_purge, icon_file_caching
from .permissions import permission_cache_purge, permission_cache_view

link_caches_list = Link(
    icon_class=icon_file_caching, permissions=(permission_cache_view,),
    text=_('File caches'), view='file_caching:cache_list'
)
link_cache_purge = Link(
    icon_class=icon_cache_purge, kwargs={'cache_id': 'resolved_object.id'},
    permissions=(permission_cache_purge,), text=_('Purge cache'),
    view='file_caching:cache_purge'
)
link_cache_multiple_purge = Link(
    icon_class=icon_cache_purge, text=_('Purge cache'),
    view='file_caching:cache_multiple_purge'
)
