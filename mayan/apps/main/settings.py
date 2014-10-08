"""Configuration options for the main app"""

from django.utils.translation import ugettext_lazy as _
from smart_settings.api import register_setting, register_settings

register_settings(
    namespace=u'main',
    module=u'main.settings',
    settings=[
        {'name': u'ENABLE_SCROLL_JS', 'global_name': u'MAIN_ENABLE_SCROLL_JS', 'default': True, 'hidden': True},
    ]
)
