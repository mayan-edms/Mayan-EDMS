from __future__ import absolute_import

import psutil

from django.utils.translation import ugettext_lazy as _

from smart_settings import ClusterScope, LocalScope

from .icons import icon_tool_link
from .links import tool_link
from .literals import (DEFAULT_JOB_QUEUE_POLL_INTERVAL, DEFAULT_DEAD_JOB_REMOVAL_INTERVAL,
    DEFAULT_MAX_CPU_LOAD, DEFAULT_MAX_MEMORY_USAGE)

label = _(u'Job processor')
description = _(u'Handles queuing of jobs to be processed by the cluster nodes.')
icon = icon_tool_link
dependencies = ['navigation', 'icons', 'permissions']
tool_links = [tool_link]
settings = [
    {
        'name': 'QUEUE_POLL_INTERVAL',
        'default': DEFAULT_JOB_QUEUE_POLL_INTERVAL,
        'description': _(u'job queue poll interval (in seconds)'),
        'scopes': [ClusterScope()]
    },
    {
        'name': 'DEAD_JOB_REMOVAL_INTERVAL',
        'default': DEFAULT_DEAD_JOB_REMOVAL_INTERVAL,
        'description': _(u'Interval of time (in seconds) to check the cluster for and remove unresponsive jobs.'),
        'scopes': [ClusterScope()]
    },
    {
        'name': 'MAX_CPU_LOAD',
        'default': DEFAULT_MAX_CPU_LOAD,
        'description': _(u'Nodes with a CPU load above this will not process jobs from the queue.'),
        'scopes': [ClusterScope(), LocalScope()]
    },
    {
        'name': 'MAX_MEMORY_USAGE',
        'default': DEFAULT_MAX_MEMORY_USAGE,
        'description': _(u'Nodes with a memory usage above this will not process jobs from the queue.'),
        'scopes': [ClusterScope(), LocalScope()]
    },
    {
        'name': 'NODE_MAX_WORKERS',
        'default': len(psutil.cpu_percent(interval=0.1, percpu=True)),  # Get CPU/cores count
        'description': _(u'Maximum amount of workers to launch per node, default is number or CPUs or cores.'),
        'scopes': [LocalScope()]
    },
]
