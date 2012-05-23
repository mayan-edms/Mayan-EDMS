from django.utils.translation import ugettext_lazy as _

from navigation.api import register_top_menu, Link

tool_menu = register_top_menu('tools', link=Link(text=_(u'tools'), view='tools_list', sprite='wrench'), position=-3)
