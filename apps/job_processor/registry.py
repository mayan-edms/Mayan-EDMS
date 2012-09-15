from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_tool_link
from .links import tool_link

label = _(u'Job processor')
description = _(u'Handles queuing of jobs to be processed by the cluster nodes.')
icon = icon_tool_link
dependencies = ['navigation', 'icons', 'permissions']
tool_links = [tool_link]
