"""Configuration options for the web_theme app"""
from django.utils.translation import ugettext_lazy as _

from smart_settings.api import register_settings

register_settings(
    namespace=u'web_theme',
    module=u'web_theme.conf.settings',
    settings=[
        {'name': u'THEME', 'global_name': u'WEB_THEME_THEME', 'default': u'default', 'description': _(u'CSS theme to apply, options are: amro, bec, bec-green, blue, default, djime-cerulean, drastic-dark, kathleene, olive, orange, red, reidb-greenish and warehouse.')},
        {'name': u'ENABLE_SCROLL_JS', 'global_name': u'WEB_THEME_ENABLE_SCROLL_JS', 'default': True, 'hidden': True},
    ]
)
