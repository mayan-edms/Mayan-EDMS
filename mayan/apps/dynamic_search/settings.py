from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from smart_settings.api import register_settings

register_settings(
    namespace='dynamic_search',
    module='dynamic_search.settings',
    settings=[
        {'name': 'SHOW_OBJECT_TYPE', 'global_name': 'SEARCH_SHOW_OBJECT_TYPE', 'default': True, 'hidden': True},
        {'name': 'LIMIT', 'global_name': 'SEARCH_LIMIT', 'default': 100, 'description': _('Maximum amount search hits to fetch and display.')},
        {'name': 'RECENT_COUNT', 'global_name': 'SEARCH_RECENT_COUNT', 'default': 5, 'description': _('Maximum number of search queries to remember per user.')},
    ]
)
