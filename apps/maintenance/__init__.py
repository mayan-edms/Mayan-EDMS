from __future__ import absolute_import

from navigation.api import bind_links

from .links import maintenance_menu, maintenance_execute
from .api import MaintenanceTool

bind_links(['maintenance_menu'], maintenance_menu, menu_name='secondary_menu')
bind_links([MaintenanceTool], maintenance_execute)
