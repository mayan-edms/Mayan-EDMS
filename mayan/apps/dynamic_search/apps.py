from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import menu_facet, menu_secondary, menu_tools

from .classes import SearchModel
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
        super(DynamicSearchApp, self).ready()

        SearchModel.load_modules()
        SearchModel.initialize()

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
