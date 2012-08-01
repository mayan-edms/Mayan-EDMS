from __future__ import absolute_import

import logging

from lock_manager.decorators import simple_locking

from .models import Node, ClusteringConfig

LOCK_EXPIRE = 10

logger = logging.getLogger(__name__)


@simple_locking('node_heartbeat', 10)
def node_heartbeat():
    logger.debug('starting')
    node = Node.objects.myself()
    node.save()


@simple_locking('house_keeping', 10)
def house_keeping():
    logger.debug('starting')
    ClusteringConfig.objects.delete_dead_nodes()
    
