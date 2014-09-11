"""Configuration options for the dynamic_search app"""

from django.utils.translation import ugettext_lazy as _

from smart_settings.api import register_settings

register_settings(
    namespace=u'dynamic_search',
    module=u'dynamic_search.settings',
    settings=[
        {'name': u'SHOW_OBJECT_TYPE', 'global_name': u'SEARCH_SHOW_OBJECT_TYPE', 'default': True, 'hidden': True},
        {'name': u'LIMIT', 'global_name': u'SEARCH_LIMIT', 'default': 100, 'description': _(u'Maximum amount search hits to fetch and display.')},
        {'name': u'RECENT_COUNT', 'global_name': u'SEARCH_RECENT_COUNT', 'default': 5, 'description': _(u'Maximum number of search queries to remember per user.')},
    ]
)
