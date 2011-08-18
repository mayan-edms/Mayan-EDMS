from django.utils.translation import ugettext_lazy as _

from navigation.api import register_top_menu
from navigation.api import register_links
from history import history_list
from converter import formats_list
from project_setup.api import register_setup

from main.conf.settings import SIDE_BAR_SEARCH
from main.conf.settings import DISABLE_HOME_VIEW


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser

check_settings = {'text': _(u'settings'), 'view': 'setting_list', 'famfam': 'cog'}
statistics = {'text': _(u'statistics'), 'view': 'statistics', 'famfam': 'table'}
diagnostics = {'text': _(u'diagnostics'), 'view': 'diagnostics', 'famfam': 'pill'}
tools_menu = {'text': _(u'tools'), 'view': 'tools_menu', 'famfam': 'wrench'}
admin_site = {'text': _(u'admin site'), 'url': '/admin', 'famfam': 'keyboard', 'icon': 'keyboard.png', 'condition': is_superuser}
sentry = {'text': _(u'sentry'), 'url': '/sentry', 'famfam': 'bug', 'condition': is_superuser}
document_types = {'text': _(u'document types'), 'view': 'document_type_list', 'famfam': 'layout', 'children_view_regex': ['document_type', 'setup_document_type']}

__version_info__ = {
    'major': 0,
    'minor': 8,
    'micro': 2,
    'releaselevel': 'final',
    'serial': 0
}

#setup_views = []
#setup_views.extend(permission_views)
#setup_views.extend(user_management_views)
#setup_views.extend(['setting_list'])

if not DISABLE_HOME_VIEW:
    register_top_menu('home', link={'text': _(u'home'), 'view': 'home', 'famfam': 'house'}, position=0)
if not SIDE_BAR_SEARCH:
    register_top_menu('search', link={'text': _(u'search'), 'view': 'search', 'famfam': 'zoom'}, children_path_regex=[r'^search/'])

register_top_menu('tools', link=tools_menu, children_views=['statistics', 'history_list', 'formats_list'], position=-3)
register_links(['tools_menu', 'statistics', 'history_list', 'history_view', 'formats_list'], [tools_menu, statistics, history_list, formats_list, sentry], menu_name='secondary_menu')


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
