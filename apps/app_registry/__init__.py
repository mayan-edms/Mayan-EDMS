from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from icons.literals import APP
from navigation.api import bind_links
from project_tools.api import register_tool
from project_setup.api import register_setup

from .models import App
from .links import app_registry_tool_link, app_list
from .api import register_app

register_tool(app_registry_tool_link)
register_app('app_registry', label=_(u'App registry'), icon=APP)
bind_links(['app_list'], [app_list], menu_name='secondary_menu')
