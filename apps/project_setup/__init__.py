from __future__ import absolute_import

from navigation.api import register_top_menu

from .links import link_setup

setup_menu = register_top_menu('setup_menu', link_setup, position=-2)
