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
