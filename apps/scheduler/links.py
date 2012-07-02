from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import Link

from .permissions import PERMISSION_VIEW_JOB_LIST

job_list = Link(text=_(u'interval job list'), view='job_list', icon='time.png', permissions=[PERMISSION_VIEW_JOB_LIST])
