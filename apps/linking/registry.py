from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from smart_settings import LocalScope

#from .icons import icon_tick

label = _(u'Document linking')
#description = _(u'Contains many commonly used models, views and utilities.')
dependencies = ['app_registry', 'icons', 'navigation', 'documents', 'metadata']
#icon = icon_tick
settings = [
    {
        'name': 'SHOW_EMPTY_SMART_LINKS',
        'default': True,
        'description': _(u'Show smart link that don\'t return any documents.'),
        'scopes': [LocalScope()]
    }
]
