from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_top_menu
from rest_api.classes import APIEndPoint

from .links import search, search_advanced, search_again, search_menu
from .urls import api_urls

register_links(['search:search', 'search:search_advanced', 'search:results'], [search, search_advanced], menu_name='form_header')
register_links(['search:results'], [search_again], menu_name='sidebar')

register_top_menu('search', search_menu)

endpoint = APIEndPoint('search')
endpoint.register_urls(api_urls)
endpoint.add_endpoint('recentsearch-list', _(u'Returns a list of all recent searches.'))
endpoint.add_endpoint('search-view', _(u'Perform a search operaton.'))
