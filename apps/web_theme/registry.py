from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from smart_settings import LocalScope

from .icons import icon_web_theme

label = _(u'Web theme')
description = _(u'Handles UI rendering.')
dependencies = ['app_registry', 'icons']
icon = icon_web_theme
settings = [
    {
        'name': 'THEME',
        'default': u'activo',
        'description': _(u'CSS theme to apply, options are: amro, bec, bec-green, blue, default, djime-cerulean, drastic-dark, kathleene, olive, orange, red, reidb-greenish and warehouse.'),
        'scopes': [LocalScope()]
    },
    {
        'name': 'ENABLE_SCROLL_JS',
        'default': True,
        'hidden': True,
        'scopes': [LocalScope()]
    },
    {
        'name': 'VERBOSE_LOGIN',
        'default': True,
        'description': _(u'Display extra information in the login screen.'),
        'scopes': [LocalScope()]
    },
]
