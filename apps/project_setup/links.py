from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import register_top_menu, Link

from .icons import icon_setup

link_setup=Link(text=_(u'setup'), view='setup_list', icon=icon_setup)
