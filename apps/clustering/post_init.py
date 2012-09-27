from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.db import transaction, DatabaseError

from scheduler.api import LocalScheduler
from navigation.api import bind_links

from .tasks import send_heartbeat, house_keeping
from .links import tool_link, node_list
from .models import Node
from .settings import NODE_HEARTBEAT_INTERVAL, DEAD_NODE_REMOVAL_INTERVAL


@transaction.commit_on_success
def add_clustering_jobs():
    clustering_scheduler = LocalScheduler('clustering', _(u'Clustering'))
    try:
        # TODO: auto convert setting using JSON loads
        clustering_scheduler.add_interval_job('send_heartbeat', _(u'Update a node\'s properties.'), send_heartbeat, seconds=int(NODE_HEARTBEAT_INTERVAL))
        clustering_scheduler.add_interval_job('house_keeping', _(u'Check for unresponsive nodes in the cluster list.'), house_keeping, seconds=int(DEAD_NODE_REMOVAL_INTERVAL))
    except DatabaseError:
        transaction.rollback()
    clustering_scheduler.start()


add_clustering_jobs()
bind_links([Node, 'node_list'], [node_list], menu_name='secondary_menu')
