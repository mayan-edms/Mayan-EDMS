from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from scheduler.api import LocalScheduler
from navigation.api import bind_links
from project_tools.api import register_tool

from .tasks import node_heartbeat, house_keeping
from .links import tool_link, node_list
from .models import Node, ClusteringConfig

clustering_scheduler = LocalScheduler('clustering', _(u'Clustering'))
clustering_scheduler.add_interval_job('node_heartbeat', _(u'Update a node\'s properties.'), node_heartbeat, seconds=ClusteringConfig.get().node_heartbeat_interval)
clustering_scheduler.add_interval_job('house_keeping', _(u'Check for unresponsive nodes in the cluster list.'), house_keeping, seconds=1)
clustering_scheduler.start()

register_tool(tool_link)
bind_links([Node, 'node_list'], [node_list], menu_name='secondary_menu')
