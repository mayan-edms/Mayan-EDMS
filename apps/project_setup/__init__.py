from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import register_top_menu, Link

from .icons import icon_setup

setup_menu = register_top_menu('setup_menu', link=Link(text=_(u'setup'), view='setup_list', icon=icon_setup), position=-2)
