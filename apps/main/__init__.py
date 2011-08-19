from django.utils.translation import ugettext_lazy as _

from navigation.api import register_top_menu
from navigation.api import register_links
from project_setup.api import register_setup
from project_tools.api import register_tool

from main.conf.settings import SIDE_BAR_SEARCH
from main.conf.settings import DISABLE_HOME_VIEW


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser

maintenance_menu = {'text': _(u'maintenance'), 'view': 'maintenance_menu', 'famfam': 'wrench', 'icon': 'wrench.png'}
statistics = {'text': _(u'statistics'), 'view': 'statistics', 'famfam': 'table', 'icon': 'blackboard_sum.png'}
diagnostics = {'text': _(u'diagnostics'), 'view': 'diagnostics', 'famfam': 'pill', 'icon': 'pill.png'}
sentry = {'text': _(u'sentry'), 'url': '/sentry', 'famfam': 'bug', 'icon': 'bug.png', 'condition': is_superuser}
admin_site = {'text': _(u'admin site'), 'url': '/admin', 'famfam': 'keyboard', 'icon': 'keyboard.png', 'condition': is_superuser}

__version_info__ = {
    'major': 0,
    'minor': 8,
    'micro': 3,
    'releaselevel': 'final',
    'serial': 0
}

if not DISABLE_HOME_VIEW:
    register_top_menu('home', link={'text': _(u'home'), 'view': 'home', 'famfam': 'house'}, position=0)
if not SIDE_BAR_SEARCH:
    register_top_menu('search', link={'text': _(u'search'), 'view': 'search', 'famfam': 'zoom'}, children_path_regex=[r'^search/'])


def get_version():
    """
    Return the formatted version information
    """
    vers = ["%(major)i.%(minor)i" % __version_info__, ]

    if __version_info__['micro']:
        vers.append(".%(micro)i" % __version_info__)
    if __version_info__['releaselevel'] != 'final':
        vers.append('%(releaselevel)s%(serial)i' % __version_info__)
    return ''.join(vers)

__version__ = get_version()

register_setup(admin_site)
register_tool(maintenance_menu)
register_tool(statistics)
register_tool(diagnostics)
register_tool(sentry)
