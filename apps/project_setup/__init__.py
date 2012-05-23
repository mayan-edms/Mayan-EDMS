from django.utils.translation import ugettext_lazy as _

from navigation.api import register_top_menu, Link

setup_menu = register_top_menu('setup_menu', link=Link(text=_(u'setup'), view='setup_list', sprite='cog'), position=-2)
