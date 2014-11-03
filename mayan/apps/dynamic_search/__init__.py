from __future__ import absolute_import

from navigation.api import register_links, register_top_menu
from rest_api.classes import APIEndPoint

from .links import search, search_advanced, search_again, search_menu

register_links(['search:search', 'search:search_advanced', 'search:results'], [search, search_advanced], menu_name='form_header')
register_links(['search:results'], [search_again], menu_name='sidebar')

register_top_menu('search', search_menu)

APIEndPoint('search', app_name='dynamic_search')
