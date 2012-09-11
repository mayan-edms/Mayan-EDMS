from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_scheduler_tool_link
from .links import scheduler_tool_link

label = _(u'Scheduler')
description = _(u'Executes timed tasks.')
dependencies = ['app_registry', 'icons', 'navigation']
icon = icon_scheduler_tool_link
tool_links = [scheduler_tool_link]
