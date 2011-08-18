from django.utils.translation import ugettext_lazy as _

from navigation.api import register_top_menu


#TODO: FIXME dynamic children_path_regext on api register_setup
#register_top_menu('setup_menu', link={'text': _(u'setup'), 'view': 'setup_list', 'famfam': 'cog'}, children_path_regex=[r'^settings/', r'^user_management/', r'^permissions', r'^documents/type', r'^metadata/setup', r'sources/setup'], position=-2)


register_top_menu('tools', link={'text': _(u'tools'), 'view': 'tools_list', 'famfam': 'wrench'}, children_views=['statistics', 'history_list', 'formats_list'], position=-3)
#register_links(['tools_menu', 'statistics', 'history_list', 'history_view', 'formats_list'], [tools_menu, statistics, history_list, formats_list, sentry], menu_name='secondary_menu')
