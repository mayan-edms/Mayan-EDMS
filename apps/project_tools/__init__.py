from django.utils.translation import ugettext_lazy as _

from navigation.api import register_top_menu

tool_link = register_top_menu('tools', link={'text': _(u'tools'), 'view': 'tools_list', 'famfam': 'wrench'}, position=-3)
