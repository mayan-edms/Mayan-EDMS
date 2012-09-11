"""
Configuration options for the web_theme app
"""

from django.utils.translation import ugettext_lazy as _

from smart_settings import SettingsNamespace, LocalScope

namespace = SettingsNamespace(name='web_theme', label=_(u'Web theme'), module='web_theme.settings')

namespace.add_setting(
    name='THEME',
    default=u'activo',
    description=_(u'CSS theme to apply, options are: amro, bec, bec-green, blue, default, djime-cerulean, drastic-dark, kathleene, olive, orange, red, reidb-greenish and warehouse.'),
    scopes=[LocalScope()]
)

namespace.add_setting(
    name='ENABLE_SCROLL_JS',
    default=True,
    hidden=True,
    scopes=[LocalScope()]
)

namespace.add_setting(
    name='VERBOSE_LOGIN',
    default=True,
    description=_(u'Display extra information in the login screen.'),
    scopes=[LocalScope()]
)
