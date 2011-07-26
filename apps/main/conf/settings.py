"""Configuration options for the main app"""

from django.utils.translation import ugettext_lazy as _
from smart_settings.api import register_setting

register_setting(
    namespace=u'main',
    module=u'main.conf.settings',
    name=u'SIDE_BAR_SEARCH',
    global_name=u'MAIN_SIDE_BAR_SEARCH',
    default=False,
    description=_(u'Controls whether the search functionality is provided by a sidebar widget or by a menu entry.')
)

register_setting(
    namespace=u'main',
    module=u'main.conf.settings',
    name=u'DISABLE_HOME_VIEW',
    global_name=u'MAIN_DISABLE_HOME_VIEW',
    default=False,
)

register_setting(
    namespace=u'main',
    module=u'main.conf.settings',
    name=u'DISABLE_ICONS',
    global_name=u'MAIN_DISABLE_ICONS',
    default=False,
)
