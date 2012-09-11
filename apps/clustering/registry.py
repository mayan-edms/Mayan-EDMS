from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from smart_settings import ClusterScope

from .icons import icon_tool_link
from .literals import (DEFAULT_NODE_HEARTBEAT_INTERVAL, DEFAULT_NODE_HEARTBEAT_TIMEOUT,
    DEFAULT_DEAD_NODE_REMOVAL_INTERVAL)

label = _(u'Clustering')
description = _(u'Registers nodes into a Citadel (Mayan EDMS cluster).')
dependencies = ['app_registry', 'icons', 'navigation', 'scheduler']
icon = icon_tool_link
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
