from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from navigation.api import register_top_menu
from navigation.api import register_links
from project_setup.api import register_setup
from project_tools.api import register_tool

from .conf.settings import SIDE_BAR_SEARCH, DISABLE_HOME_VIEW
from .links import (admin_site, diagnostics, maintenance_menu, sentry, statistics)

__author__ = 'Roberto Rosario'
__copyright__ = 'Copyright 2012 Roberto Rosario'
__credits__ = ['Roberto Rosario',]
__license__ = 'GPL'
__maintainer__ = 'Roberto Rosario'
__email__ = 'roberto.rosario.gonzalez@gmail.com'
__status__ = 'Production'

__version_info__ = {
    'major': 1,
    'minor': 0,
    'micro': 0,
    'releaselevel': 'beta',
    'serial': 0
}

if not DISABLE_HOME_VIEW:
    register_top_menu('home', link={'text': _(u'home'), 'view': 'home', 'famfam': 'house'}, position=0)
if not SIDE_BAR_SEARCH:
    register_top_menu('search', link={'text': _(u'search'), 'view': 'search', 'famfam': 'zoom'}, children_path_regex=[r'^search/'])


def get_version():
    '''
    Return the formatted version information
    '''
    vers = ['%(major)i.%(minor)i' % __version_info__, ]

    if __version_info__['micro']:
        vers.append('.%(micro)i' % __version_info__)
    if __version_info__['releaselevel'] != 'final':
        vers.append('%(releaselevel)s%(serial)i' % __version_info__)
    return ''.join(vers)


__version__ = get_version()

if 'django.contrib.admin' in settings.INSTALLED_APPS:
    register_setup(admin_site)

register_tool(maintenance_menu)
register_tool(statistics)
register_tool(diagnostics)

if 'sentry' in settings.INSTALLED_APPS:
    register_tool(sentry)
