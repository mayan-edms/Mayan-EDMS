from django.utils.translation import ugettext_lazy as _

from navigation.api import register_top_menu

setup_link = register_top_menu('setup_menu', link={'text': _(u'setup'), 'view': 'setup_list', 'famfam': 'cog'}, position=-2)
