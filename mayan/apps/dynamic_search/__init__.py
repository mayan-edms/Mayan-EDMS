from __future__ import absolute_import

from navigation.api import (register_links, register_sidebar_template,
                            register_top_menu)

from .links import search, search_advanced, search_again, search_menu

register_sidebar_template(['search:search', 'search:search_advanced'], 'search_help.html')

register_links(['search:search', 'search:search_advanced', 'search:results'], [search, search_advanced], menu_name='form_header')
register_links(['search:results'], [search_again], menu_name='sidebar')

register_sidebar_template(['search:search', 'search:search_advanced', 'search:results'], 'recent_searches.html')
register_top_menu('search', search_menu)
