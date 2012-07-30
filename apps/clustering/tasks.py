from __future__ import absolute_import

import logging

from lock_manager.decorators import simple_locking

from .models import Node

LOCK_EXPIRE = 10

logger = logging.getLogger(__name__)


@simple_locking('refresh_node', 10)
def refresh_node():
    logger.debug('starting')
    node = Node.objects.myself()  # Automatically calls the refresh() method too
