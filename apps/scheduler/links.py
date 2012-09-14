from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import PERMISSION_VIEW_JOB_LIST, PERMISSION_VIEW_SCHEDULER_LIST
from .icons import icon_scheduler_tool_link, icon_scheduler_list, icon_job_list

scheduler_tool_link = Link(text=_(u'local schedulers'), view='scheduler_list', icon=icon_scheduler_tool_link, permissions=[PERMISSION_VIEW_SCHEDULER_LIST])
scheduler_list = Link(text=_(u'scheduler list'), view='scheduler_list', icon=icon_scheduler_list, permissions=[PERMISSION_VIEW_SCHEDULER_LIST])
job_list = Link(text=_(u'interval job list'), view='job_list', args='object.name', icon=icon_job_list, permissions=[PERMISSION_VIEW_JOB_LIST])
