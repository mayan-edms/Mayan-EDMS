from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .icons import icon_app

app_registry_tool_link = Link(text=_(u'Apps'), view='app_list', icon=icon_app)#, permissions=[PERMISSION_BACKUP_JOB_VIEW])
app_list = Link(text=_(u'app list'), view='app_list', icon=icon_app)#, permissions=[PERMISSION_BACKUP_JOB_VIEW])
