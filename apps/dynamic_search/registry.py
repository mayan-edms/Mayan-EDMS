from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from smart_settings import LocalScope

from .icons import icon_search
from .links import menu_link

label = _(u'Search')
description = _(u'Handles document search and search indexing.')
dependencies = ['app_registry', 'icons', 'navigation']
icon = icon_search
menu_links = [menu_link]
settings = [
    {
        'name': 'INDEX_UPDATE_INTERVAL',
        'default': 1800,
        'description': _(u'Interval in second on which to trigger the search index update.'),
        'scopes': [LocalScope()]
    }
]
