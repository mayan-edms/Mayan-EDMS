from __future__ import absolute_import, unicode_literals

from .classes import Worker

worker_fast = Worker(name='fast', nice_level=1)
worker_medium = Worker(name='medium', nice_level=18)
worker_slow = Worker(name='slow', nice_level=19)
