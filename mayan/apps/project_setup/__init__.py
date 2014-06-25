from __future__ import absolute_import

from navigation.api import register_top_menu

from .links import link_setup

setup_link = register_top_menu('setup_menu', link=link_setup, position=-2)
