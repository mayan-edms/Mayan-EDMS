from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from smart_settings import ClusterScope

from .icons import icon_tool_link
from .literals import (DEFAULT_NODE_HEARTBEAT_INTERVAL, DEFAULT_NODE_HEARTBEAT_TIMEOUT,
    DEFAULT_DEAD_NODE_REMOVAL_INTERVAL)
from .links import tool_link

label = _(u'Clustering')
description = _(u'Registers nodes into a Citadel (Mayan EDMS cluster).')
dependencies = ['app_registry', 'icons', 'navigation', 'scheduler']
icon = icon_tool_link
tool_links = [tool_link]
settings = [
    {
        'name': 'NODE_HEARTBEAT_INTERVAL',
        'default': DEFAULT_NODE_HEARTBEAT_INTERVAL,
        'description': _(u'Interval of time (in seconds) for the node\'s heartbeat update to the cluster.'),
        'scopes': [ClusterScope()]
    },
    {
        'name': 'NODE_HEARTBEAT_TIMEOUT',
        'default': DEFAULT_NODE_HEARTBEAT_TIMEOUT,
        'description': _(u'After this amount of time a node without heartbeat updates is considered dead and removed from the cluster node list.'),
        'scopes': [ClusterScope()]
    },
    {
        'name': 'DEAD_NODE_REMOVAL_INTERVAL',
        'default': DEFAULT_DEAD_NODE_REMOVAL_INTERVAL,
        'description': _(u'Interval of time to check the cluster for unresponsive nodes and remove them from the cluster.'),
        'scopes': [ClusterScope()]
    },
]

# TODO: implement settings post edit clean like method for sanity checks
#def clean(self):
#    if self.node_heartbeat_interval > self.node_heartbeat_timeout:
#        raise ValidationError(_(u'Heartbeat interval cannot be greater than heartbeat timeout or else nodes will always be rated as "dead"'))
