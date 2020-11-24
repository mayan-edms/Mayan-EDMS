from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link
from mayan.apps.navigation.utils import get_content_type_kwargs_factory
from mayan.apps.storage.classes import DefinedStorage

from .icons import (
    icon_cache_partition_purge, icon_cache_purge, icon_file_caching
)
from .permissions import permission_cache_purge, permission_cache_view


def condition_valid_storage(context):
    try:
        storage = DefinedStorage.get(name=context['object'].defined_storage_name)
    except KeyError:
        return False
    else:
        return storage


link_caches_list = Link(
    icon=icon_file_caching, permissions=(permission_cache_view,),
    text=_('File caches'), view='file_caching:cache_list'
)
link_cache_partition_purge = Link(
    icon=icon_cache_partition_purge, kwargs=get_content_type_kwargs_factory(
        variable_name='resolved_object'
    ), permissions=(permission_cache_purge,), text=_('Purge cache'),
    view='file_caching:cache_partitions_purge'
)
link_cache_purge = Link(
    condition=condition_valid_storage, icon=icon_cache_purge,
    kwargs={'cache_id': 'resolved_object.id'},
    permissions=(permission_cache_purge,), text=_('Purge cache'),
    view='file_caching:cache_purge'
)
link_cache_multiple_purge = Link(
    icon=icon_cache_purge, text=_('Purge cache'),
    view='file_caching:cache_multiple_purge'
)
