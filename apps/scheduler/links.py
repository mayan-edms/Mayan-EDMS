from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import Link

from .permissions import PERMISSION_VIEW_JOB_LIST, PERMISSION_VIEW_SCHEDULER_LIST

scheduler_tool_link = Link(text=_(u'local schedulers'), view='scheduler_list', icon='time.png', permissions=[PERMISSION_VIEW_SCHEDULER_LIST])
scheduler_list = Link(text=_(u'scheduler list'), view='scheduler_list', sprite='time', permissions=[PERMISSION_VIEW_SCHEDULER_LIST])
job_list = Link(text=_(u'interval job list'), view='job_list', args='object.name', sprite='timeline_marker', permissions=[PERMISSION_VIEW_JOB_LIST])
