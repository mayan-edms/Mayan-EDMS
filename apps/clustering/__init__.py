from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from scheduler.api import register_interval_job
from navigation.api import bind_links
from project_tools.api import register_tool

from .tasks import refresh_node
from .links import tool_link, node_list
from .models import Node

NODE_REFRESH_INTERVAL = 1

register_interval_job('refresh_node', _(u'Update a node\'s properties.'), refresh_node, seconds=NODE_REFRESH_INTERVAL)

register_tool(tool_link)
bind_links([Node, 'node_list'], [node_list], menu_name='secondary_menu')
