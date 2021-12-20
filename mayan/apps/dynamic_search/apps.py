from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import menu_facet, menu_secondary, menu_tools
from mayan.apps.common.signals import (
    signal_post_initial_setup, signal_post_upgrade
)

from .classes import SearchBackend, SearchModel
from .handlers import (
    handler_search_backend_initialize, handler_search_backend_upgrade
)
from .links import (
    link_search, link_search_advanced, link_search_again,
    link_search_backend_reindex
)


class DynamicSearchApp(MayanAppConfig):
    app_namespace = 'search'
    app_url = 'search'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.dynamic_search'
    verbose_name = _('Dynamic search')

    def ready(self):
        super().ready()

        SearchModel.load_modules()
        SearchBackend._enable()

        menu_facet.bind_links(
            links=(link_search, link_search_advanced),
            sources=(
                'search:search', 'search:search_advanced', 'search:results'
            )
        )
        menu_secondary.bind_links(
            links=(link_search_again,), sources=('search:results',)
        )
        menu_tools.bind_links(
            links=(link_search_backend_reindex,),
        )

        signal_post_initial_setup.connect(
            dispatch_uid='search_handler_search_backend_initialize',
            receiver=handler_search_backend_initialize
        )

        signal_post_upgrade.connect(
            dispatch_uid='search_handler_search_backend_upgrade',
            receiver=handler_search_backend_upgrade
        )
