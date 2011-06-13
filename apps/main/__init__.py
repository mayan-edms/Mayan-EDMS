from django.utils.translation import ugettext_lazy as _

from navigation.api import register_top_menu
from permissions import role_list, permission_views
from user_management import user_list, group_list, user_management_views
from navigation.api import register_links
from history import history_list
from documents import document_type_views

from main.conf.settings import SIDE_BAR_SEARCH


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser

check_settings = {'text': _(u'settings'), 'view': 'setting_list', 'famfam': 'cog'}
statistics = {'text': _(u'statistics'), 'view': 'statistics', 'famfam': 'table'}
diagnostics = {'text': _(u'diagnostics'), 'view': 'diagnostics', 'famfam': 'pill'}
tools_menu = {'text': _(u'tools'), 'view': 'tools_menu', 'famfam': 'wrench'}
admin_site = {'text': _(u'admin site'), 'url': '/admin', 'famfam': 'keyboard', 'condition': is_superuser}
sentry = {'text': _(u'sentry'), 'url': '/sentry', 'famfam': 'bug', 'condition': is_superuser}
document_types = {'text': _(u'document types'), 'view': 'document_type_list', 'famfam': 'layout'}

__version_info__ = {
    'major': 0,
    'minor': 7,
    'micro': 4,
    'releaselevel': 'final',
    'serial': 0
}

#setup_views = []
#setup_views.extend(permission_views)
#setup_views.extend(user_management_views)
#setup_views.extend(['setting_list'])

register_top_menu('home', link={'text': _(u'home'), 'view': 'home', 'famfam': 'house'}, position=0)
if not SIDE_BAR_SEARCH:
    register_top_menu('search', link={'text': _(u'search'), 'view': 'search', 'famfam': 'zoom'})
register_top_menu('tools', link=tools_menu, children_views=['statistics', 'history_list'])
#register_top_menu('setup_menu', link={'text': _(u'setup'), 'view': 'setting_list', 'famfam': 'cog'}, children=setup_views)
register_top_menu('setup_menu', link={'text': _(u'setup'), 'view': 'setting_list', 'famfam': 'cog'}, children_path_regex=[r'^settings/', r'^user_management/', r'^permissions', r'^documents/type'])
register_top_menu('about', link={'text': _(u'about'), 'view': 'about', 'famfam': 'information'})

register_links(['tools_menu', 'statistics', 'history_list', 'history_view'], [tools_menu, statistics, history_list, sentry], menu_name='secondary_menu')

tool_links = [check_settings, role_list, user_list, group_list, document_types, admin_site]
register_links(['setting_list'], tool_links, menu_name='secondary_menu')
register_links(permission_views, tool_links, menu_name='secondary_menu')
register_links(user_management_views, tool_links, menu_name='secondary_menu')
register_links(document_type_views, tool_links, menu_name='secondary_menu')


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
