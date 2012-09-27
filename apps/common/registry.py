from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from smart_settings import ClusterScope, LocalScope

from .icons import icon_tick
from .links import link_admin_site
from .literals import (DEFAULT_TEMPORARY_DIRECTORY, DEFAULT_PAGE_SIZE, 
    DEFAULT_PAGE_ORIENTATION, DEFAULT_LOGIN_METHOD)

label = _(u'Common')
description = _(u'Contains many commonly used models, views and utilities.')
dependencies = ['app_registry']
icon = icon_tick
setup_links = [link_admin_site]
settings=[
    {
        'name': 'TEMPORARY_DIRECTORY',
        'default': DEFAULT_TEMPORARY_DIRECTORY,
        'description': _(u'Temporary directory used site wide to store thumbnails, previews and temporary files.  If none is specified, one will be created using tempfile.mkdtemp().'),
        'exists': True,
        'scopes': [LocalScope()]
    },
    {
        'name': 'DEFAULT_PAPER_SIZE',
        'default': DEFAULT_PAGE_SIZE,
        'scopes': [ClusterScope()]
    },
    {
        'name': 'DEFAULT_PAGE_ORIENTATION',
        'default': DEFAULT_PAGE_ORIENTATION,
        'description': _(u'Password of the superuser admin that will be created.'),
        'scopes': [ClusterScope()]
    },
    {
        'name': 'LOGIN_METHOD',
        'default': DEFAULT_LOGIN_METHOD,
        'description': _(u'Controls the mechanism used to authenticated user.  Options are: username, email.'),
        'scopes': [ClusterScope()]
    },
    {
        'name': 'ALLOW_ANONYMOUS_ACCESS',
        'default': False,
        'description': _(u'Allow non authenticated users, access to all views.'),
        'scopes': [ClusterScope()]
    }
]
