from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.acls.permissions import permission_acl_edit, permission_acl_view
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import (
    menu_list_facet, menu_multi_item, menu_object, menu_secondary, menu_tools
)
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.navigation.classes import SourceColumn

from .events import (
    event_cache_edited, event_cache_partition_purged, event_cache_purged
)
from .links import (
    link_caches_list, link_cache_multiple_purge, link_cache_purge
)
from .permissions import permission_cache_purge, permission_cache_view


class FileCachingConfig(MayanAppConfig):
    app_namespace = 'file_caching'
    app_url = 'file_caching'
    has_tests = True
    name = 'mayan.apps.file_caching'
    verbose_name = _('File caching')

    def ready(self):
        super().ready()

        Cache = self.get_model(model_name='Cache')
        CachePartition = self.get_model(model_name='CachePartition')

        EventModelRegistry.register(model=Cache)
        EventModelRegistry.register(model=CachePartition)

        ModelEventType.register(
            event_types=(event_cache_edited, event_cache_purged,),
            model=Cache
        )
        ModelEventType.register(
            event_types=(event_cache_partition_purged,), model=CachePartition
        )

        ModelPermission.register(
            model=Cache, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_cache_purge, permission_cache_view
            )
        )

        SourceColumn(
            attribute='label', is_identifier=True, is_object_absolute_url=True, source=Cache
        )
        SourceColumn(
            attribute='get_maximum_size_display', include_label=True,
            is_sortable=True, sort_field='maximum_size', source=Cache
        )
        SourceColumn(
            attribute='get_total_size_display', include_label=True,
            source=Cache
        )

        menu_list_facet.bind_links(
            links=(link_acl_list,), sources=(Cache,)
        )

        menu_object.bind_links(
            links=(link_cache_purge,),
            sources=(Cache,)
        )
        menu_multi_item.bind_links(
            links=(link_cache_multiple_purge,),
            sources=(Cache,)
        )
        menu_secondary.bind_links(
            links=(link_caches_list,), sources=(
                Cache,
            )
        )

        menu_tools.bind_links(links=(link_caches_list,))
