from django.utils.translation import ugettext_lazy as _

from navigation.api import register_top_menu


#TODO: FIXME dynamic children_path_regext on api register_setup
register_top_menu('tools', link={'text': _(u'tools'), 'view': 'tools_list', 'famfam': 'wrench'}, children_views=['statistics', 'history_list', 'formats_list'], position=-3)
