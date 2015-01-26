from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation.api import register_top_menu
from project_setup.api import register_setup
from project_tools.api import register_tool

from .links import admin_site, maintenance_menu
from .classes import FrontPageButton  # NOQA

register_top_menu('home', link={'text': _('Home'), 'view': 'main:home', 'famfam': 'house'}, position=0)
register_setup(admin_site)
register_tool(maintenance_menu)
