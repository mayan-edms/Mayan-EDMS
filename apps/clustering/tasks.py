from __future__ import absolute_import

import logging

from lock_manager.decorators import simple_locking

from .models import Node
from .signals import node_heartbeat

LOCK_EXPIRE = 10

logger = logging.getLogger(__name__)


@simple_locking('node_heartbeat', 10)
def send_heartbeat():
    logger.debug('starting')
    node = Node.objects.myself()
    node.send_heartbeat()
    node_heartbeat.send(sender=node, node=node)


@simple_locking('house_keeping', 10)
def house_keeping():
    logger.debug('starting')
    Node.objects.check_dead_nodes()
    
