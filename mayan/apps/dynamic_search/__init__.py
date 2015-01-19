from __future__ import unicode_literals

from navigation.api import register_links
from rest_api.classes import APIEndPoint

from .links import search, search_advanced, search_again

register_links(['search:search', 'search:search_advanced', 'search:results'], [search, search_advanced], menu_name='form_header')
register_links(['search:results'], [search_again], menu_name='sidebar')

APIEndPoint('search', app_name='dynamic_search')
