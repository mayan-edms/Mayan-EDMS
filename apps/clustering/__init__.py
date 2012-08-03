from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.db import transaction, DatabaseError

from scheduler.api import LocalScheduler
from navigation.api import bind_links
from project_tools.api import register_tool
from project_setup.api import register_setup

from .tasks import send_heartbeat, house_keeping
from .links import tool_link, node_list, clustering_config_edit, setup_link
from .models import Node, ClusteringConfig

ClusteringConfig()
@transaction.commit_on_success
def add_clustering_jobs():
    clustering_scheduler = LocalScheduler('clustering', _(u'Clustering'))
    try:
        clustering_scheduler.add_interval_job('send_heartbeat', _(u'Update a node\'s properties.'), send_heartbeat, seconds=ClusteringConfig.get().node_heartbeat_interval)
        clustering_scheduler.add_interval_job('house_keeping', _(u'Check for unresponsive nodes in the cluster list.'), house_keeping, seconds=ClusteringConfig.get().dead_node_removal_interval)
    except DatabaseError:
        transaction.rollback()
    clustering_scheduler.start()


add_clustering_jobs()
register_tool(tool_link)
register_setup(setup_link)
bind_links([Node, 'node_list'], [node_list], menu_name='secondary_menu')
bind_links(['clustering_config_edit'], [clustering_config_edit], menu_name='secondary_menu')
