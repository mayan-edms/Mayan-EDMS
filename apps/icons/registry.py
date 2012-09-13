from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from smart_settings import LocalScope

from .icons import icon_icons_app
from .literals import DEFAULT_ICON_SET

name = 'icons'
label = _(u'Icons')
description = _(u'Handles the registration and rendering of icons and sprites.')
dependencies = ['app_registry']
icon = icon_icons_app
settings = [
    {
        'name': 'ICON_SET',
        'default': DEFAULT_ICON_SET,
        'description': _(u'Icon set to use to render all the icon in the project.'),
        'scopes': [LocalScope()] # TODO: Cluster, Org, User
    }
]
