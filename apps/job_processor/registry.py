from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from smart_settings import ClusterScope

from .icons import icon_tool_link
from .links import tool_link
from .literals import DEFAULT_JOB_QUEUE_POLL_INTERVAL, DEFAULT_DEAD_JOB_REMOVAL_INTERVAL

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
    }    
]
