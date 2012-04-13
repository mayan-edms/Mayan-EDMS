"""Configuration options for the dynamic_search app"""

from django.utils.translation import ugettext_lazy as _

from smart_settings.api import Setting, SettingNamespace

namespace = SettingNamespace('dynamic_search', _(u'Searching'), module='dynamic_search.conf.settings')

Setting(
    namespace=namespace,
    name='RECENT_COUNT',
    global_name='SEARCH_RECENT_COUNT',
    default=5,
    description=_(u'Maximum number of search queries to remember per user.')
)

Setting(
    namespace=namespace,
    name='INDEX_UPDATE_INTERVAL',
    global_name='SEARCH_INDEX_UPDATE_INTERVAL',
    default=1800,
    description=_(u'Interval in second on which to trigger the search index update.')
)
