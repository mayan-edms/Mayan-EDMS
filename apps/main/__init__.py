from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import Link, register_top_menu

from .conf.settings import SIDE_BAR_SEARCH, DISABLE_HOME_VIEW

__author__ = 'Roberto Rosario'
__copyright__ = 'Copyright 2011 Roberto Rosario'
__credits__ = ['Roberto Rosario', ]
__license__ = 'GPL'
__maintainer__ = 'Roberto Rosario'
__email__ = 'roberto.rosario.gonzalez@gmail.com'
__status__ = 'Production'

__version_info__ = {
    'major': 0,
    'minor': 13,
    'micro': 0,
    'releaselevel': 'alpha',
    'serial': 0
}


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
if not DISABLE_HOME_VIEW:
    register_top_menu('home', link=Link(text=_(u'home'), view='home', sprite='house'), position=0)
if not SIDE_BAR_SEARCH:
    register_top_menu('search', link=Link(text=_(u'search'), view='search', sprite='zoom', children_url_regex=[r'^search/']))
