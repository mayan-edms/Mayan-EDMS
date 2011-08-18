from django.utils.translation import ugettext_lazy as _

from navigation.api import register_top_menu

#TODO: FIXME dynamic children_path_regext on api register_setup
register_top_menu('setup_menu', link={'text': _(u'setup'), 'view': 'setup_list', 'famfam': 'cog'}, children_path_regex=[r'^settings/', r'^user_management/', r'^permissions', r'^documents/type', r'^metadata/setup', r'sources/setup'], position=-2)
